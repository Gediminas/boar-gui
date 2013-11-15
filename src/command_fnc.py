import wx
import os
import sys
import threading
import subprocess
import time
import shutil
from defs import *


class CReader:
    def __init__(self, stdout): self.stdout = stdout
    def read(self):             return self.stdout.read(1)



class CRedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl
    def write(self,string):
        self.out.WriteText(string)
def RedirectText(object):
        redir = CRedirectText(object)
        sys.stdout=redir
        sys.stderr=redir



class CThreadCommand(threading.Thread):
	def __init__(self, cmd, bConsole, fnc_on_data_line):
		threading.Thread.__init__(self)
		self.cmd         = cmd
		self.fnc_on_data_line = fnc_on_data_line
		self.bConsole    = bConsole
	def run(self):
		data = Command(self.cmd, self.bConsole, self.fnc_on_data_line)
def ThreadCommand(cmd, bConsole, fnc_on_data_line):
    #print '---------------------------------'
    #print '{:10}{}'.format('[THREAD]:', cmd)

    t = CThreadCommand(cmd, bConsole, fnc_on_data_line)
    t.daemon = True # thread dies with the program
    t.start()


    
def Command(cmd, bConsole, on_data_line):

    #cmd = 'cmd /c \"' + cmd + '\"' #2>&1 >f:\\test\\Sesija1\\_out.txt'
    
    mode = on_data_line(cmd + "\n", EMode_Starting)
    process = subprocess.Popen( (cmd),
                                 stdout  = subprocess.PIPE,
                                 stderr  = subprocess.PIPE,
                                 bufsize = 1,
                                 shell   = not bConsole)
    
    if mode == EMode_Execute:
        buffer = ''
        line   = ''
        reader = CReader(process.stdout)

        for c in iter(reader.read, u''):
            buffer = buffer + c;
            
            if  ( c == '\n' or
                  c == '\r' or
                 (c == '.' and 2 < len(buffer) and buffer[-2] == '.' and buffer[-3] == '.') ):
                pass #flush
            else:
                continue #collect

            #line = line + buffer
            #if not on_data_line(line, mode) == EMode_Execute:
            if not on_data_line(buffer, mode) == EMode_Execute:
               break
            #if c == '\n' or c == '\r':
            #    line = ''

            buffer = ''
        
    for buffer in iter(process.stdout.readline, u''):
        if (mode == EMode_Finish or mode == EMode_Extra):
            mode = on_data_line(buffer, EMode_Extra)
            continue;
        if (buffer.find('Finished in ') == 0):
            mode = on_data_line(buffer, EMode_Finish)
        else:
            mode = on_data_line(buffer, EMode_Data)

    for error in iter(process.stderr.readline, u''):
		print 'ERROR:', error

def DynamicOutput(txtCtrl, line, var):
    if not 'dyn_ret' in var:
        var['dyn_pos'] = txtCtrl.GetLastPosition()
        var['dyn_ret'] = False
        var['dyn_buf'] = ''
        
    if (var['dyn_ret'] == True and not line == '\n'):
        txtCtrl.Remove(var['dyn_pos'], txtCtrl.GetLastPosition());
        var['dyn_buf'] = ''

    if var['dyn_ret'] == False or not line == '\n':
        txtCtrl.WriteText(line)
        var['dyn_buf'] += line

    if line[-1] == '\n':
        var['dyn_pos'] = txtCtrl.GetLastPosition()
        var['dyn_ret'] = False
        ret = var['dyn_buf']
        var['dyn_buf'] = ''
        return ret
    elif line[-1] == '\r':
        var['dyn_ret'] = True

    return ''