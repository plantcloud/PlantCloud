import gps
import subprocess

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

#subprocess.call('sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock',shell=True)

def get_gps_coords():
	while True:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'lat'):
					return report.lat,  report.lon
