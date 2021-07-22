from flask import Flask, request, abort, jsonify

import os
import shutil
import subprocess

app = Flask(__name__)

def validate_file(input_path):
	# Run promtool in order to check file syntax
	completed = subprocess.run(["promtool","check","rules",input_path],text=True,capture_output=True)
	output = completed.stdout
	if (output.find("SUCCESS") != -1):
		return True
	else:
		os.remove(input_path)
		return False

def validate_monitoring_id(monitoring_id, presence):
	if monitoring_id is None:
		return False
	if not presence: 
		return True
	else:
		return os.path.isfile("/etc/prometheus/rules/%s.yml" % monitoring_id)

def register_rule_file(filepath):
	try:
		print(filepath)
		shutil.copy(filepath,'/etc/prometheus/rules')
		os.remove(filepath)
		return True
	except OSError:
		return False

def unregister_rule_file(monitoring_id):
	try:
		os.remove("/etc/prometheus/rules/%s.yml" % monitoring_id)
		return True
	except FileNotFoundError:
		return False

def reload_prometheus_configuration():
	p1 = subprocess.Popen(["echo", "-e", "POST /containers/prometheus/kill?signal=SIGHUP HTTP/1.0\r\n"], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["nc", "-U", "/var/run/docker.sock"], stdin=p1.stdout, stdout=subprocess.PIPE)
	out, err = p2.communicate()
	check = str(out).find("HTTP/1.0 204 No Content")
	return (check > 0)

@app.route('/rules/<monitoring_id>', methods=['POST'])
def add_rule_file(monitoring_id=None):
	if not validate_monitoring_id(monitoring_id, False):
		return "Model id is not valid\n", 400

	input_path = "/tmp/%s.yml" % monitoring_id
	f = open(input_path, "bw")
	f.write(request.get_data())
	f.close()

	if not validate_file(input_path):
		return "Rule file did not pass the promtool check\n", 400
	else:
		if register_rule_file(input_path):
			if reload_prometheus_configuration():
				return ("Updated Prometheus config with a rule file for monitoring id %s\n" % monitoring_id), 200
			else:
				return "Rule file was added but config reload failed\n", 500
		else:
			return "Rule file could not be copied to Prometheus rules folder\n", 500

@app.route('/rules/<monitoring_id>', methods=['DELETE'])
def remove_rule_file(monitoring_id=None):

	if not validate_monitoring_id(monitoring_id, True):
		return ("Could not find ruleset for monitoring_id %s\n" % monitoring_id),  404

	if unregister_rule_file(monitoring_id):
		if reload_prometheus_configuration():
			return ("Updated Prometheus config with rules for monitoring id %s removed\n" % monitoring_id), 200
		else:
			return "Rule file was removed but config reload failed\n", 500
	else:
		return ("Rule file for monitoring id %s could not be deleted\n" % monitoring_id), 500
