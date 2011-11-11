# -*- coding: utf-8 -*-

import string
from infoparser import MInfo

class MEGenerator():
    """Classe que gera linhas de comando para o MEncoder."""
    def __init__(self):
        
        self._cut_cmd = string.Template("")
        self.info = MInfo()
        self._supported_ops = ['sub','wmv2avi','avixvid']
    def gen_convert_line(self, media_file, operation):
#TODO: Escrever DocString 
        if operation == 'sub':
            resp = self._subtitle(media_file)
        elif operation == 'wmv2avi':
            resp = self._wmv2avi(media_file)
        elif operation == 'avixvid':
            resp = self._avixvid(media_file)
        else:
            resp = None
        return resp
    
    def gen_cut_line(self, media_file, cut_point=None):
        """Gera uma lista com as linhas de comando para cortar um video
        atraves do MEncoder. Se os dois argumentos forem None, os video e
        dividido em dois."""
        pass

    def _subtitle(self, media_file):
        cmd = string.Template("""mencoder -oac $audio_opts -ovc xvid -xvidencopts
         bitrate=$br -sub $srt_file -subpos 90 -subfont-text-scale 3 
        -subfont-outline 2 -subcp ISO-8859-1 -sub-bg-alpha 200 -o $conv_file $orig_file""")
        base_name=media_file[:-4]        
        self.info.parse_data(base_name+'.avi')        
        kbps = int(self.info.get_vdata('Bit rate').split()[0])
        if kbps % 50 != 0:
            br = str(kbps + (50 - kbps % 50))
        else:
            br = str(kbps)
            
        audio_opts=''
        if self.info.get_adata('Codec ID/Hint')=='MP3':
            audio_opts = 'copy'
        else:
            audio_opts = 'mp3lame -lameopts cbr:mode=2:br=192'
        
        return ' '.join(cmd.substitute({'audio_opts':audio_opts, 'br':br,
     'srt_file': base_name+'.srt', 'conv_file':base_name+'_sub.avi',
     'orig_file':base_name+'.avi'}).split())

    def _wmv2avi(self, media_file):
        cmd = string.Template("""mencoder -oac mp3lame -lameopts cbr:mode=2:br=64
         -ovc lavc -ofps 23.976 -o $conv_file $orig_file""")
        base_name=media_file[:-4]
        return ' '.join(cmd.substitute({'conv_file':base_name+'_conv.avi', 'orig_file':base_name+'.wmv'}).split())
    
    def _avixvid(self, media_file):
        cmd = string.Template("""mencoder -oac $audio_opts -ovc xvid -xvidencopts
         bitrate=850 -o $conv_file $orig_file""")  
        base_name=media_file[:-4]        
        self.info.parse_data(base_name+'.avi')  
        audio_opts=''
        if self.info.get_adata('Codec ID/Hint')=='MP3':
            audio_opts = 'copy'
        else:
            audio_opts = 'mp3lame -lameopts cbr:mode=2:br=192'
        
        return ' '.join(cmd.substitute({'audio_opts':audio_opts,
        'conv_file':base_name+'_conv.avi', 'orig_file':base_name+'.avi'}).split())
    def get_supported_operations(self):
        return self._supported_ops
    
#TODO: Implementar gen_cut_line!!!!
#mencoder infile.wmv -ofps 23.976 -ovc lavc -oac copy -o outfile.avi