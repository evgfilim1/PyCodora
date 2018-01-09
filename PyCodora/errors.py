# PyCodora
# Copyright © 2018 Evgeniy Filimonov <evgfilim1 (at) gmail (dot) com>
# See full NOTICE at http://github.com/evgfilim1/PyCodora

class NotSupported(RuntimeError):
    def __init__(self, what, language):
        super().__init__('{0} is not supported for {1}'.format(what, language))


class MethodNotSupported(NotSupported):
    def __init__(self, name, language):
        super().__init__('Method {0}'.format(name), language)
