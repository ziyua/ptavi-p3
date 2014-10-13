#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax import make_parser
import smallsmilhandler as ssh
import sys
import os


class KaraokeLocal():

    def __init__(self, filename):
        parser = make_parser()
        SSMILH = ssh.SmallSMILHandler()
        parser.setContentHandler(SSMILH)
        parser.parse(open(filename))
        self.list = SSMILH.get_tags()

    def do_local(self):
        for dic in self.list:
            if 'src' in dic and dic['src'][:7] == "http://":
                nameLocal = dic['src'].rsplit('/', 1)[1]
                if not os.path.exists(nameLocal):
                    os.system("wget -q " + dic['src'])
                dic['src'] = nameLocal

    def __str__(self):
        returnStr = ""
        for dic in self.list:
            returnStr += dic['name']
            for key in dic:
                if key != "name":
                    returnStr += '\t' + key + '="' + dic[key] + '"'
            returnStr += "\n"
        return returnStr


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python karaoke.py file.smil")

    k = KaraokeLocal(sys.argv[1])
    print k
    k.do_local()
    print k
