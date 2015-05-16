# nanoblog.py

import os
import sys
import markdown

__usage__ = """\
nanoblog.py command [args...]

Commands:
    ...

"""

if __name__ == "__main__":

    if not sys.argv[1:]:
        print >> sys.stderr, __usage__
        sys.exit(1)

    cmd, rest = sys.argv[1], sys.argv[2:]
    print (cmd, rest)

