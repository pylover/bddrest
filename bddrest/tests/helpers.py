import contextlib
import io
import sys


@contextlib.contextmanager
def standard_files_mockup(stdin, argv=None):

    class StandardFile:
        encoding = 'UTF-8'
        def __init__(self, content=None):
            if content is None:
                self.buffer = io.BytesIO()
            else:
                self.buffer = io.BytesIO(content.encode() if isinstance(content, str) else content)

        def write(self, d):
            self.buffer.write(d.encode())

        def read(self, i=None):
            return self.buffer.read(i).decode()

        def seek(self, n):
            self.buffer.seek(0)

        def getvalue(self):
            return self.buffer.getvalue()

    stdinfile = StandardFile(stdin)
    stdoutfile = StandardFile()
    stderrfile = StandardFile()

    stdinbackup = sys.stdin
    stdoutbackup = sys.stdout
    stderrbackup = sys.stderr
    argvbackup = sys.argv

    sys.stdin = stdinfile
    sys.stdout = stdoutfile
    sys.stderr = stderrfile
    if argv:
        sys.argv = argv

    yield stdoutfile, stderrfile

    sys.stdin = stdinbackup
    sys.stdout = stdoutbackup
    sys.stderr = stderrbackup
    if argv:
        sys.argv = argvbackup

    stdoutfile.seek(0)
    stderrfile.seek(0)

