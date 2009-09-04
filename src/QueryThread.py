import threading, time
import sys
import Queue
import musicbrainz2.model as model
from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ArtistIncludes

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
            query( data, callback )
            time.sleep(1.01)

    def lookupAId( self, aKey, cbk, pri=10 ):
        self.queue.put( (pri, self.getArtistId, aKey, cbk) )

    def lookupReleases( self, aKey, cbk, pri=12 ):
        self.queue.put( (pri, self.getReleases, aKey, cbk) )

    def getArtistId( self, artistName, cbk ):

        q = Query()
        
        try:
            #Search for the best match for the given name only
            #change the limit to adjust how many artists are found
            #
            f = ArtistFilter(name=artistName, limit=1)
            artistResults = q.getArtists(f)
        except WebServiceError, e:
            print 'Error:', e
            sys.exit(1)

        if len(artistResults) > 0 :
            artist = artistResults[0].artist

            ###### DEBUG #######
            if debug:
                print artist.name, ' => ', artist.id

            #### END DEBUG #####
            cbk( artist.id )

    def getReleases( self, aKey, cbk ):

        id = self.lib.artists[aKey]['aid']
        if id == 0: # Don't have an aId yet
            print "Tried to look up ", id, " releases without an id"
            return;

        q = Query()

        try:
            # Grab all the official releases for this artists id, ignoring
            # tags for now. All the releases are found in artist.getReleases()
            # after the query is completed
            #
            # TODO: The types searched for should be an option somewhere,
            # and tags should be incorporated somehow
            # For now I will only search for Official releases, and Albums
            inc = ArtistIncludes(
                releases = (model.Release.TYPE_OFFICIAL,
                            model.Release.TYPE_ALBUM),
                tags=False)
            artist = q.getArtistById( id, inc )
        except WebServiceError, e:
            print 'Error:', e
            sys.exit(1)

        ###### DEBUG ######
        if debug:
            if len(artist.getReleases()) == 0:
                print "No releases found for ", artist.name
                print
            else:
                for release in artist.getReleases():
                    print "Title: ", release.title
        #####    END DEBUG  #######

        cbk( artist.getReleases() )
        
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
