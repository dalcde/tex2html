#!/usr/bin/env python

import sys, os, re, shutil
from pathlib import Path
import plasTeX.Renderers.HTML5
from plasTeX.Renderers import Renderer as BaseRenderer
from plasTeX.Renderers import Renderable as _Renderable
from plasTeX.Logging import getLogger
import pyduktape
import jinja2

ctx = pyduktape.DuktapeContext()
ctx.eval_js_file("%s/katex.min.js" % os.path.dirname(__file__))

log = getLogger()

def _katex(string, display):
    string = string.replace("\n", " ")
    ctx.set_globals(input=string)
    if display:
        return ctx.eval_js("katex.renderToString(input, {displayMode: true, throwOnError: false})")
    else:
        return ctx.eval_js("katex.renderToString(input, {displayMode: false, throwOnError: false})")

# Monkey patch to use our mathEngine
_Renderable.displayMath = property(lambda obj: _katex(obj.childrenSource, True), None)
_Renderable.inlineMath = property(lambda obj: _katex(obj.childrenSource, False), None)

# Support for Jinja2 templates
from jinja2 import Environment

def jinja2template(s, encoding='utf8'):
    env = Environment(trim_blocks=True, lstrip_blocks=True)

    def renderjinja2(obj, s=s):
        tvars = {'here':obj,
                 'obj':obj,
                 'container':obj.parentNode,
                 'config':obj.ownerDocument.config,
                 'context':obj.ownerDocument.context,
                 'templates':obj.renderer}

        tpl = env.from_string(s)
        return tpl.render(tvars)

    return renderjinja2

class Renderer(BaseRenderer):
    """ Renderer for page template based documents """

    outputType = str

    fileExtension = '.html'
    imageTypes = ['.svg', '.png','.jpg','.jpeg','.gif']
    vectorImageTypes = ['.svg']

    def __init__(self, *args, **kwargs):
        BaseRenderer.__init__(self, *args, **kwargs)

    def textDefault(self, node):
        """
        Default renderer for text nodes

        This method makes sure that special characters are converted to
        entities.

        Arguments:
        node -- the Text node to process

        """

        if not(getattr(node, 'isMarkup', None)):
            node = node.replace('&', '&amp;')
            node = node.replace('<', '&lt;')
            node = node.replace('>', '&gt;')
        return self.outputType(node)

    def loadTemplates(self, document):
        """ Load and compile page templates """

        # Load package templates
        cwd = Path(__file__).parent

        self.importDirectory(Path(plasTeX.Renderers.HTML5.__file__).parent)
        self.importDirectory(cwd / "Templates")

        # Load main template
        self.parseTemplate(cwd / "layout.jinja2", "default-layout")

        # Copy style.css if config["custom"]["css-path"] is "style.css". Otherwise,
        # it is some custom location specified by the user, and the user is
        # responsible for placing it in the right place.
        if document.config["custom"]["css-path"] == "style.css":
            shutil.copy(str(cwd / "style.css"), document.config['files']['directory'])

    def render(self, document):
        """ Load templates and render the document """
        self.loadTemplates(document)
        BaseRenderer.render(self, document)

    def importDirectory(self, templatedir: Path):
        """
        Compile all jinja2 files in the given directory

        Required Arguments:
        templatedir -- the directory to search for template files

        """
        if templatedir and templatedir.is_dir():
            # Compile multi-pt files first
            for f in templatedir.iterdir():
                if not f.is_file():
                    continue

                # Multi-pt files
                if f.suffix == ".jinja2s":
                    self.parseTemplates(f)

            # Now compile macros in individual files.  These have
            # a higher precedence than macros found in multi-pt files.
            for f in templatedir.iterdir():
                if not f.is_file():
                    continue

                if f.suffix == ".jinja2":
                    self.parseTemplate(f, f.stem)

    def setTemplate(self, template, name):
        """
        Compile template and set it in the renderer

        Required Arguments:
        template -- the content of the template to be compiled
        options -- dictionary containing the name (or names) and type
            of the template

        """

        if name is None:
            raise ValueError('No name given for template')

        names = name.split()
        if not names:
            names = [' ']

        # Compile template and add it to the renderer
        template = ''.join(template).strip()

        try:
            template = jinja2template(template)
        except Exception as msg:
            raise ValueError('Could not compile template "%s"' % names[0])

        for name in names:
            self[name] = template

    def parseTemplate(self, f: Path, name: str):
        template = f.read_text()

        try:
            self.setTemplate(template, name)
        except ValueError as msg:
            print('ERROR: {} in template {} in file {}'.format(msg, template, f))

    def parseTemplates(self, filename: Path):
        """
        Parse templates from the file and set them in the renderer

        Required Arguments:
        filename -- file to parse templates from

        Keyword Arguments:
        options -- dictionary containing initial parameters for templates
            in the file

        """
        template = []
        name = None
        with filename.open() as f:
            for i, line in enumerate(f):
                # Found a meta-data command
                if re.match(r'(default-)?\w+:', line):
                    # Purge any awaiting templates
                    if template:
                        try:
                            self.setTemplate(''.join(template), name)
                        except ValueError as msg:
                            print('ERROR: %s at line %s in file %s' % (msg, i, str(filename)))
                        name = None
                        template = []

                    # Done purging previous template, start a new one
                    _, name = line.split(':', 1)
                    name = name.strip()
                    while name.endswith('\\'):
                        name = name[:-1] + ' ' + f.readline().rstrip()

                    name = re.sub(r'\s+', r' ', name)
                elif template or (not(template) and line.strip()):
                    template.append(line)
                elif not(template) and name is not None:
                    template.append('')

        # Purge any awaiting templates
        if template:
            try:
                self.setTemplate(''.join(template), name)
            except ValueError as msg:
                print('ERROR: %s in template %s in file %s' % (msg, ''.join(template), str(filename)))

        elif name is not None and not(template):
            self.setTemplate('', name)

    def processFileContent(self, document, s):
        # Add width, height, and depth to images
        s = re.sub(r'&amp;(\S+)-(width|height|depth);(?:&amp;([a-z]+);)?',
                   self.setImageData, s)

        # Convert characters >127 to entities
        if document.config['files']['escape-high-chars']:
            s = list(s)
            for i, item in enumerate(s):
                if ord(item) > 127:
                    s[i] = '&#%.3d;' % ord(item)
            s = ''.join(s)

        # Remove empty paragraphs
        s = re.compile(r'<p>\s*</p>', re.I).sub(r'', s)

        # Add a non-breaking space to empty table cells
        s = re.compile(r'(<(td|th)\b[^>]*>)\s*(</\2>)', re.I).sub(r'\1&nbsp;\3', s)

        return BaseRenderer.processFileContent(self, document, s)

    def setImageData(self, m):
        """
        Substitute in width, height, and depth parameters in image tags

        The width, height, and depth parameters aren't known until after
        all of the output has been generated.  We have to post-process
        the files to insert this information.  This method replaces
        the &filename-width;, &filename-height;, and &filename-depth;
        placeholders with their appropriate values.

        Required Arguments:
        m -- regular expression match object that contains the filename
            and the parameter: width, height, or depth.

        Returns:
        replacement for entity

        """
        filename, parameter, units = m.group(1), m.group(2), m.group(3)

        try:
            img = self.imager.images.get(filename, self.vectorImager.images.get(filename, self.imager.staticimages.get(filename)))
            if img is not None and getattr(img, parameter) is not None:
                if units:
                    return getattr(getattr(img, parameter), units)
                return str(getattr(img, parameter))
        except KeyError: pass

        return '&%s-%s;' % (filename, parameter)
