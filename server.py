#!/usr/bin/python

from flask import Flask, jsonify, redirect, render_template
import math, json
import phatsniffer

app = Flask(__name__)

@app.route('/')
def index():
	data = phatsniffer.get_sniffer_data()
	beacons = sorted(data['beacons'].iteritems(), key=lambda x: -x[1]['rssi'])
	clients = sorted(data['clients'].iteritems(), key=lambda x: -x[1]['rssi'])
	circles = {}
	circles['name'] = 'root'
	circles['children'] = []
	circles_beacons = circles['children']
	for beacon in data['beacons']:
		data_beacon = data['beacons'][beacon]
		circles_beacon = {}
		if 'vendor' in data_beacon:
			circles_beacon['name'] = data_beacon['vendor']
		else:
			circles_beacon['name'] = 'Unknown'
		circles_beacon['children'] = []
		circles_clients = circles_beacon['children']
		for client in data['clients']:
			data_client = data['clients'][client]
			if data_client['beacon'] == beacon and data_client['rssi'] > -100:
				circles_client = {}
				if 'vendor' in data_client:
					circles_client['name'] = data_client['vendor']
				else:
					circles_client['name'] = 'Unknown'
				circles_client['size'] = math.sqrt(100+data_client['rssi'])
				circles_clients.append(circles_client)
		circles_beacons.append(circles_beacon)
	return render_template('index.html', beacons=beacons, clients=clients, circles=json.dumps(circles))

@app.route('/download')
def download():
	return jsonify(phatsniffer.get_sniffer_data())

@app.route('/reset')
def reset():
	phatsniffer.reset_phat()
	return redirect('/')


if __name__ == '__main__':
	phatsniffer.read_vendors('data/vendors.tsv')
	app.run(debug=False, host='0.0.0.0')
