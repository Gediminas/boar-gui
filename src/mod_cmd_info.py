import wx
import os
from defs import *

def Open_Info(frame):
    if not (frame.mod == 'info'):
        frame.szrTop.DeleteWindows()
        frame.txtData = wx.TextCtrl(parent=frame.pnlTop, id=-1, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP)
        frame.szrTop.AddWindow(frame.txtData, 1, wx.ALL | wx.EXPAND)
        frame.szrTop.Layout()
    else:
        frame.mod = 'info'
    
    frame.txtData.SetValue("<executing>")
    frame.txtConsole.SetValue('')
    pass
    
def OnData_Info(self, line, mode, globals, var):
    if (mode == EMode_Starting):
        var['cmd'] = line.strip()
        self.txtConsole.WriteText(line)
        var['cnt'] = 0
        session = ''
        return EMode_Data
    
    elif (mode == EMode_Data):
        var['cnt'] += 1
        
        if (var['cnt'] == 2):
            if (line.find('Session / Path: ') == 0):
                globals['session'] = line.strip()[16:]
        elif (var['cnt'] == 3):
            if (line.find('Snapshot id: ') == 0):
                globals['snapshot'] = line.strip()[13:]
                
        ar = line.split(': ')
        if var['cmd'] == 'boar info' and len(ar) > 1:
            if ar[0] == 'Repository':
                #ar[1].split('/')
                self.txtData.WriteText((ar[0]+':').ljust(20) + ar[1])
            else:
                self.txtData.WriteText((ar[0]+':').ljust(20) + ar[1])
        else:
            self.txtData.WriteText(line)

    else: #(EMode_Finish == mode or EMode_Extra == mode)
        self.txtData.Remove(self.txtData.GetInsertionPoint(), self.txtData.GetLastPosition())
        if (var['cmd'] == 'boar info'):
            self.txtData.WriteText('current folder:'.ljust(20) + os.getcwd() + '\n')
            self.txtData.WriteText('\n-------------------------\n')
        self.txtConsole.WriteText(line)

    return mode
    pass