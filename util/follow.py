import time
import re

class Follower(object):
    def __init__(self):
        self.go = True
    def follow(self, thefile):
        thefile.seek(0,2)      # Go to the end of the file
        rex = re.compile('[0-9]+\%')
        while self.go:
            line = thefile.readline()
            if not line:
                time.sleep(1.0)    # Sleep briefly
                continue                
            match = rex.search(line)
            if match:
                resp = match.string[match.start():match.end()-1]
            else:
                resp = 0
            yield resp
        
    def unfollow(self):
        self.go = False
        
##logfile = open("ops")
##loglines = follow(logfile)
##for line in loglines:
##    print line

#TODO: Implement unfollow method!!!