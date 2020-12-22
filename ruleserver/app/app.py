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

def validate_modelid(model_id):
	return (model_id is not None)

def register_rule_file(filepath,model_id):
	try:
		print(filepath)
		shutil.copy(filepath,'/etc/prometheus/rules')
		os.remove(filepath)
		return True
	except OSError:
		return False

def unregister_rule_file(model_id):
	try:
		os.remove("/etc/prometheus/rules/rules_%s.yml" % model_id)
		return True
	except FileNotFoundError:
		return False

def reload_prometheus_configuration():
	p1 = subprocess.Popen(["echo", "-e", "POST /containers/prometheus/kill?signal=SIGHUP HTTP/1.0\r\n"], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["nc", "-U", "/var/run/docker.sock"], stdin=p1.stdout, stdout=subprocess.PIPE)
	out, err = p2.communicate()
	check = str(out).find("HTTP/1.0 204 No Content")
	return (check > 0)

@app.route('/rules/add/<model_id>', methods=['POST'])
def add_rule_file(model_id=None):
	if not validate_modelid(model_id):
		return "Model id is not valid", 400

	input_path = "/tmp/rules_%s.yml" % model_id
	f = open(input_path, "bw")
	f.write(request.get_data())
	f.close()

	if not validate_file(input_path):
		return "Rule file did not pass the promtool check", 400
	else:
		if register_rule_file(input_path,model_id):
			if reload_prometheus_configuration():
				return ("Updated Prometheus config with a rule file for model id %s" % model_id), 200
			else:
				return "Rule file was added but config reload failed", 400
		else:
			return "Rule file could not be copied to Prometheus rules folder", 400

@app.route('/rules/remove/<model_id>', methods=['GET'])
def remove_rule_file(model_id=None):

	if not validate_modelid(model_id):
		return "Model id is not valid", 400

	if unregister_rule_file(model_id):
		if reload_prometheus_configuration():
			return ("Updated Prometheus config with rules for model id %s removed" % model_id), 200
		else:
			return "Rule file was removed but config reload failed", 400
	else:
		return ("Rule file for model %s has been not found" % model_id), 400
