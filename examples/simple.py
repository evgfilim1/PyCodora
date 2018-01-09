# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

from PyCodora import CodeGenerator, Argument, FunctionCall, EqualityCondition, InequalityCondition, Snippets


def generate_cpp():
    code = CodeGenerator('C++')
    snippets = Snippets('C++')

    code.add_module('iostream')

    bar = code.add_function('bar', int, Argument('n', int))
    bar.add_comment('This is a bar function that does\n almost nothing')
    bar.add(EqualityCondition('n', 2, (lambda context: context.return_(2048)),
                              (lambda context: context.return_('n - 2'))))

    foo = code.add_function('foo', int, Argument('n', int))
    foo.add_comment('This is foo function')
    foo.return_(FunctionCall('bar', 'n', inline=True))

    main = code.add_main_function(pass_args=False)
    main.add(InequalityCondition(FunctionCall('foo', 44, inline=True), 42,
                                 (lambda context: context.return_(1))))
    main.add(snippets.print('"Hello from PyCodora!"'))
    main.return_(0)

    print(code)


def generate_python():
    code = CodeGenerator('Python')
    snippets = Snippets('Python')

    code.add_module('sys')

    bar = code.add_function('bar', int, Argument('n', int))
    bar.add_comment('This is a bar function that does\n almost nothing')
    bar.add(EqualityCondition('n', 2, (lambda context: context.return_(2048)),
                              (lambda context: context.return_('n - 2'))))

    foo = code.add_function('foo', int, Argument('n', int))
    foo.add_comment('This is foo function')
    foo.return_(FunctionCall('bar', 'n', inline=True))

    main = code.add_main_function(pass_args=False)
    main.add(InequalityCondition(FunctionCall('foo', 44, inline=True), 42,
                                 (lambda context: context.return_(1))))
    main.add(snippets.print('"Hello from PyCodora!"'))
    main.return_(0)

    code.add(snippets.ifmain(return_=True))

    print(code)


if __name__ == '__main__':
    generate_cpp()
    print('================')
    generate_python()
