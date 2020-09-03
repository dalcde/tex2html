from plasTeX import Command, VerbatimEnvironment
from plasTeX.Tokenizer import EscapeSequence

class useimager(VerbatimEnvironment):
    pass

class info(Command):
    def invoke(self, tex):
        text = tex.readArgument()
        tex.pushToken(EscapeSequence("footnote"))
        return text

class tph(Command):
    doCharSubs = False

    # see hyperref.texorpdfstring
    def invoke(self, tex):
        tex.readArgument()
        tex.readArgument()
        _, source = tex.readArgumentAndSource()
        self.html = source[1:-1]

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
