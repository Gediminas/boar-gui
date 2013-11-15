import wx
import os
import time
import datetime
from defs import *

def Open_Log(frame):
    if not (frame.mod == 'log'):
        frame.szrTop.DeleteWindows()
        frame.lstData = wx.ListCtrl(parent=frame.pnlTop, id=-1, style=wx.LC_REPORT)
        frame.txtData = wx.TextCtrl(parent=frame.pnlTop, id=-1, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP)
        frame.szrTop.AddWindow(frame.lstData, 3, wx.ALL | wx.EXPAND)
        frame.szrTop.AddWindow(frame.txtData, 1, wx.ALL | wx.EXPAND)
        frame.szrTop.Layout()
        
        frame.lstData.InsertColumn(0, "#",       wx.LIST_FORMAT_LEFT,  50)
        frame.lstData.InsertColumn(1, "Date",    wx.LIST_FORMAT_LEFT, 150)
        frame.lstData.InsertColumn(2, "Session", wx.LIST_FORMAT_LEFT, 150)
        frame.lstData.InsertColumn(3, "Comment", wx.LIST_FORMAT_LEFT, 300)
        
        frame.lstData.Bind(wx.EVT_CONTEXT_MENU, OnShowPopup)
    else:
        frame.mod = 'log'
    
    frame.txtConsole.SetValue('')
    pass
    
def OnData_Log(self, line, mode, globals, var):
    if (mode == EMode_Starting):
        self.txtConsole.WriteText(line)
        self.txtConsole.WriteText('connecting and executing...\n')
        var['cnt'] = 0
        var['cmm'] = 0
        var['buf'] = ''
        return EMode_Data
    
    elif (mode == EMode_Data):
        var['cnt'] += 1

        if (var['cnt'] == 1 or var['cnt'] == 3):    #-------------------------------------------------------
            pass
        elif (var['cnt'] == 2):                     #r9 | Session1 | Sat Nov 09 02:01:06 2013 | 1 log line
            ar = line.split(' | ')
            if (len(ar) == 4):
                date = time.strftime(u"%Y-%m-%d  %H:%M:%S", time.strptime(ar[2]))
                cmnt = ar[3].strip()
                cmnt = cmnt.replace(' log lines', '')
                cmnt = cmnt.replace(' log line',  '')
                var['cmm'] = int(cmnt)
                var['buf'] = ''
                snid = ar[0][1:]
                index = self.lstData.InsertStringItem(self.lstData.GetItemCount(), "")
                self.lstData.SetStringItem(index, 0, snid)
                self.lstData.SetStringItem(index, 1, date)
                self.lstData.SetStringItem(index, 2, ar[1])
                if (snid == globals['snapshot']):
                    self.lstData.SetStringItem(index, 0, '[%s]'%snid)
                    
            else:
                print 'ERROR: ', line
                return EMode_Finish
        elif (var['cmm'] == 0):                     # user comments ended
            var['cnt'] = 1
        else:                                       # user comments
            var['cmm'] -= 1
            var['buf'] += line.strip()
            index = self.lstData.GetItemCount()-1
            text  = line.strip()
            self.lstData.SetStringItem(index, 3, var['buf'])

    else: #(EMode_Finish == mode or EMode_Extra == mode)
        self.txtConsole.WriteText(line)
        
    return mode

def OnShowPopup(event):
    self.txtConsole.WriteText('popup\n')
    pass