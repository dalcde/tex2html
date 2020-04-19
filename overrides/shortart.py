
from plasTeX import Command
from plasTeX.Packages.report import *
from plasTeX.Packages.hyperref import *

def ProcessOptions(options, document):
    from plasTeX.Packages import report
    report.ProcessOptions(options, document)
    document.context['thesection'].format = '${section}'
    document.context['theindex'].counter = 'section'
    document.context['theindex'].level = Environment.SECTION_LEVEL
    document.context['printindex'].counter = 'section'
    document.context['printindex'].level = Command.SECTION_LEVEL
    document.context['bibliography'].counter = 'section'
    document.context['bibliography'].level = Command.SECTION_LEVEL

class appendices(Command):

    class thesection(TheCounter):
        format = '${section.Alph}'

    def invoke(self, tex):
        self.ownerDocument.context.counters['section'].setcounter(0)
        self.ownerDocument.context['thesection'] = type(self).thesection

class separator(Command):
    pass
