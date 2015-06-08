#!/usr/bin/env python2


import urllib2
import json
import re
import HTMLParser


class search(object):
    term = ""
    definition = ""
    link = ""

    def __init__(self, term):
        self.term = term
        try:
           website = urllib2.urlopen("https://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&safe=active&q=" + urllib2.quote(self.term) + "&max-results=1&v=2&prettyprint=false&alt=json")
        except:
           pass
        response = json.load(website)
        if len(response['responseData']['results']) > 0:
            self.definition = re.sub(r'<.*?>', '', response['responseData']['results'][0]['content'])
            self.link = response['responseData']['results'][0]['url']
        else:
            self.definition = "No answers found for: " + self.term

        return None

    def results(self):
        parse = HTMLParser.HTMLParser()
        return self.link + ": " + parse.unescape(self.definition)

    def usage(self):
        return "Usage: sb gsearch term"


def main(words):
    data = search(words)
    print data.results()


if __name__ == "__main__":
    main(raw_input("Write a word to search \n >>"))
