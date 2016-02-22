#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Bryan Hernandez -- @Bheru27

import json
import urllib2
import wget
import os
import shutil
import time


class Downloader(object):
    """Class downloader, we parse the thread and download the media found"""
    media = []
    downloaded = []

    def __init__(self, board, number):
        self.thread = str(number)
        self.board = board
        # [0] is board path, [1] is full path (read createfolder()
        self.folder = [board + "_" + str(number)]

    def createFolder(self):
        #Check for /4chan/ directory, change it to whatever directory you want.
        parentdirectory = os.getenv("HOME") + "/4chan/"
        fullpath = parentdirectory + self.folder[0]
        #is a bit obvious, but that way we can be "safe"
        if not os.path.isdir(parentdirectory):
            os.mkdir(parentdirectory)

        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)
            self.folder.append(fullpath)

    def parser(self):
        url="http://a.4cdn.org/{}/thread/{}.json".format(self.board, self.thread)
        try:
            website = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "404 - Thread or board not found"
                exit()

        result = json.load(website)
        files = []
        for x in xrange(len(result['posts'])):
            if 'tim' in result['posts'][x]:
                filetosave = str(result['posts'][x]['tim'])+result['posts'][x]['ext']
                if filetosave not in self.media:
                    files.append(filetosave)
        self.media = files

    def downloader(self):
        #We check again if there's media
        if not self.media:
            self.parser()
        self.createFolder()
        for picture in self.media:
            if picture not in self.downloaded:
                try:
                    print "Downloading " + picture
                    filename = wget.download("http://i.4cdn.org/"+ self.board + "/" + picture)
                    shutil.move(filename, str(self.folder[1])+"/"+filename)
                    self.downloaded.append(picture)
                    print "\n"
                except KeyboardInterrupt:
                    print "Exit"
                    exit()

    def main(self):
        while True:
            self.parser()
            self.downloader()
            print "Monitoring \n"
            #testing purposes
            #print self.downloaded
            #print self.media
            time.sleep(60) #seconds to wait


if __name__ == "__main__":
    try:
        board = raw_input("Enter board: ")
        thread = str(raw_input("Enter thread number: "))
        get = Downloader(board, thread)
        get.main()
    except KeyboardInterrupt:
        print "Canceled"
    exit()


