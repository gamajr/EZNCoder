# -*- coding: utf-8 -*-

import commands

class MInfo(object):
    
    def parse_data(self, file):
        """Parses data from the media file <file>"""
        self.goutput = {}
        self.voutput = {}
        self.aoutput = {}
        self.raw_lines = commands.getoutput('mediainfo %s'% file).splitlines()
        for i in self.raw_lines:
            line = i.split(':')
            if line[0] == 'General':
                output = self.goutput
            if line[0] == 'Video':
                output = self.voutput    
            if line[0] == 'Audio':
                output = self.aoutput
            output[line[0].strip()] = line[-1].strip()
               
        
    def get_vdata(self,field):
        """Retorna o valor do campo 'field' da categoria Video"""
        if self.voutput.has_key(field):
            value = self.voutput[field]
            if field == 'Bit rate':
                if value.count(' ') == 2:
                    ret = value.split()
                    value = None
                    value = ret[0]+ret[1]+' '+ret[2]
                    
            return value
        else:
            return "Field not available."
        
    def get_adata(self, field):
        """Retorna o valor do campo 'field' da categoria Audio"""
        if self.aoutput.has_key(field):
            return self.aoutput[field]
        else:
            return "Field not available."
    
    def get_gdata(self,field):
        """Retorna o valor do campo 'field' da categoria Geral"""
        if self.goutput.has_key(field):
            return self.goutput[field]
        else:
            return "Field not available."
        
    def list_fields(self, type):
        """Retorna uma lista contendo os campos disponiveis para consulta de
        cada categoria"""
        input = None
        if type == 'General':
            input = self.goutput
        if type == 'Video':
            input = self.voutput
        if type == 'Audio':
            input = self.aoutput
        return list(input.keys())