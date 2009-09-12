import threading, time
import sys
import Queue
import musicbrainz2.model as model
from musicbrainz2.webservice import Query, WebServiceError, ReleaseFilter

debug = False

class QueryThread ( threading.Thread ):

    def __init__( self, library ):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = Queue.PriorityQueue()
        self.lib = library

    def run ( self ):
        while True:
            pri,query,data,callback = self.queue.get(True)
            if( query( data, callback ) ):
                time.sleep(1.11)

    def lookupReleases( self, aKey, cbk, pri=12 ):
        self.queue.put( (pri, self.getReleases, aKey, cbk) )

    def getReleases( self, aKey, cbk ):

        if( self.lib.artists[aKey]['queried'] ) :
            return False

        q = Query()

        try:
            # Grab all the official releases for this artists id, ignoring
            # tags for now. All the releases are found in artist.getReleases()
            # after the query is completed
            #
            # TODO: The types searched for should be an option somewhere,
            # and tags should be incorporated somehow
            # For now I will only search for Official releases, and Albums
            filt = ReleaseFilter(
                    releaseTypes = (model.Release.TYPE_OFFICIAL,
                                    model.Release.TYPE_ALBUM),
                    artistName = aKey )
            releases = q.getReleases( filt )
        except WebServiceError, e:
            print 'Error:', e
            sys.exit(1)

        relList = []
        for xRelease in releases:
            release = xRelease.getRelease()
            if release.isSingleArtistRelease():
                found=False
                for rel in relList:
                    if release.title == rel.title:
                        found = True
                        break
                if not found:
                    relList.append( release )

        cbk( relList )

        self.lib.artists[aKey]['queried'] = True
        return True
        
if 0:
    def myPrint( releases ):
        for r in releases:
            print "Title: ", r.title

    def findReleases( aId ):
        qt.queue.put( (qt.getReleases,aId,myPrint) )

    debug = False
    qt = QueryThread()
    qt.start()
    qt.queue.put( (qt.getArtistId,"Tool",findReleases) )
    time.sleep(2)
