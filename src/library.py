import wx
import os
import utils
import QueryThread
import time
import re
from statusUpdate import StatusUpdate

def sanitize(str):
    return re.sub(r'[^a-zA-Z0-9]+',' ',str.encode('ascii','ignore')).lower().strip()

class Release:
    
    def __init__(self,title,have=False,date='Unknown'):
        self.title = title
        self.have = have
        self.date = date
        self.cmp = sanitize(title)

class Library:

    def __init__(self, main):
        self.main = main

        config = utils.GetConfig()
        self.musicDir = config.Read('MusicDirectory')

        self.querier = QueryThread.QueryThread(self)
        self.querier.start()
        
        self.artists = {} # la_artist: {aid:,aname:, releases:()}

    def lookupReleases(self,artistKey,priority=12):
        def compareReleases(releases,aKey=artistKey):
            wx.PostEvent( self.main,
                    StatusUpdate( "Looking up " + self.artists[aKey]['name'] ) )
            if len(releases):
                self.artists[aKey]['aid'] = releases[0].getArtist().id
            for rel in releases:
                found = False
                cmp = sanitize(rel.title)
                date = rel.getEarliestReleaseDate()
                if date is None: date = "Unknown"
                for cur in self.artists[aKey]['releases']:
                    if cur.cmp == cmp:
                        found = True
                        cur.date = date
                        #print "Found ", rel.title, " (", cur.date
                        break
                if not found:
                    #print "Found new ", rel.title
                    self.artists[aKey]['releases'].append(
                            Release(rel.title, False, date) )
        self.querier.lookupReleases( artistKey, compareReleases, priority  )
       

    def Populate(self):
        artists = os.listdir( self.musicDir )
        for name in artists:
            try:
                artistDir = os.path.join( self.musicDir, name )
            except UnicodeDecodeError:
                print "Bad artist path: " + name
                continue
            if os.path.isdir( artistDir ):
                aKey = sanitize(name)
                self.artists[aKey] = {
                        'aid':0,
                        'name':name,
                        'releases': [],
                        'queried':False
                        }
                albums = os.listdir(artistDir)
                for release in albums:
                    try:
                        releaseDir = os.path.join(artistDir, release)
                    except UnicodeDecodeError:
                        print "Bad album path: " + release
                        continue
                    if os.path.isdir(releaseDir):
                        self.artists[aKey]['releases'].append( Release(release,True) )
                self.lookupReleases( aKey );

if 0:
    app = wx.App()
    app.SetAppName("pylbum")
    l = Library()
    l.Populate()
    time.sleep(30)
