from sqlite3 import connect

conn = connect('monitor_downloads.db')
c = conn.cursor()

def read_db():
	raw = c.execute("SELECT * FROM sampling")
	for line in raw:
		print "id:", line[0]
		print "bytes:", line[1]
		print "download rate (mbs):", line[2]
		print "download url:", line[3]
		print "create date:", line[4]
		print "\n"

read_db()

