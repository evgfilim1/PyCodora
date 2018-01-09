from ..base import BaseCodeBlock, BaseGenerator, BaseSnippets
from . import SNIPPETS as S


class CodeBlock(BaseCodeBlock):
    def __init__(self):
        super().__init__('python')


class Generator(BaseGenerator):
    def __init__(self):
        super().__init__('python')
        self.context = CodeBlock


class Snippets(BaseSnippets):
    def __init__(self):
        super().__init__('python')

    def ifmain(self, return_: bool = False):
        key = 'ifmain'
        if return_:
            key += '_return'
        return S[self.language].get(key)


CODEBLOCK = CodeBlock
GENERATOR = Generator
SNIPPETS = Snippets
