#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Bryan Hernandez -- @Bheru27

import json
import urllib2
import wget # pip install wget
import os
import shutil #is the best option to move from tmp(wget) to the current folder
import time

class Downloader(object):
    """Class downloader, we parse the thread and download the media found"""
    media = []
    downloaded = []
    
    def __init__(self, board, number):
        self.thread = str(number)
        self.board = board
        self.folder = [board+"_"+str(number)] # [0] is board path, [1] is full path (read createfolder()

    def createFolder(self):
        #We check for /4chan/ directory, change it to whatever directory you want.
        parentdirectory = os.getenv("HOME")+"/4chan/"
        fullpath = parentdirectory+self.folder[0]
        #is a bit obvious, but that way we can be "safe"
        if not os.path.isdir(parentdirectory):
            os.mkdir(parentdirectory)
            
        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)
            self.folder.append(fullpath)

    def parser(self):
        try:
                website = urllib2.urlopen("http://a.4cdn.org/"+ self.board +"/thread/"+ self.thread +".json")
        except urllib2.HTTPError, err:
                if err.code == 404:
                    print "404 - Thread or board not found"
                    exit()
                    
        result = json.load(website)
        files = []
        for x in xrange(len(result['posts'])):
            if 'tim' in result['posts'][x]:
                file = str(result['posts'][x]['tim'])+result['posts'][x]['ext']
                if file not in self.media:
                    files.append(file)
        self.media = files

    def downloader(self):
        #We check again if there's media
        if not self.media:
            self.parser()
        links = []
        self.createFolder()
        for picture in self.media:
            if picture not in self.downloaded:
                try:
                    #print "File %i of %i" %(links.index(self.media), len(self.media))
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

    
