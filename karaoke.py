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

    def get_tags_local(self):
        if self.Ready:
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
                            succ = os.system(self.download + tags[2][i])
                            if succ == 0:
                                tags[2][i] = srcLocal
            return listSMIL
        else:
            return None

    def orderList(self, listSMIL):
        """
        genera:
        root-layout\twidth= "248"\theight="300"\tbackground-color="blue"\n
        """
        if self.Ready:
            newlist = []
            for tags in listSMIL:
                string = tags[0]
                for i in range(len(tags[1])):
                    string += '\\t' + tags[1][i] + '=' + '"' + tags[2][i] + '"'
                newlist.append(string + '\\n')
            return newlist
        else:
            return None

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

    def printLists(self, newlist):
        """
        print list SMIL
        """
        if self.Ready:
            for tags in newlist:
                print tags


class KaraokeLocal(openSMIL):

    def __init__(self):
        super(KaraokeLocal, self).__init__()
        self.readNow()
        self.printLists(self.orderList(self.get_tags()))

    def __str__(self):
        self.printLists(self.orderList(self.get_tags()))

    def do_local(self):
        self.printLists(self.orderList(self.get_tags_local()))


def main():
    os.system('clear')
    KL = KaraokeLocal()
    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    KL.__str__()
    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    KL.do_local()

if __name__ == '__main__':
    main()
