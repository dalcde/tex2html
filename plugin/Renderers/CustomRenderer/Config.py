from plasTeX.ConfigManager import *
from plasTeX.DOM import Node

def addConfig(config: ConfigManager):
    section = config.addSection('custom', 'CustomRenderer Options')

    section['css-path'] = StringOption(
        """ Path to CSS """,
        options='--css-path',
        default='style.css',
    )

    section['katex-css-path'] = StringOption(
        """ Path to katex.min.css """,
        options='--katex-css-path',
        default='https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css',
    )

    section['font-css-path'] = StringOption(
        """ Path to font css file. This should import the Google fonts Lora and Marcellus SC """,
        options='--font-css-path',
        default='https://fonts.googleapis.com/css?family=Lora|Marcellus+SC',
    )

    section['display-toc'] = BooleanOption(
        """ Display table of contents on each page """,
        options='--display-toc !--no-display-toc',
        default=True,
    )
