#!/usr/bin/python

from flask import Flask, jsonify, redirect, render_template
import phatsniffer

app = Flask(__name__)

@app.route('/')
def index():
	data = phatsniffer.get_sniffer_data()
	beacons = sorted(data['beacons'].iteritems(), key=lambda x: -x[1]['rssi'])
	clients = sorted(data['clients'].iteritems(), key=lambda x: -x[1]['rssi'])
	return render_template('index.html', beacons=beacons, clients=clients)

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
