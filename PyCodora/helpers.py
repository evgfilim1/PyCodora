# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

from .base import PyCodoraBase
from .errors import MethodNotSupported
from .languages import SYNTAX
from functools import wraps
from typing import Union, Optional, Any


class FunctionCall(PyCodoraBase):
    def __init__(self, name: str, *args, inline: bool = False):
        if not isinstance(name, str):
            raise TypeError('`name` must be str')
        if len(name) == 0:
            raise ValueError('`name` must be non-empty')
        self.name = name
        self.args = args
        self.inline = inline

    def __format__(self, language: str):
        args = ''
        for arg in self.args:
            args += '{0}, '.format(arg)
        args = args[:-2]
        key = 'function_call'
        if self.inline:
            key += '_inline'
        return SYNTAX[language].get(key).render(name=self.name, args=args)


class Argument(PyCodoraBase):
    def __init__(self, name: str, arg_type: Optional[Union[type, str]] = None,
                 default: Optional[Any] = None):
        if arg_type is not None and not isinstance(arg_type, (type, str)):
            raise TypeError('`arg_type` must be built-in type or str')
        elif isinstance(arg_type, type):
            arg_type = arg_type.__name__
        if not isinstance(name, str):
            raise TypeError('`name` must be str')
        if len(name) == 0:
            raise ValueError('`name` must be non-empty')
        if default is not None and isinstance(arg_type, type) and not isinstance(default, arg_type):
            raise TypeError('`default` must be instance of `arg_type`')
        self.name = name
        self.type = arg_type
        self.default = default

    def __format__(self, language: str):
        if self.default is not None:
            arg = SYNTAX[language].get('arg_default')
        else:
            arg = SYNTAX[language].get('arg')
        return arg.render(type=self.type, name=self.name, default=self.default)


def method_not_supported(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        raise MethodNotSupported(fn.__qualname__, self.language)
    return wrapper
