#!/usr/bin/env python3

import os

def speak(words):
    vbs = createVbs(words)
    runVbs(vbs)

def createVbs(words):
    file = 'tmp.vbs'
    with open(file, 'w') as f:
        f.write('set speech = Wscript.CreateObject("SAPI.spVoice")' + os.linesep)
        f.write(('speech.speak "%s"' % words) + os.linesep)
    return file

def runVbs(vbs):
    system = os.name
    if system == 'posix':
        with open(vbs, 'r') as f:
            print('vbs content: %s' % f.read())
    elif system == 'nt':
        cmd = 'cscript %s' % vbs
        os.system(cmd)
