from plasTeX.ConfigManager import *
from plasTeX.DOM import Node

config = ConfigManager()

section = config.add_section('custom')

config.add_category('custom', 'CustomRenderer Options')

section['css-path'] = StringOption(
    """ Path to CSS """,
    options='--css-path',
    category='custom',
    default='style.css',
)

section['katex-css-path'] = StringOption(
    """ Path to katex.min.css """,
    options='--katex-css-path',
    category='custom',
    default='https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css',
)

section['font-css-path'] = StringOption(
    """ Path to font css file. This should import the Google fonts Lora and Marcellus SC """,
    options='--font-css-path',
    category='custom',
    default='https://fonts.googleapis.com/css?family=Lora|Marcellus+SC',
)

section['display-toc'] = BooleanOption(
    """ Display table of contents on each page """,
    options='--display-toc !--no-display-toc',
    category='custom',
    default=True,
)

section['localtoc-level'] = IntegerOption(
    """ Create local toc above this level """,
    options='--localtoc-level',
    category='custom',
    default=Node.DOCUMENT_LEVEL-1,
)

section['breadcrumbs-level'] = IntegerOption(
    """ Create breadcrumbs from this level """,
    options='--breadcrumbs-level',
    category='custom',
    default=-10,
)

section['filters'] = MultiOption(
    """Comma separated list of commands to invoke on each output page.""",
    options='--filters',
    category='custom',
    default='',
)
