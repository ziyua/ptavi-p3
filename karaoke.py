#! /usr/bin/python
# -*- coding: utf-8 -*-


from xml.sax import make_parser
import smallsmilhandler as ssh
from sys import argv
import os


class openSMIL(ssh.SmallSMILHandler):

    def __init__(self):
        """
        try error
        """
        self.Ready = False
        try:
            self.ofile = open(argv[1])
        except IndexError:
            print 'Usage: python karaoke.py file.smil.'
        except IOError:
            print 'Archivo <' + argv[1] + '> no encontrado.'
        else:
            """
            def ready si esta bien, run, si no exit
            """
            self.Ready = True
            self.download = "wget -q "
            super(openSMIL, self).__init__()

    def _get_src(self):
        listSMIL = self.get_tags()
        for tags in listSMIL:
            for i in range(len(tags[1])):
                if tags[1][i].lower() == 'src':
                    try:
                        srcLocal = tags[2][i].rsplit('/', 1)[1]
                    except IndexError:
                        srcLocal = tags[2][i]
                    if os.path.exists(srcLocal):
                        tags[2][i] = srcLocal
                    else:
                        print 'Downloading... ' + srcLocal,
                        succ = os.system(self.download + tags[2][i])
                        if succ == 0:
                            print ':) ok'
                            tags[2][i] = srcLocal
                        else:
                            print ':( No exsist.'
        return listSMIL

    def _orderList(self, listSMIL):
        """
        genera:
        root-layout\twidth= "248"\theight="300"\tbackground-color="blue"\n
        """
        newlist = []
        for tags in listSMIL:
            string = tags[0]
            for i in range(len(tags[1])):
                string += '\\t' + tags[1][i] + '=' + '\"' + tags[2][i] + '\"'
            newlist.append(string + '\\n')
        return newlist

    def readNow(self):
        """
        handler es self.
        """
        if self.Ready:
            parser = make_parser()
            parser.setContentHandler(self)
            try:
                parser.parse(self.ofile)
            except:
                self.Ready = False
                print 'Waring: Error contenido en <' + self.ofile.name + '>'
            else:
                self.newlist = self._orderList(self._get_src())

    def printLists(self):
        """
        print list SMIL
        """
        if self.Ready:
            for tags in self.newlist:
                print tags


def main():
    RSMIL = openSMIL()
    RSMIL.readNow()
    RSMIL.printLists()

if __name__ == '__main__':
    main()
