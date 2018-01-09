# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

from .conditions import EqualityCondition, InequalityCondition
from .helpers import Argument, FunctionCall
from .languages import supported_languages
from .base import BaseCodeBlock
from pathlib import Path
from importlib import import_module

_modules = {}


def _check_supported(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(lang: str):
        _reload_languages()
        language = lang.lower()
        if language not in supported_languages:
            raise ValueError('{0} is not supported'.format(language))
        return fn(language)
    return wrapper


@_check_supported
def CodeGenerator(language: str) -> '.base.BaseGenerator':
    return _modules[language].GENERATOR()


@_check_supported
def Snippets(language: str) -> '.base.BaseSnippets':
    return _modules[language].SNIPPETS()


def _reload_languages():
    _modules.clear()
    supported_languages.clear()
    for file in (Path(__file__).parent/'languages').glob('*.py'):
        if file.name == '__init__.py':
            continue
        try:
            module = import_module('.' + file.stem, 'PyCodora.languages')
            assert hasattr(module, 'CODEBLOCK')
            assert hasattr(module, 'GENERATOR')
            assert hasattr(module, 'SNIPPETS')
        except (ImportError, AssertionError):
            continue
        supported_languages.add(file.stem)
        _modules.update({file.stem: module})
