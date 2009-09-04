import wx
import utils
import os

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

BORDER_WIDTH = 20

ID_OK = 100
ID_CANCEL = 101
ID_DIR = 102

class OptionWindow(wx.Frame):

    def __init__(self, parent, id, title, main):
        wx.Frame.__init__(self, parent, id, title,
                size=(FRAME_WIDTH, FRAME_HEIGHT))
       
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        nb = wx.Notebook( self, wx.ID_ANY, style=wx.BK_LEFT|wx.BORDER_DOUBLE )

        config = utils.GetConfig()

        self.MainWindow = main

        # Make the main configuration tab
        main = wx.Panel( nb, wx.ID_ANY )

        mainBox = wx.BoxSizer( wx.VERTICAL )
        mainBox.AddSpacer( BORDER_WIDTH )

        directoryBox  = wx.BoxSizer( wx.HORIZONTAL )
        st = wx.StaticText( main, wx.ID_ANY, "Music Directory: ")
        self.directoryInput = wx.TextCtrl( main, wx.ID_ANY )
        val = config.Read('MusicDirectory')
        if val:
            self.directoryInput.SetValue(val)
        
        dirChooser = wx.Button( main, ID_DIR, "..." )
        wx.EVT_BUTTON( self, ID_DIR, self.OnChooser )
        directoryBox.AddSpacer( BORDER_WIDTH )
        directoryBox.Add( st, 0, wx.EXPAND )
        directoryBox.Add( self.directoryInput, 1, wx.EXPAND )
        directoryBox.AddSpacer( BORDER_WIDTH )
        directoryBox.Add( dirChooser, 0, wx.FIXED_MINSIZE )
        mainBox.Add( directoryBox, 0, wx.EXPAND )
        
        main.SetSizer( mainBox )
        main.SetAutoLayout( True )
        mainBox.Fit( main )
        main.Show( True )

        
        # Add the pages
        nb.AddPage( main, "Main" )


        # Make the Ok / Cancel buttons
        buttonBox = wx.BoxSizer( wx.HORIZONTAL )
        ok = wx.Button( self, ID_OK, "&Ok" )
        cancel = wx.Button( self, ID_CANCEL, "&Cancel" )
        wx.EVT_BUTTON( self, ID_OK, self.OnOk )
        wx.EVT_BUTTON( self, ID_CANCEL, self.OnCancel )
        buttonBox.Add( ok, 1, wx.ALIGN_RIGHT )
        buttonBox.AddSpacer( 20 )
        buttonBox.Add( cancel, 1, wx.ALIGN_RIGHT )
        buttonBox.AddSpacer( BORDER_WIDTH )

        # Add the notebook and buttons to the main sizer
        self.sizer.Add( nb, 1, wx.EXPAND )
        self.sizer.AddSpacer( BORDER_WIDTH / 2 )
        self.sizer.Add( buttonBox, 0, wx.ALIGN_RIGHT )
        self.sizer.AddSpacer( BORDER_WIDTH / 2 )

        self.SetSizer( self.sizer )
        self.SetAutoLayout( True )

    def OnChooser( self, event ):
        val = self.directoryInput.GetValue()
        if val:
            userPath = val
        else:
            userPath = os.curdir
        dialog = wx.DirDialog(None,\
                              "Please choose your music directory:",\
                              style=1,
                              defaultPath=userPath,
                              pos = (10,10))
        if dialog.ShowModal() == wx.ID_OK:
            self.directoryInput.SetValue(dialog.GetPath())

    def OnOk( self, event ):
        config = utils.GetConfig()
        config.Write('MusicDirectory', self.directoryInput.GetValue())

        config.Flush()
        self.MainWindow.releaseP.musicDir = self.directoryInput.GetValue()
        self.MainWindow.releaseP.RecreateArtists()
        self.Close()

    def OnCancel( self, event ):
        self.Close()

