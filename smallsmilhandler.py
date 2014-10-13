#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILHandler(ContentHandler):

    # see me aqui __Init__
    def __init__(self):
        # main smil
        self.smil = []
        self.Tags = ['root-layout', 'region', 'img', 'audio', 'textstream']

    def startElement(self, name, attrs):
        if name in self.Tags:
            dic = {}
            dic["name"] = name
            for name in attrs.getNames():
                dic[name] = attrs.get(name, '')
            self.smil.append(dic)

    def get_tags(self):
        return self.smil

if __name__ == '__main__':
    parser = make_parser()
    SSMILH = SmallSMILHandler()
    parser.setContentHandler(SSMILH)
    parser.parse(open('karaoke.smil'))
    print SSMILH.get_tags()
