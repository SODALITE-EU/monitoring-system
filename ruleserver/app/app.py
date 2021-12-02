from flask import Flask, request

import os
import shutil
import subprocess
import requests
import re

app = Flask(__name__)

prometheus_address = os.getenv("PROMETHEUS_ADDRESS", "prometheus")
prometheus_address = prometheus_address if prometheus_address.startswith('http') else 'http://' + prometheus_address
reload_endpoint = prometheus_address + '/-/reload'


def _validate_file(input_path):
    # Run promtool in order to check file syntax
    completed = subprocess.run(["promtool", "check", "rules", input_path], text=True, capture_output=True)
    output = completed.stdout
    if (output.find("SUCCESS") != -1):
        return True
    else:
        os.remove(input_path)
        return False


def _find_monitoring_id(monitoring_id):
    return os.path.isfile("/etc/prometheus/rules/%s.yml" % monitoring_id)


def _validate_monitoring_id(monitoring_id):
    pattern = re.compile("^[0-9a-zA-Z_-]+$")
    pattern.match(monitoring_id)


def _register_rule_file(filepath):
    try:
        print(filepath)
        shutil.copy(filepath, '/etc/prometheus/rules')
        os.remove(filepath)
        return True
    except OSError:
        return False


def _unregister_rule_file(monitoring_id):
    try:
        os.remove("/etc/prometheus/rules/%s.yml" % monitoring_id)
        return True
    except FileNotFoundError:
        return False


def _reload_prometheus_configuration():
    resp = requests.post(reload_endpoint)
    return resp.ok


@app.route('/rules/<monitoring_id>', methods=['POST'])
def add_rule_file(monitoring_id=None):
    if not _validate_monitoring_id(monitoring_id):
        return "Monitoring id is not valid\n", 401

    input_path = "/tmp/%s.yml" % monitoring_id
    f = open(input_path, "bw")
    f.write(request.get_data())
    f.close()

    if not _validate_file(input_path):
        return "Rule file did not pass the promtool check\n", 400
    else:
        if _register_rule_file(input_path):
            if _reload_prometheus_configuration():
                return ("Updated Prometheus config with a rule file for monitoring id %s\n" % monitoring_id), 200
            else:
                return "Rule file was added but config reload failed\n", 500
        else:
            return "Rule file could not be copied to Prometheus rules folder\n", 500


@app.route('/rules/<monitoring_id>', methods=['DELETE'])
def remove_rule_file(monitoring_id=None):
    if not _validate_monitoring_id(monitoring_id):
        return ("Not a valid monitoring_id"), 401

    if not _find_monitoring_id(monitoring_id):
        return ("Could not find ruleset for monitoring_id %s\n" % monitoring_id),  404

    if _unregister_rule_file(monitoring_id):
        if _reload_prometheus_configuration():
            return ("Updated Prometheus config with rules for monitoring id %s removed\n" % monitoring_id), 200
        else:
            return "Rule file was removed but config reload failed\n", 500
    else:
        return ("Rule file for monitoring id %s could not be deleted\n" % monitoring_id), 500
