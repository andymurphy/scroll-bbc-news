# Gets bbc news headlines

import urllib2
import xml.etree.ElementTree as et
import scrollphathd as sphd
import time
import RPi.GPIO as GPIO
#import msvcrt

# Set up the headlines stuff
news_rss = 'http://feeds.bbci.co.uk/news/rss.xml'
sport_rss = 'http://feeds.bbci.co.uk/sport/rss.xml?edition=uk'
tech_rss = 'http://feeds.bbci.co.uk/news/technology/rss.xml'
headlines = []
sport_headlines = []
tech_headline = ""
# Set up the GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

# Define functions
def internet_on():
	try:
		urllib2.urlopen('http://216.58.192.142', timeout = 1)
		sphd.set_pixel(0,0,0.3)
		sphd.show()
		return True
	except urllib2.URLError as err:
		return False

def get_news_headlines():
	GPIO.output(21, GPIO.HIGH)
	response = urllib2.urlopen(news_rss)
	text = response.read()
	root = et.fromstring(text)
	# Store the first three headlines in a list
	for i in range(9, 12):
		headlines.append(root[0][i][0].text)
	sphd.set_pixel(1,0,0.3)
	sphd.show()
	GPIO.output(21, GPIO.LOW)
	# print them to the console
	for listitem in range(len(headlines)):
		print(str(listitem + 1) + ": " + headlines[listitem])

def get_sport_headlines():
	GPIO.output(21, GPIO.HIGH)
	sport_response = urllib2.urlopen(sport_rss)
	sport_text = sport_response.read()
	sport_root = et.fromstring(sport_text)
	sport_headline1 = sport_root[0][9][0].text
	sport_headlines.append(sport_headline1)
	sphd.set_pixel(2,0,0.3)
	sphd.show()
	GPIO.output(21, GPIO.LOW)
	print("Sport: " + sport_headlines[0])

def get_tech_headline():
	GPIO.output(21, GPIO.HIGH)
	tech_response = urllib2.urlopen(tech_rss)
	tech_text = tech_response.read()
	tech_root = et.fromstring(tech_text)
	tech_headline = tech_root[0][9][0].text
	sphd.set_pixel(0,0,0.3)
	sphd.show()
	GPIO.output(21, GPIO.LOW)
	print("Tech: " + tech_headline)
	return tech_headline

print("Starting scroll script for BBC news, sport and tech headlines.")
print ("Waiting for Internet to be available...")

internet_available = False
while (internet_available == False):
	internet_available = internet_on()
print("Internet available")

sphd.set_brightness(0.3) # could add a light sensor and adjust the brightness automatically

# Loop to refresh the headlines from the Internet
for n in range(0,2):
	# clear the lists
	headlines = [] 
	sport_headlines = []
	# refresh the info from the internet
	get_news_headlines()
	get_sport_headlines()
	tech_headline = get_tech_headline()

	# scroll them on the scrollphathd
	sphd.write_string("Headlines 1: " + headlines[0] + "  2: " + headlines[1] +  "  Sport: " + sport_headlines[0] + " Tech: " + tech_headline + "        ")
	buffer = sphd.get_buffer_shape()

	# Loop to scroll the headlines n times
	for i in range(0, 2):
		print(i)
		# Loop to scroll the buffer
		for j in range(0, buffer[0] - 10):
			sphd.show()
			sphd.scroll(1)
			time.sleep(0.02) # used 0.02 initially
	print("Headlines scrolled 2 times. Refreshing headlines.")


