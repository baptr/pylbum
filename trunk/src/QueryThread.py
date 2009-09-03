import threading, time
import sys
import musicbrainz2.model as model
from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ArtistIncludes

class QueryThread ( threading.Thread ):

    def run ( self ):
        id = self.getArtistId( sys.argv[1] )
        self.getReleases( id )

    def getArtistId( self, artistName ):

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

        artist = artistResults[0].artist

        ###### DEBUG #######
        if debug:
            print artist.name, ' => ', artist.id

        #### END DEBUG #####
        time.sleep(1.01)
        return artist.id

    def getReleases( self, id ):

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

        time.sleep(1.01)
        return artist.getReleases()
        
        
    
        
debug = False
QueryThread().start()
