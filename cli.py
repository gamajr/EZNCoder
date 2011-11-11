# -*- coding: utf-8 -*-
from ezncoder import EZNCoder
import subprocess
from util.progressbar import ProgressBar
from threading import Thread

class EZNCoderC(object):    
    def __init__(self):
        self._encoder = EZNCoder()
        self._encoder.include_observer(self)
        self._p_bar = ProgressBar('green', width=70, block='▣', empty='□')
        print 'EZNCoder  v0.2'
        self._encoder.avixvid()
            
    def update(self):
        print 'Converting: ' + self._encoder.get_cur_conv()
        print '\n'
        print 'Remaining ' + str(self._encoder.get_rem_count()) + ' file(s).'
        
    def update_percent(self):
        i = self._encoder.get_percent()
        self._p_bar.render(i,'')        
    
    def cleanup(self):    
        pass
        
if __name__ == "__main__":
    
    c = EZNCoderC()
    
  