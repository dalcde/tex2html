#!/usr/bin/env python

from plasTeX import Command, Environment
from plasTeX.Base.LaTeX.Math import MathEnvironment, displaymath, equation

from plasTeX.Packages.amsmath import *

class AlignStar(MathEnvironment):
    macroName = 'align*'

    def invoke(self, tex):
        if self.macroMode == Command.MODE_BEGIN:
            o = self.ownerDocument.createElement('displaymath')
            o.macroMode = Command.MODE_BEGIN
            self.ownerDocument.context.push(o)

            p = self.ownerDocument.createElement('aligned')
            p.macroMode = Command.MODE_BEGIN
            self.ownerDocument.context.push(p)

            return [o, p]

        elif self.macroMode == Command.MODE_END:
            p = self.ownerDocument.createElement('aligned')
            p.macroMode = Command.MODE_END
            self.ownerDocument.context.push(p)

            o = self.ownerDocument.createElement('displaymath')
            o.macroMode = Command.MODE_END
            self.ownerDocument.context.push(o)

            return [p, o]

class GatherStar(MathEnvironment):
    macroName = 'gather*'

    def invoke(self, tex):
        if self.macroMode == Command.MODE_BEGIN:
            o = self.ownerDocument.createElement('displaymath')
            o.macroMode = Command.MODE_BEGIN
            self.ownerDocument.context.push(o)

            p = self.ownerDocument.createElement('gathered')
            p.macroMode = Command.MODE_BEGIN
            self.ownerDocument.context.push(p)

            return [o, p]

        elif self.macroMode == Command.MODE_END:
            p = self.ownerDocument.createElement('gathered')
            p.macroMode = Command.MODE_END
            self.ownerDocument.context.push(p)

            o = self.ownerDocument.createElement('displaymath')
            o.macroMode = Command.MODE_END
            self.ownerDocument.context.push(o)

            return [p, o]

class aligned(Environment):
    pass

class gathered(Environment):
    pass

class multline(equation):
    class NewLine(Command):
        macroName = '\\'

        def invoke(self, tex):
            return []

class MultlineStar(displaymath):
    macroName = "multline*"

    class NewLine(Command):
        macroName = '\\'

        def invoke(self, tex):
            return []
