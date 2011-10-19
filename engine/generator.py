# -*- coding: utf-8 -*-

import string
from infoparser import MInfo

class MEGenerator():
    """Classe que gera linhas de comando para o MEncoder."""
    def __init__(self):
        self._cnv_cmd = string.Template("""mencoder -oac $audio_opts -ovc xvid -xvidencopts
         bitrate=$br -sub $srt_file -subpos 90 -subfont-text-scale 3 
        -subfont-outline 2 -subcp ISO-8859-1 -sub-bg-alpha 200 -o $conv_file $orig_file""")
        self._cut_cmd = string.Template("")
        
    def gen_convert_line(self, media_file):
        """Gera uma linha de comando para o MEncoder para a incorporacao de 
        legendas .srt no arquivo avi, bastando informar o nome do arquivo atraves
        do argumento media_file."""
        base_name=media_file[:-4]
        info = MInfo()
        info.parse_data(base_name+'.avi')        
        kbps = int(info.get_vdata('Bit rate').split()[0])
        if kbps % 50 != 0:
            br = str(kbps + (50 - kbps % 50))
        else:
            br = str(kbps)
            
        audio_opts=''
        if info.get_adata('Codec ID/Hint')=='MP3':
            audio_opts = 'copy'
        else:
            audio_opts = 'mp3lame -lameopts cbr:mode=2:br=192'
        
        return ' '.join(self._cnv_cmd.substitute({'audio_opts':audio_opts, 'br':br,
     'srt_file': base_name+'.srt', 'conv_file':base_name+'_sub.avi',
     'orig_file':base_name+'.avi'}).split())
    
    def gen_cut_line(self, media_file, cut_point=None):
        """Gera uma lista com as linhas de comando para cortar um video
        atraves do MEncoder. Se os dois argumentos forem None, os video e
        dividido em dois."""
#TODO: Implementar gen_cut_line!!!!

