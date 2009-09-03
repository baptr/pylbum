import wx, wx.aui
import os
import utils

RELEASE_ARTIST_WIDTH=150
RELEASE_RELEASE_WIDTH=100
RELEASE_DATE_WIDTH=100
RELEASE_FONT_SIZE=8

RELATED_ARTIST_WIDTH=150

ALLOW_AUI_FLOATING = False
LEFT_WIDTH = 160

class ReleasePage( wx.Panel ):
    def __init__( self, parent, id, width ):

        wx.Panel.__init__( self, parent, id )

        self.artistWidth = LEFT_WIDTH
        self.leftWidth = LEFT_WIDTH
        self.rightWidth = width - LEFT_WIDTH
        self.sizer = wx.BoxSizer( wx.VERTICAL )

        self.lrSplitter = wx.SplitterWindow( self, wx.ID_ANY,
                style = wx.SP_LIVE_UPDATE, size=(-1, 480))
        self.lrSplitter.SetMinimumPaneSize( 160 )
        self.lrSplitter.Bind( wx.EVT_SPLITTER_SASH_POS_CHANGING,
                self.OnVertSash )
        self.lrSplitter.Bind( wx.EVT_SPLITTER_SASH_POS_CHANGED,
                self.OnVertSashEnd )
        self.tbSplitter = wx.SplitterWindow( self.lrSplitter, wx.ID_ANY,
                style = wx.SP_LIVE_UPDATE, size=(-1, 480))
        self.tbSplitter.SetMinimumPaneSize( 60 )

        # Create the  left panel with an artist list and a search box
        leftPanel = wx.Panel( self.lrSplitter, wx.ID_ANY,
                style = wx.CLIP_CHILDREN )
        self.searchItems = {}
        
        self.artistList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition,
                                       wx.DefaultSize,  
                                       wx.LC_REPORT|wx.LC_SINGLE_SEL )
        self.artistList.Bind( wx.EVT_LIST_COL_END_DRAG, self.OnArtistColDrag,
                self.artistList )


        self.filter = wx.SearchCtrl(leftPanel, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateArtists)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancelBtn)
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Artist")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Year")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)

        self.RecreateArtists()
        self.artistList.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

        # Create the top pane with the list of releases
        topPanel = wx.Panel( self.tbSplitter, style=wx.CLIP_CHILDREN )
        self.releases = wx.ListCtrl( topPanel, wx.ID_ANY, 
                style=wx.LC_REPORT|wx.LC_SINGLE_SEL )
        self.RecreateReleases()

        topBox = wx.BoxSizer( wx.VERTICAL )
        topBox.Add( self.releases, 1, wx.EXPAND )
        topPanel.SetSizer( topBox )
        topPanel.SetAutoLayout( True )

        # Create static text placeholder
        bottomPanel = wx.Panel( self.tbSplitter, style=wx.CLIP_CHILDREN )
        self.placeholder = wx.StaticText( bottomPanel, wx.ID_ANY, 
            "\n\n Placeholder \n\n" )

        bottomBox = wx.BoxSizer( wx.VERTICAL )
        bottomBox.Add( self.placeholder, 1, wx.EXPAND )
        bottomPanel.SetSizer( bottomBox )
        bottomPanel.SetAutoLayout( True )

        # Create top/bottom splitter

        self.tbSplitter.SplitHorizontally( topPanel, bottomPanel )

        # Create the left pane
        leftBox = wx.BoxSizer( wx.VERTICAL )
        leftBox.Add( self.artistList, 1, wx.EXPAND )
        leftBox.Add( wx.StaticText( leftPanel, label="Filter artists:" ), 0, 
                wx.TOP|wx.LEFT, 5 )
        leftBox.Add( self.filter, 0, wx.EXPAND|wx.ALL, 5 )
        leftPanel.SetSizer( leftBox )
        leftPanel.SetAutoLayout( True )

        # Split left / right
        self.lrSplitter.SplitVertically( leftPanel, self.tbSplitter )

        self.sizer.Add( self.lrSplitter, 1, wx.EXPAND )
        self.SetSizer( self.sizer )
        self.SetAutoLayout( True )
        self.sizer.Fit( self )
        self.Show( True )

    def OnVertSash( self, event ):
        if self.artistList.GetColumnWidth( 0 ) < event.GetSashPosition():
            self.artistList.SetColumnWidth( 0, event.GetSashPosition() )
            self.artistWidth = event.GetSashPosition()

    def OnVertSashEnd( self, event ):
        self.Refresh()

    def OnSearchCancelBtn( self, event ):
        self.filter.SetValue('')
        self.OnSearch()
        self.RecreateReleases()

    def OnSearch( self ):
        self.RecreateArtists()

    def OnSearchMenu( self ):
        x = 1

    def OnItemSelected( self, event ):
        self.RecreateReleases()

    def RecreateArtists( self, event=None ):
        self.artistList.DeleteAllColumns()
        self.artistList.DeleteAllItems()
        self.artistList.InsertColumn( 0, "Artist" )
        self.artistList.SetColumnWidth( 0, self.artistWidth )

        config = utils.GetConfig()
        artists = os.listdir( config.Read('MusicDirectory' ) )

        index = 0
        for name in artists:
            if (( self.artistList.FindItem( -1, name, True ) == -1 ) and 
                ( name.lower().find( self.filter.GetValue().lower()) > -1 ) and
                ( os.path.isdir(os.path.join(config.Read('MusicDirectory'), 
                    name)))):
                self.artistList.InsertStringItem( index, name )
                index += 1

    def RecreateReleases( self ):
        self.releases.DeleteAllColumns()
        self.releases.DeleteAllItems()
        self.releases.InsertColumn( 0, "Release" )
        self.releases.InsertColumn( 1, "Date" )
        self.releases.SetColumnWidth( 0, self.rightWidth * .75 )
        self.releases.SetColumnWidth( 1, self.rightWidth * .25 )


        index = 0
        config = utils.GetConfig()
        artists = os.listdir(config.Read('MusicDirectory'))
        for name in artists:
            artistDir = os.path.join(config.Read('MusicDirectory'), name)
            if os.path.isdir( artistDir ):
                albums = os.listdir( os.path.join(
                    config.Read('MusicDirectory'), name))
                for release in albums:
                    try:
                        releaseDir = os.path.join(artistDir, release)
                    except UnicodeDecodeError:
                        print "Bad filename: " + release
                        continue
                    if os.path.isdir(releaseDir):
                        listItem = self.artistList.GetItem( 
                                self.artistList.GetFirstSelected(),
                                0 )
                        if( listItem.GetText() == name):
                            self.releases.InsertStringItem( index, release )
                            self.releases.SetStringItem( index, 1,
                                    '12/12/2009' )
                            index += 1



    def InitSize( self ):
        self.lrSplitter.SetSashPosition( LEFT_WIDTH )
        self.tbSplitter.SetSashPosition( -100 )
        self.artistList.SetColumnWidth( 0, LEFT_WIDTH )

    def OnArtistColDrag( self, event ):
        self.artistWidth = event.GetPosition()[0]

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
