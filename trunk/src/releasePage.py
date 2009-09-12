import wx, wx.aui, wx.lib.hyperlink
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
    def __init__( self, parent, id, width, main ):

        wx.Panel.__init__( self, parent, id )

        self.main = main

        self.__uiInit( parent,id,width )

    def __uiInit( self, parent, id, width ):
        self.artistWidth = LEFT_WIDTH
        self.leftWidth = LEFT_WIDTH
        self.rightWidth = width - LEFT_WIDTH - 7
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
        
        self.artistList = wx.ListCtrl( leftPanel, wx.ID_ANY, wx.DefaultPosition,
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
        #self.placeholder = wx.StaticText( bottomPanel, wx.ID_ANY, 
            #"\n\n Placeholder \n\n" )
        self.link = wx.lib.hyperlink.HyperLinkCtrl( parent=bottomPanel )
        self.whatLink = wx.lib.hyperlink.HyperLinkCtrl( parent=bottomPanel )

        bottomBox = wx.BoxSizer( wx.VERTICAL )
        #bottomBox.Add( self.placeholder, 1, wx.EXPAND )
        bottomBox.Add( self.link, 1, wx.EXPAND )
        bottomBox.Add( self.whatLink, 1, wx.EXPAND )
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

    def OnSearch( self, item=None ):
        self.RecreateArtists()

    def OnSearchMenu( self, item ):
        x = 1

    def OnItemSelected( self, event ):
        self.RecreateReleases( event )

    def RecreateArtists( self, event=None ):
        self.artistList.DeleteAllColumns()
        self.artistList.DeleteAllItems()
        self.artistList.InsertColumn( 0, "Artist" )
        self.artistList.SetColumnWidth( 0, self.artistWidth )

        index = 0
        for junk,artist in sorted( self.main.library.artists.items() ):
            if( artist['name'].lower().find( self.filter.GetValue().lower() ) > -1 ):
                self.artistList.InsertStringItem( index, artist['name'] )
                index+=1

    def RecreateReleases( self, event=None ):
        self.releases.DeleteAllColumns()
        self.releases.DeleteAllItems()
        self.releases.InsertColumn( 0, "Release" )
        self.releases.InsertColumn( 1, "Have" )
        self.releases.InsertColumn( 2, "Date" )
        self.releases.SetColumnWidth( 0, self.rightWidth * .70 )
        self.releases.SetColumnWidth( 1, self.rightWidth * .09 )
        self.releases.SetColumnWidth( 2, self.rightWidth * .21 )

        if event:
            index = 0
            for junk,artist in self.main.library.artists.items() :
                if( artist['name'] == event.GetItem().GetText() ) :
                    self.link.SetURL( str(artist['aid']) )
                    self.link.SetLabel( artist['name'] )
                    self.link.SetToolTipString( str(artist['aid']) )
                    self.link.SetVisited(False)
                    whatURL = "http://what.cd/artist.php?name=" + str(artist['name'])
                    self.whatLink.SetURL( str(whatURL) )
                    self.whatLink.SetLabel('Search on What.CD' )
                    self.whatLink.SetToolTipString( str(whatURL) )
                    self.whatLink.SetVisited(False)
                    if( artist['aid'] == 0 ):
                        # queue a high priority lookup of this artist
                        self.main.library.lookupReleases( junk, 6 )
                    for rel in artist['releases']:
                        self.releases.InsertStringItem( index, rel.title )
                        self.releases.SetStringItem( index, 1, rel.have and "Y" or "N" )
                        self.releases.SetStringItem( index, 2, rel.date )
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
