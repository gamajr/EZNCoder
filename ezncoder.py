# -*- coding: utf-8 -*-

from engine.generator import MEGenerator
from util.notifier import Notifier
import glob
import sys
import subprocess
import time
from Queue import Queue
from threading import Thread
from util.follow import Follower

class EZNCoder(object):
    """Classe que simplifica diversas tarefas, relacionadas ao MEncoder, tais 
    como adicao de legendas, corte de vídeos."""
    def __init__(self):
        self._gen = MEGenerator()
        self._cur_video = ""
        self._rem_video = 0
        self._videos = None
        self._fila = Queue()
        self._observers = []
        self._gen_percent = Follower()
        self._percent = 0
        
    def open_message(self):
        pass
        
    def end_message(self):
        pass
        
    def st_encoding(self, file):
        Notifier.notify("Starting %s conversion" % file)
        
    def end_encoding(self, file, signal):
        Notifier.notify("%s conversion finished" % file)
        
    def include_observer(self, observer):
        self._observers.append(observer)
        
    def remove_observer(self, observer):
        self._observers.remove(observer)
        
    def _eval_percent(self):
        input = open('output','r')
        def work():
            values = self._gen_percent.follow(input)
            for value in values:
                self._percent = int(value)
                for i in self._observers:
                    i.update_percent()
        
        t = Thread(target=work)
        t.setDaemon(True)
        t.start()
    
    def get_percent(self):
        return self._percent
    
    def get_cur_conv(self):
        return self._cur_video
        
    def get_rem_count(self):
        return self._fila.qsize()
    
    def subtitle_all(self, verbose=False):
        self._convert('sub', 'avi', verbose)
        
    def wmv2avi(self, verbose=False):
        self._convert('wmv2avi', 'wmv', verbose)
        
    def avixvid(self, verbose=False):
        self._convert('avixvid', 'avi',verbose)
        
    def _convert(self, operation, target, verbose=False):
        def work():
            if verbose:
                f = sys.stdout
                g = sys.stderr 
            else:
                f = open('output','w')
                g = open('errors','w')  
                
            for avi in sorted(glob.glob('*.'+target)):
                self._fila.put(avi)
                
            while True:
                if self._fila.empty():
                    break
                self._cur_video = self._fila.get()                
                for obs in self._observers:
                    obs.update()
                time.sleep(0.5)
                self.st_encoding(self._cur_video)
                cmd_line = self._gen.gen_convert_line(self._cur_video, operation)
                encoder = subprocess.Popen(cmd_line, shell=True, stdout=f, stderr=g)
                if not verbose:
                    self._eval_percent()
                ret = encoder.wait()
                self._fila.task_done()
                self.end_encoding(self._cur_video, ret)
                
            self._gen_percent.unfollow()
        
        p = Thread(target=work)        
        p.start()        
        
    def print_usage(self):
        print 'Rode o script com um dos argumentos:'
        print 'sub - incorpora legendas.'
        print 'wmv2avi - converte wmv para avi.'
        print 'avixvid - converte para XVid 4.' 
        
if __name__ == "__main__":
    ez = EZNCoder()
    if len(sys.argv) != 2:
        ez.print_usage()
        sys.exit(0)
    option = sys.argv[1]
    if option == 'sub':
        ez.subtitle_all(True)
    elif option == 'wmv2avi':
        ez.wmv2avi(True)
    elif option == 'avixvid':
        ez.avixvid(True)
    sys.exit(0)
    