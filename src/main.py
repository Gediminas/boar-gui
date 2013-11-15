import wx
import os
import sys
import threading
import subprocess
import time
import shutil

from defs import *
import command_fnc
import mod_cmd_info
import mod_cmd_log
import mod_cmd_status
import mod_cmd_commit

globals = {
'session':'',
'snapshot':'',
}

[
 wxID_frmMain,
 wxID_frmMain_pnlMain,
 wxID_frmMain_txtHeader,
 wxID_frmMain_txtConsole,
 wxID_frmMain_btnInfo,
 wxID_frmMain_btnLog,
 wxID_frmMain_btnStatus,
 wxID_frmMain_btnCommit,

 wxID_frmMain_pnlData,
 wxID_frmMain_txtData,
]  = [wx.NewId() for _init_ctrls in range(10)]

class CMainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, id=wxID_frmMain, parent=None, pos=wx.Point(0, 0), size=wx.Size(1000, 800), style=wx.DEFAULT_FRAME_STYLE, title='boar-gui')

        self.Splitter = wx.SplitterWindow(self, -1)
        
        # TOP
        self.pnlTop = wx.Panel(id=-1, parent=self.Splitter)
        self.szrTop = wx.BoxSizer(orient=wx.VERTICAL)
        self.pnlTop.SetSizer(self.szrTop)
        self.mod = ''

        # BOT
        self.pnlBot     = wx.Panel(id=-1, parent=self.Splitter)
        self.txtConsole = wx.TextCtrl(parent=self.pnlBot, id=wxID_frmMain_txtConsole, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP)

        # Buttons
        self.ckbConsole  = wx.CheckBox(  id=-1,                      parent=self.pnlBot, label='(console)    ')
        self.btnInfo     = wx.Button(    id=wxID_frmMain_btnInfo,    parent=self.pnlBot, label='Info')
        self.btnLog      = wx.Button(    id=wxID_frmMain_btnLog,     parent=self.pnlBot, label='Log')
        self.btnStatus   = wx.Button(    id=wxID_frmMain_btnStatus,  parent=self.pnlBot, label='Status')
        self.btnCommit   = wx.Button(    id=wxID_frmMain_btnCommit,  parent=self.pnlBot, label='Commit')
        
        self.szButtons = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.szButtons.Add(self.ckbConsole)
        self.szButtons.Add(self.btnInfo)
        self.szButtons.Add(self.btnLog)
        self.szButtons.Add(self.btnStatus)
        self.szButtons.Add(self.btnCommit)
        
        self.szrBot = wx.BoxSizer(orient=wx.VERTICAL)
        self.szrBot.AddWindow(self.szButtons,  0, wx.ALL | wx.EXPAND)
        self.szrBot.AddWindow(self.txtConsole, 1, wx.ALL | wx.EXPAND)
        self.pnlBot.SetSizer(self.szrBot)

        # ALL
        self.Splitter.SplitHorizontally(self.pnlTop , self.pnlBot, 600)
        self.Layout()
        
        # Binds
        self.Bind(wx.EVT_BUTTON, self.OnBtnInfo,   self.btnInfo)
        self.Bind(wx.EVT_BUTTON, self.OnBtnLog,    self.btnLog)
        self.Bind(wx.EVT_BUTTON, self.OnBtnStatus, self.btnStatus)
        self.Bind(wx.EVT_BUTTON, self.OnBtnCommit, self.btnCommit)



    def OnBtnInfo(self, event):
        mod_cmd_info.Open_Info(self)
        
        command_fnc.Command('boar info', self.ckbConsole.IsChecked(), self.OnData_Info)
        command_fnc.Command('boar --version', self.ckbConsole.IsChecked(), self.OnData_Info)
        pass
        
    def OnBtnLog(self, event):
        mod_cmd_log.Open_Log(self)
        command_fnc.ThreadCommand('boar log', self.ckbConsole.IsChecked(), self.OnData_Log)
        pass
        
    def OnBtnStatus(self, event):
        mod_cmd_status.Open_Status(self)
        command_fnc.ThreadCommand('boar status', self.ckbConsole.IsChecked(), self.OnData_Status)
        pass
        
    def OnBtnCommit(self, event):
        mod_cmd_commit.Open_Commit(self)
        command_fnc.ThreadCommand('boar ci --message=\"boar-gui\"', self.ckbConsole.IsChecked(), self.OnData_Commit)
        pass


    def OnData_Info(self, line, mode, var={}):
        global globals
        return mod_cmd_info.OnData_Info(self, line, mode, globals, var)

    def OnData_Log(self, line, mode, var={}):
        global globals
        return mod_cmd_log.OnData_Log(self, line, mode, globals, var)

    def OnData_Status(self, line, mode, var={}):
        global globals
        return mod_cmd_status.OnData_Status(self, line, mode, globals, var)

    def OnData_Commit(self, line, mode, var={}):
        global globals
        return mod_cmd_commit.OnData_Commit(self, line, mode, globals, var)

if __name__ == '__main__':
    app = wx.PySimpleApp() #redirect=False
    frame = CMainFrame()
    frame.Show()
    app.SetTopWindow(frame)

    command_fnc.RedirectText(frame.txtConsole)

    frame.OnBtnInfo(None)
        
    app.MainLoop()
