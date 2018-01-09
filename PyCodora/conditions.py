# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

from .base import PyCodoraBase, BaseCodeBlock
from .languages import CONDITIONS, SYNTAX
from typing import Any, Callable, Optional


class Condition(PyCodoraBase):
    def __init__(self, operation: str, left: Any, right: Any,
                 on_true: Optional[Callable[[BaseCodeBlock], None]] = None,
                 on_false: Optional[Callable[[BaseCodeBlock], None]] = None):
        if not isinstance(operation, str):
            raise TypeError('`operation` must be str')
        if on_true is not None and not callable(on_true):
            raise TypeError('`on_true` must be callable')
        if on_false is not None and not callable(on_false):
            raise TypeError('`on_true` must be callable')
        self.operation = operation
        self.args = left, right
        self.callbacks = on_true, on_false
        self.context = None

    def __repr__(self):
        return '<{0} condition>'.format(self.operation)

    def __format__(self, language: str):
        code = SYNTAX[language]
        context_true = self.context()
        self.callbacks[0](context_true)
        body_true = context_true.indented_code
        if self.callbacks[1] is not None:
            code = code.get('full_condition')
            context_false = self.context()
            self.callbacks[1](context_false)
            body_false = context_false.indented_code
        else:
            code = code.get('condition')
            body_false = ''
        args = []
        for arg in self.args:
            if isinstance(arg, PyCodoraBase):
                arg = arg.format(language)
            args.append(arg)
        return code.render(condition=CONDITIONS['default'][self.operation].format(*args),
                           body=body_true, body_true=body_true, body_false=body_false)


class EqualityCondition(Condition):
    def __init__(self, *args):
        super().__init__('eq', *args)


class InequalityCondition(Condition):
    def __init__(self, *args):
        super().__init__('ne', *args)
