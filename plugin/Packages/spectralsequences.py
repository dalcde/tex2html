from plasTeX import VerbatimEnvironment, Command

class sseqpage(VerbatimEnvironment):
    pass

class sseqdata(VerbatimEnvironment):
    pass

class NewSseqGroup(Command):
    args = 'a:cs b c:nox'

class NewSseqCommand(Command):
    args = 'a:cs b c:nox'

class DeclareSseqCommand(Command):
    args = 'a:cs b c:nox'

class SseqNewFamily(Command):
    args = 'a'

class SseqErrorToWarning(Command):
    args = 'a'

class sseqset(Command):
    args = 'a'

class printpage(Command):
    args = '[ args ]'
