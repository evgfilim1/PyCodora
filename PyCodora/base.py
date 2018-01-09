from .languages import supported_languages, SYNTAX, SNIPPETS
from typing import Union, Any, Optional
from jinja2 import Template


class PyCodoraBase:
    def __format__(self, language: str):
        raise NotImplementedError

    def format(self, language: str) -> str:
        return self.__format__(language)


class BaseCodeBlock:
    def __init__(self, language: str):
        if not isinstance(language, str):
            raise TypeError('`language` must be str')
        language = language.lower()
        if language not in supported_languages:
            raise ValueError('{0} is not supported'.format(language))
        self.language = language
        self.__code = []
        self.__functions = {}

    def __str__(self):
        functions = {}
        for key in self.__functions:
            functions[key] = self.__functions[key].indented_code
        return Template('\n'.join(self.__code) + '\n').render(**functions)

    def __repr__(self):
        return '<{0} context object>'.format(self.language)

    @property
    def code(self) -> str:
        return self.__str__()

    @property
    def indented_code(self) -> str:
        code = ''
        for line in self.code.split('\n'):
            code += '{0}{1}\n'.format(' ' * 4, line)
        code = code[:-1]
        return code

    def _get_snippet(self, key: str) -> Optional[Template]:
        return SYNTAX[self.language].get(key)

    def add_line(self, line: str) -> None:
        if not isinstance(line, str):
            raise TypeError('`line` must be str')
        self.__code.append(line)

    def add_module(self, module: str) -> None:
        if not isinstance(module, str):
            raise ValueError('`module` must be str')
        line = self._get_snippet('module').render(lib=module)
        self.__code.insert(0, line)

    def add_function(self, name: str, return_type: Optional[Union[type, str]],
                     *args) -> 'BaseCodeBlock':
        from .helpers import Argument
        arg_list = []
        if not isinstance(name, str):
            raise TypeError('`name` must be str')
        if len(name) == 0:
            raise ValueError('`name` must be non-empty')
        if name in self.__functions:
            raise ValueError('`name` must be unique')
        if return_type is not None and not isinstance(return_type, (type, str)):
            raise TypeError('`return_type` must be built-in type or str')
        elif isinstance(return_type, type):
            return_type = return_type.__name__
        for arg in args:
            if not isinstance(arg, Argument):
                raise ValueError('All arguments must be `Argument` objects')
            arg_list.append(arg.format(self.language))
        f = self.context() if hasattr(self, 'context') else self.__class__()
        self.__functions.update({'{0}_body'.format(name): f})
        self.add_line(
            SYNTAX[self.language].get('function').render(type=return_type, name=name,
                                                         args=', '.join(arg_list),
                                                         body='{{{{{0}_body}}}}'.format(name))
        )
        return f

    def add_comment(self, comment: str, multiline: Optional[bool] = None) -> None:
        if not isinstance(comment, str):
            raise TypeError('`comment` must be str')
        if multiline is None and '\n' in comment:
            multiline = True
        if not multiline and '\n' in comment:
            raise ValueError('Cannot use one-line comment as we got multiline string')
        comment_type = ''
        if multiline:
            comment_type = 'multiline_'
        self.add_line(self._get_snippet('{0}comment'.format(comment_type)).render(text=comment))

    # TODO: implement
    # def add_docstring(self, docstring):
    #     pass

    def add(self, arg: Union[str, PyCodoraBase]) -> None:
        if isinstance(arg, str):
            self.add_line(arg)
        elif isinstance(arg, PyCodoraBase):
            arg.context = self.__class__
            self.add_line(arg.format(self.language))
        else:
            raise TypeError('`arg` must be str or PyCodora.base.PyCodoraBase subclass')

    def return_(self, expr: Union[PyCodoraBase, Any]) -> None:
        if isinstance(expr, PyCodoraBase):
            value = expr.format(self.language)
        else:
            value = expr
        self.add_line(self._get_snippet('return').render(value=value))


class BaseGenerator(BaseCodeBlock):
    def __init__(self, language: str):
        super().__init__(language)
        self.context = BaseCodeBlock

    def __repr__(self):
        return '<{0} generator object>'.format(self.language)

    def add_main_function(self, pass_args: bool = True) -> BaseCodeBlock:
        from .helpers import Argument
        args = []
        if pass_args:
            args.extend((Argument('argc', int), Argument('argv', 'char**')))
        return self.add_function('main', int, *args)


class BaseSnippets:
    def __init__(self, language: str):
        if not isinstance(language, str):
            raise TypeError('`language` must be str')
        language = language.lower()
        if language not in supported_languages:
            raise ValueError('{0} is not supported'.format(language))
        self.language = language

    def __getattr__(self, item):
        # Don't confuse this method with __getattribute__
        raise AttributeError('No such snippet')

    def print(self, *args, force_newline: Optional[bool] = None) -> str:
        sep = SNIPPETS[self.language].get('print_arg_sep')
        if force_newline is None:
            print_exec = SNIPPETS[self.language].get('print')
        elif force_newline:
            print_exec = SNIPPETS[self.language].get('print_newline')
        else:
            print_exec = SNIPPETS[self.language].get('print_no_newline')
        return print_exec.format(sep.join(args))
