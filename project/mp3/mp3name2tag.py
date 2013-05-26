#!/usr/bin/env python
'''
From mp3 file name, make a tag.
Default conversion option is to add full file name to 

Created on 2009. 8. 1.
'''

import eyeD3
import sys
import os
import glob

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >>sys.stderr, "Usage: mp3name2tag <mp3_directory> index(ex[0:3])"
        sys.exit()
    if os.path.isdir(sys.argv[1]) == False:
        print >>sys.stderr, "Usage: mp3name2tag <mp3_directory> index"
        sys.exit()
    
    files = glob.glob(sys.argv[1] + os.sep + "*" )
    
    mp3files = [ f for f in files if eyeD3.isMp3File(f) ]
    
    for mp3 in mp3files:
        try:
            mp3name = os.path.basename(mp3)
            tag = eyeD3.Tag()
            success = tag.link(mp3)
            if success == False:
                tag.header.setVersion(eyeD3.ID3_V2_3)
            
            trackNum = int(eval("mp3name"+sys.argv[2]))
            tag.setTrackNum((trackNum, trackNum))
            tag.setDiscNum((trackNum, trackNum))
            success = tag.update()
            if success == False:
                raise
            print "%s's track number is changed to %d" % (mp3, (int(eval("mp3name"+sys.argv[2]))) )
<<<<<<< .mine
        except:
            print >>sys.stderr, "Error in %s" % mp3
=======
        except Exception as detail:
            print >>sys.stderr, "Error in %s" % mp3
            print detail>>>>>>> .r49
