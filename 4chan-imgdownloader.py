#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Bryan Hernandez -- @Bheru27

import json
import urllib2
import wget
import os
import shutil

class Downloader(object):
    media = []
    thread = ''
    board = ''
    folder = ''

    def __init__(self, board, number):
        self.thread = str(number)
        self.board = board
        self.folder = "/home/user/Docs/4chan/"+board+"_"+str(number) #Change "user" and "docs" for any existing folder where it will be stored

    def img_get(self):

        try:
          website =  urllib2.urlopen("http://a.4cdn.org/"+ self.board +"/thread/"+ self.thread +".json")
        except urllib2.HTTPError, err:
            if err.code == 404:
                return "404 - Thread or board not found"
            else:
                return "Unknown error, check your internet connection or input"
        results = json.load(website)
        pictures = []
        for x in xrange(len(results['posts'])):
            if 'tim' in results['posts'][x]:
                pictures.append(str(results['posts'][x]['tim'])+results['posts'][x]['ext'])
        self.media = pictures
        return "OK"

    def img_download(self):
        if not self.media:
            self.img_get()
        links = [] 
        os.mkdir(self.folder)
        for pictures in self.media:
            links.append("http://i.4cdn.org/"+ self.board + "/" + pictures)
        try:
            for url in links:
                print "Downloading: " + url +"\n"
                print "File %i of %i" %(links.index(url), len(links))
                filename = wget.download(url)
                shutil.move(filename, self.folder+"/"+filename) 
        except KeyboardInterrupt:
            return "Canceled"
        return "OK"


if __name__ == "__main__":
    try:
        board = raw_input("Enter board: ")
        thread = str(raw_input("Enter thread number: "))
        #Working on letting the user select the path... 
        #path=raw_input("Enter path to download files: ")
        download = Downloader(board, thread)
        download.img_download() 
    except KeyboardInterrupt:
        print "Canceled"
        exit()
 


