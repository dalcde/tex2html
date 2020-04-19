from plasTeX import Command, VerbatimEnvironment

class useimager(VerbatimEnvironment):
    pass

class tph(Command):
    doCharSubs = False

    # see hyperref.texorpdfstring
    def invoke(self, tex):
        tex.readArgument()
        tex.readArgument()
        _, source = tex.readArgumentAndSource()
        self.html = source[1:-1]
