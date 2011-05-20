import datetime

COMPILERS = {
    'adb' : ('Ada', 'gnat 4.5.1'),
    'bas' : ('Basic', 'fbc ...'),
    'c'   : ('C', 'gcc 4.5.1'),
    'cpp' : ('C++', 'g++ 4.5.1'),
    'cs'  : ('C#', 'gmcs ...'),
    'd'   : ('D', 'dmd ...'),
    'lua' : ('Lua', 'luac ... '),
    'ml'  : ('Ocaml', 'ocaml ...'),
    'pas' : ('Pascal', 'fpc ...'),
    'pike': ('Pike', 'pike ...'),
    'pl'  : ('Perl', 'perl ...'),
    'py'  : ('Python', 'python 2.7'),
    'py3' : ('Python 3', 'python 3.1'),
    'rb'  : ('Ruby', 'ruby 1.8.7'),
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