import wx
import os
import command_fnc
from defs import *

def Open_Commit(frame):
    if not (frame.mod == 'commit'):
        frame.szrTop.DeleteWindows()
        frame.txtData = wx.TextCtrl(parent=frame.pnlTop, id=-1, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP)
        frame.szrTop.AddWindow(frame.txtData, 1, wx.ALL | wx.EXPAND)
        frame.szrTop.Layout()
    else:
        frame.mod = 'commit'
    
    frame.txtData.SetValue("<executing>")
    frame.txtConsole.SetValue('')
    pass
    
def OnData_Commit(self, line, mode, globals, var):
    if (EMode_Starting == mode):
        command_fnc.DynamicOutput(self.txtConsole, line, var)
        command_fnc.DynamicOutput(self.txtConsole, 'connecting...\n', var)
        return EMode_Execute
    
    elif (EMode_Execute == mode):
        full_line = command_fnc.DynamicOutput(self.txtConsole, line, var)
        if full_line == 'Calculating changes... done\n':
            return EMode_Data

    elif (EMode_Data == mode):
        self.txtData.WriteText(line)
        
    else: #(EMode_Finish == mode or EMode_Extra == mode)
        self.txtData.Remove(self.txtData.GetInsertionPoint(), self.txtData.GetLastPosition())
        self.txtConsole.WriteText(line)
        
    return mode
