import wx
from datetime import datetime, timedelta

RELEASE_ARTIST_WIDTH=150
RELEASE_RELEASE_WIDTH=100
RELEASE_DATE_WIDTH=100
RELEASE_FONT_SIZE=8

RELATED_ARTIST_WIDTH=150

class MainPage( wx.Panel ):
    def __init__( self, parent, id, width, main ):
        wx.Panel.__init__( self, parent, id )
        self.library = main.library;
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
        self.PopulateReleases()
        releaseSizer.Add( self.newReleases, 1, wx.EXPAND )
        self.sizer.Add( releaseSizer, 1, wx.EXPAND )

        self.newReleases.InsertColumn( 0, "Artist" )
        self.newReleases.InsertColumn( 1, "Release" )
        self.newReleases.InsertColumn( 2, "Date" )
        # Size the columns
        self.newReleases.SetColumnWidth( 0, width * .4 )
        self.newReleases.SetColumnWidth( 1, width * .4 )
        self.newReleases.SetColumnWidth( 2, width * .2 )

      
    def PopulateReleases( self ):
        """List recent releases across all artists in the library """
        releases = self.newReleases
        releases.DeleteAllItems()

        print "Updating new releases"

        items = sorted( self.library.artists.items() )
        targetdate = datetime.today() - timedelta(30);
        key = 1
        for junk, artist in items:
            for rel in artist['releases']:
                if rel.have:
                    continue
                if rel.date != 'Unknown':
                    try:
                        relDate = datetime.strptime(rel.date,"%Y-%m-%d")
                    except ValueError:
                        continue
                    if relDate < targetdate:
                        continue
                    index = releases.Append(
                            (artist['name'], rel.title, rel.date) )
                    key+=1
                    if key % 2:
                        self.FormatItem( index, releases, bg=wx.LIGHT_GREY )
                    else:
                        self.FormatItem( index, releases, bg=wx.WHITE )

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
        PopulateReleases( self.newReleases )
