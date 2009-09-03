import wx
import utils

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

BORDER_WIDTH = 20

ID_OK = 100
ID_CANCEL = 101

class OptionWindow(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                size=(FRAME_WIDTH, FRAME_HEIGHT))
       
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        nb = wx.Notebook( self, wx.ID_ANY, style=wx.BK_LEFT|wx.BORDER_DOUBLE )

        config = utils.GetConfig()

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
        directoryBox.AddSpacer( BORDER_WIDTH )
        directoryBox.Add( st, 0, wx.EXPAND )
        directoryBox.Add( self.directoryInput, 1, wx.EXPAND )
        directoryBox.AddSpacer( BORDER_WIDTH )
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

    def OnOk( self, event ):
        config = utils.GetConfig()
        config.Write('MusicDirectory', self.directoryInput.GetValue())

        config.Flush()
        self.Close()

    def OnCancel( self, event ):
        self.Close()

