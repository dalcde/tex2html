import re
from plasTeX import TheCounter

def counter_invoke(self, tex):
    def counterValue(m):
      """ Replace the counter values """
      name = m.group(1)

      # If there is a reference to another \\thecounter, invoke it
      if name.startswith('the') and name != re.sub(r'^the', '', self.__class__.__name__):
          return ''.join(tex.expandTokens(self.ownerDocument.createElement(name).invoke(tex)))

      # Get formatted value of the requested counter
      format = m.group(2)
      if not format:
          format = 'arabic'

      return getattr(self.ownerDocument.context.counters[name], format)

    format = re.sub(r'\$(\w+)', r'${\1}', self.format)
    if self.format is None:
      format = '${%s.arabic}' % self.nodeName[3:]

    t = re.sub(r'\$\{\s*(\w+)(?:\.(\w+))?\s*\}', counterValue, format)

    return tex.textTokens(t)

TheCounter.invoke = counter_invoke

from plasTeX import NewCommand
from plasTeX.Context import Context, macrolog
from plasTeX.Tokenizer import Tokenizer

def newcommand(self, name, nargs=0, definition=None, opt=None):
    """
    Create a \\newcommand

    Required Arguments:
    name -- name of the macro to create
    nargs -- integer number of arguments that the macro has
    definition -- string containing the LaTeX definition
    opt -- string containing the LaTeX code to use in the
      optional argument

    Examples::
      c.newcommand('bold', 1, r'\\textbf{#1}')
      c.newcommand('foo', 2, r'{\\bf #1#2}', opt='myprefix')

    """
    # Macro already exists
    if name in list(self.keys()):
      macrolog.debug('redefining command "%s"', name)

    if nargs is None:
      nargs = 0
    assert isinstance(nargs, int), 'nargs must be an integer'

    if isinstance(definition, str):
        definition = list(Tokenizer(definition, self))

    if isinstance(opt, str):
        opt = list(Tokenizer(opt, self))

    macrolog.debug('creating newcommand %s', name)
    newclass = type(name, (NewCommand,),
                 {'nargs':nargs, 'opt':opt, 'definition':definition})

    self.addGlobal(name, newclass)

Context.newcommand = newcommand
