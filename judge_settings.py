import datetime

COMPILERS = {
    'adb' : ('Ada', 'gnat 4.5.2'),
    'bas' : ('Basic', 'fbc 0.21.1'),
    'boo' : ('Boo', 'boo 0.9.4.9'),
    'c'   : ('C', 'gcc 4.5.2'),
    'cpp' : ('C++', 'g++ 4.5.2'),
    'cs'  : ('C#', 'gmcs 2.10.1'),
    'd'   : ('D', 'dmd 1.066'),
    'lua' : ('Lua', 'luac 5.1.4 '),
    'ml'  : ('Ocaml', 'ocaml 3.12.0'),
    'pas' : ('Pascal', 'fpc 2.4.2'),
    'pike': ('Pike', 'pike 7.8'),
    'pl'  : ('Perl', 'perl 5.12.3'),
    'py'  : ('Python', 'python 2.7.1'),
    'py3' : ('Python 3', 'python 3.2'),
    'rb'  : ('Ruby', 'ruby 1.8.7'),
    'tcl' : ('Tcl', 'tclsh 8.5'),
}

# Default time limit in miliseconds
DEFAULT_TIME_LIMIT = 1000

# Default memory limit in kbytes
DEFAULT_MEMORY_LIMIT = 16384

# Default source limit in bytes
DEFAULT_SOURCE_LIMIT = 50000

# Time before round starts when registration is available
REGISTRATION_START_TIME = datetime.timedelta(days=5)

# Time before round when registration closes
REGISTRATION_END_TIME = datetime.timedelta(minutes=10)


TICKET_TYPES = ['bug', 'feature']
TICKET_SEVERITIES = ['high', 'normal', 'critical', 'low']
TICKET_STATES = ['open', 'todo', 'in progress', 'on hold', 'completed', 'invalid', 'duplicate', 'wontfix']
TICKET_COMMENT_EDIT_TIMESTAMP = datetime.timedelta(minutes=150)
