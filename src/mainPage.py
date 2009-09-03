import wx

RELEASE_ARTIST_WIDTH=150
RELEASE_RELEASE_WIDTH=100
RELEASE_DATE_WIDTH=100
RELEASE_FONT_SIZE=8

RELATED_ARTIST_WIDTH=150

class MainPage( wx.Panel ):
    def __init__( self, parent, id, width ):
        wx.Panel.__init__( self, parent, id )
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        st = wx.StaticText( self, wx.ID_ANY, "\nNew Releases:" )
        self.sizer.Add( st )
        self.CreateNewReleases( width )
        self.sizer.AddSpacer( 40 )
        st = wx.StaticText( self, wx.ID_ANY, "Recommended Artists:" )
        self.sizer.Add( st )
        self.CreateTopRelated( width )
        self.SetSizer( self.sizer )
        self.SetAutoLayout( True )
        self.sizer.Fit( self )
        self.Show( True )

    def CreateTopRelated( self, width ):
        relatedSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.relatedList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.LC_REPORT )
        self.PopulateRelated( self.relatedList, width )
        relatedSizer.Add( self.relatedList, 1, wx.EXPAND )
        self.sizer.Add( relatedSizer, 1, wx.EXPAND )
        
        

    def PopulateRelated( self, list, width ):
        """
        list.InsertColumn( 0, "Artist" )
        items = musicdata.items()
        for key, data in items:
            if key % 10 == 0:
                index = list.InsertStringItem( key, data[0] )
                self.FormatItem( index, list )

        list.SetColumnWidth( 0, width )
        """

    def CreateNewReleases( self, width ):
        releaseSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.newReleases = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize,  wx.LC_REPORT )
        self.PopulateReleases( self.newReleases, width )
        releaseSizer.Add( self.newReleases, 1, wx.EXPAND )
        self.sizer.Add( releaseSizer, 1, wx.EXPAND )
       
    def PopulateReleases( self, releases, width ):
        """
        releases.InsertColumn( 0, "Artist" )
        releases.InsertColumn( 1, "Release" )
        releases.InsertColumn( 2, "Date" )

        items = musicdata.items()
        for key, data in items:
            index = releases.InsertStringItem( key, data[0] )
            releases.SetStringItem( index, 1, data[1] )
            releases.SetStringItem( index, 2, data[2] )
            if key % 2 == 0:
                self.FormatItem( index, releases, fg=wx.BLUE,
                        bg=wx.WHITE )
            else:
                self.FormatItem( index, releases )

        # Size the columns
        releases.SetColumnWidth( 0, width * .4 )
        releases.SetColumnWidth( 1, width * .4 )
        releases.SetColumnWidth( 2, width * .2 )
        """

    def FormatItem( self, itemNum, list, bg=wx.WHITE, fg=wx.BLACK, 
                    size=RELEASE_FONT_SIZE,family=wx.FONTFAMILY_DEFAULT, 
                    weight=wx.FONTWEIGHT_NORMAL ):
        item =  list.GetItem( itemNum )
        font = wx.Font( size, family, wx.FONTSTYLE_NORMAL, weight )
        item.SetFont( font )
        item.SetBackgroundColour( bg )
        item.SetTextColour( fg )
        list.SetItem( item )

    def OnResize( self, event ):
        if self.GetAutoLayout():
            self.Layout()
