python -c 'import os;os.system("./input "+64*"A "+"\x00 "+"\x20\x0a\x0d "+(100-67)*"A ")'

export var=$(python -c 'print 64*"A "+"\x00 "+"\x20\x0a\x0d "+(100-67)*"A "')