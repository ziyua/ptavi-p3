#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILHandler(ContentHandler, object):
    """
    Obujeto es
    crea un list como:
    self._smil =
    [[name of tag, [names of attributes], [value of attributes]], ...]
    """

    def _subinit(self):
        # attr
        self.tmpAttr = []
        self.tmpAttrNames = []
        # smil.name
        self.root_layout = []
        self.region = []
        self.img = []
        self.audio = []
        self.textstream = []

    # see me aqui __Init__
    def __init__(self):
        # main smil
        self._smil = []
        self._subinit()

    def _addAttr(self, attrs):
        """
        crea dos list temp, 1: [names of attributes]; 2: [value of attributes]
        """
        #! self.tmpAttr = []
        names = attrs.getNames()
        self.tmpAttrNames = names
        for name in names:
            self.tmpAttr.append(attrs.get(name, ''))

    def _addNameQAttrs(self, listname, name):
        """
        list:
        Añade 1: name of tag;
               2: [names of attributes];
               3: [value of attributes];

        Añade list a self._smil;
        """
        listname.append(name)
        listname.append(self.tmpAttrNames)
        listname.append(self.tmpAttr)
        self._smil.append(listname)

    def startElement(self, name, attrs):
        """
        1. 'self._smil' es list total;
        eval() name como "self.root_layout" --> list: self.root_layout = []
        clean sub-list, than anade element.
        """

        selfname = 'self.' + name
        selfname = selfname.replace('-', '_')
        try:
            selflist = eval(selfname)
        except AttributeError:
            pass
        else:
            self._subinit()
            self._addAttr(attrs)
            self._addNameQAttrs(selflist, name)

    def endElement(self, name):
        """
        no usa etiquetas </final> -> pass
        """
        pass

    def characters(self, char):
        """
        no tiene contenido entre <div></div> -> pass
        """
        pass

    def get_tags(self):
        return self._smil


def main():
    parser = make_parser()
    SSMILH = SmallSMILHandler()
    parser.setContentHandler(SSMILH)
    parser.parse(open('karaoke.smil'))
    print SSMILH.get_tags()

if __name__ == '__main__':
    main()
