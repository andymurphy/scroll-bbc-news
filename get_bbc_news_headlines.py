import urllib2
import xml.etree.ElementTree

print "Top Ten BBC News Headlines"

response = urllib2.urlopen('http://feeds.bbci.co.uk/news/rss.xml')

text = response.read()

root = xml.etree.ElementTree.fromstring(text)

counter = 0
for child in root[0]:
    if child.tag == 'item':
        print "Headline: " + child[0].text
        counter = counter + 1
        if counter == 10: # Break out if we get to ten
            break
