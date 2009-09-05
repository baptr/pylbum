import wx

EVT_STATUS_UPDATE_ID = wx.NewId()

def EVT_STATUS_UPDATE(win, func) :
    win.Connect( -1, -1, EVT_STATUS_UPDATE_ID, func )

class StatusUpdate(wx.PyEvent):
    def __init__(self,msg):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_STATUS_UPDATE_ID)
        self.msg = msg


