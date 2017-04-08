#!/usr/bin/python

import json
import serial
import time
import RPi.GPIO


vendors = {}
def read_vendors(filename):
	file = open(filename, 'r')
	for line in file:
		prefix, vendor = line.rstrip().split('\t')
		vendors[prefix] = vendor


def send_command(command):
	comm = serial.Serial('/dev/serial0', 115200)
	if comm.isOpen():
		comm.close()
	comm.open()
	comm.flushInput()
	comm.write(command+'\n')
	time.sleep(0.1)
	return comm.readline()


def get_sniffer_data():
	data = json.loads(send_command('print_all'))
	beacons = data['beacons']
	clients = data['clients']
	for beacon in beacons:
		prefix = beacon[0:8]
		if prefix in vendors:
			beacons[beacon]['vendor'] = vendors[prefix]
	for client in clients:
		beacon = clients[client]['beacon']
		if beacon in beacons:
			clients[client]['ssid'] = beacons[beacon]['ssid']
			clients[client]['channel'] = beacons[beacon]['channel']
		else:
			clients[client]['ssid'] = ''
			clients[client]['channel'] = ''
		prefix = client[0:8]
		if prefix in vendors:
			clients[client]['vendor'] = vendors[prefix]
	return data


def reset_phat():
	RPi.GPIO.setmode(RPi.GPIO.BCM)
	RPi.GPIO.setup(17,RPi.GPIO.OUT,initial=1)
	RPi.GPIO.setup(27,RPi.GPIO.OUT,initial=1)
	RPi.GPIO.output(17,0)
	time.sleep(0.5)
	RPi.GPIO.output(17,1)
	time.sleep(0.5)
	RPi.GPIO.cleanup()


if __name__ == '__main__':
	read_vendors('data/vendors.tsv')
	print json.dumps(get_sniffer_data(), sort_keys=True, indent=4, separators=(',', ': '))
