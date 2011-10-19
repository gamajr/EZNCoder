# -*- coding: utf-8 -*-

from engine.generator import MEGenerator
from util.notifier import Notifier
import glob
import subprocess

class EZNCoder(object):
    """Classe que simplifica diversas tarefas, relacionadas ao MEncoder, tais 
    como adição de legendas, corte de vídeos."""
    def __init__(self):
        self._gen = MEGenerator()
    
    def open_message(self):
        pass
        
    def end_message(self):
        pass
        
    def st_encoding(self, file):
        Notifier.notify("Starting %s conversion" % file)
        
    def end_encoding(self, file, signal):
        Notifier.notify("%s conversion finished" % file)
        
    def subtitle_all(self):
        self.open_message()
        avis = sorted(glob.glob("*.avi"))
        for avi in avis:
            cmd_line = self._gen.gen_convert_line(avi)
            self.st_encoding(avi) 
            encoder = subprocess.Popen(cmd_line, shell=True)
            ret = encoder.wait()
            self.end_encoding(avi, ret)
        self.end_message()
        
if __name__ == "__main__":
    ez = EZNCoder()
    ez.subtitle_all()  