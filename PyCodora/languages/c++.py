# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

from ..base import BaseCodeBlock, BaseGenerator, BaseSnippets
from ..helpers import method_not_supported


class CodeBlock(BaseCodeBlock):
    def __init__(self):
        super().__init__('c++')

    @method_not_supported
    def add_module(self, module):
        pass

    @method_not_supported
    def add_function(self, name, return_type, *args):
        pass


class Generator(BaseGenerator):
    def __init__(self):
        super().__init__('c++')
        self.context = CodeBlock


class Snippets(BaseSnippets):
    def __init__(self):
        super().__init__('c++')


CODEBLOCK = CodeBlock
GENERATOR = Generator
SNIPPETS = Snippets
