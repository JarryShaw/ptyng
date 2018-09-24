# import io
# import os
# import pty
# import subprocess

# class IOBase(io.IOBase):

#     def fileno(self):
#         return self._fileno

#     def __init__(self, fileno, *args, **kwargs):
#         self._fileno = fileno
#         super().__init__(*args, **kwargs)

# # parent, child = pty.openpty()
# # print('ptyed!') ###
# # # subprocess.run(['brew', 'info'], stdout=IOBase(child))
# # # subprocess.run(['brew', 'info'], stdout=IOBase(child))
# # # subprocess.run(['curl https://httpbin.org/ip; sleep 5'], shell=True, stdout=IOBase(child), stderr=subprocess.STDOUT, timeout=60)
# # subprocess.run(['brew', 'info', 'python'], stdout=IOBase(child), stderr=subprocess.STDOUT, timeout=60)
# # print('subprocessed!') ###
# # print(os.read(parent, 1024))



# pid, fd = pty.fork()
# if pid == 0:
#     print(fd)
#     subprocess.run(['npm', 'help'])
# else:
#     print(fd)
#     print(os.read(fd, 1024))
#     print(os.wait4(pid, os.WEXITED))


import argparse
import os
import pty
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='append', action='store_true')
parser.add_argument('-p', dest='use_python', action='store_true')
parser.add_argument('filename', nargs='?', default='typescript')
options = parser.parse_args()

shell = sys.executable if options.use_python else os.environ.get('SHELL', 'sh')
filename = options.filename
mode = 'ab' if options.append else 'wb'

with open(filename, mode) as script:
    def read(fd):
        data = os.read(fd, 1024)
        script.write(data)
        return data

    print('Script started, file is', filename)
    script.write(('Script started on %s\n' % time.asctime()).encode())

    # pty.spawn(shell, read)
    pty.spawn(['brew', 'info', 'python'], read)

    script.write(('Script done on %s\n' % time.asctime()).encode())
    print('Script done, file is', filename)
