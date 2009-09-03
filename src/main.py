#!/usr/bin/python

import wx
import mainPage
import releasePage
import lyricPage
import similarPage
import optionWindow

# File menu 11**
ID_QUIT = 1101

# View menu 12**
ID_PREFERENCES = 1201

# Help menu 13**
ID_ABOUT = 1301

FRAME_WIDTH=640
FRAME_HEIGHT=480

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, 
                size=(FRAME_WIDTH, FRAME_HEIGHT))
        self.CreateStatusBar()
        self.CreateMenu()
        self.CreateNotebook()


    def CreateMenu( self ):
        """ Create the menu items """
        # File menu
        filemenu = wx.Menu()
        filemenu.Append( ID_QUIT, "&Quit", "Quit pylbum" )
        wx.EVT_MENU( self, ID_QUIT, self.OnQuit )

        # Help menu
        helpmenu = wx.Menu()
        helpmenu.Append( ID_ABOUT, "&About pylbum",
                "Information about pylbum" )
        wx.EVT_MENU( self, ID_ABOUT, self.OnAbout )

        # View menu
        viewmenu = wx.Menu()
        viewmenu.Append( ID_PREFERENCES, "&Preferences",
                "Edit your preferences and configuration" )
        wx.EVT_MENU( self, ID_PREFERENCES, self.OnPreferences )

        """ Create the menubar """
        menuBar = wx.MenuBar()
        menuBar.Append( filemenu, "&File" )
        menuBar.Append( viewmenu, "&View" )
        menuBar.Append( helpmenu, "&Help" )
        self.SetMenuBar( menuBar )

    
    def CreateNotebook( self ):
        """ Create panels and add them to the notebook """
        nb = wx.Notebook( self, -1 )

        # Create the pages
        mainP = mainPage.MainPage( nb, -1, FRAME_WIDTH )
        releaseP = releasePage.ReleasePage( nb, -1, FRAME_WIDTH )
        releaseP.InitSize()
        #similarP = similarPage.SimilarPage( nb, -1 )
        #lyricP = lyricPage.LyricPage( nb, -1 )
        
        # Add the pages
        nb.AddPage( mainP, "Main" )
        nb.AddPage( releaseP, "Releases" )
        #nb.AddPage( similarP, "Similar" )
        #nb.AddPage( lyricP, "Lyrics" )

    def OnQuit(self, e):
        self.Close( True )

    def OnAbout(self, e):
        x = 1

    def OnPreferences( self, e ):
        frame = optionWindow.OptionWindow( None, wx.ID_ANY, "Preferences" )
        frame.Show( True )
        print "options shown"

class MyApp(wx.App):
    def OnInit(self):
        self.SetAppName("pylbum")

        return True

def main():
    app = MyApp(False)
    frame = MainWindow( None, wx.ID_ANY, "pylbum" )
    frame.Show( True )
    app.MainLoop()

main()
