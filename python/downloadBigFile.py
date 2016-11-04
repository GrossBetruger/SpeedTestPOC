import requests 
import time 
import sys
import sqlite3
from datetime import datetime, date

kodi_url = "http://mirrors.kodi.tv/releases/osx/x86_64/kodi-16.1-Jarvis-x86_64.dmg"

url = sys.argv[1]

def download_big_file():
	print "starting download"
	payload = requests.get(url)
	print "done downloading"
	filesize = payload.headers['content-length']
	return filesize

def download_and_monitor():
	stamp = time.time() 
	filesize = int(download_big_file())
	seconds = str(time.time() - stamp)
	rate = float(filesize)/float(seconds)
	mb_rate = rate/10**6
	return filesize, mb_rate
	


conn = sqlite3.connect('monitor_downloads.db')
c = conn.cursor()
filesize, rate = download_and_monitor()
speedtest = "unknown"

c.execute("""INSERT INTO sampling (
		filesize,
		downloadrate,
		url)
		
		VALUES 
		(
		?, ?, ?
		);""", (filesize, rate, url))

conn.commit()
conn.close()
			
				 
		
	
