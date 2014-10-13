#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax import make_parser
import smallsmilhandler as ssh
import sys
import os


class KaraokeLocal(ssh.SmallSMILHandler):

    def __init__(self, fichero):
        parser = make_parser()
        SSMILH = ssh.SmallSMILHandler()
        parser.setContentHandler(SSMILH)
        parser.parse(open(fichero))
        self.list = SSMILH.get_tags()

    def do_local(self):
        for tagsDict in self.list:
            if 'src' in tagsDict and tagsDict['src'][:6] == "http://":
                os.system("wget -q " + tagsDict['src'])
                tagsDict['src'] = tagsDict['src'].split('/')[-1]

    def __str__(self):
        returnString = ""
        for diccionario in self.list:
            returnString += diccionario['name']
            for valor in diccionario:
                if valor != "name":
                    returnString += '\t' + valor + "=" + diccionario[valor]
            returnString += "\n"
        return returnString


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage:")

    k = KaraokeLocal(sys.argv[1])
    print k
    k.do_local()
    print k
