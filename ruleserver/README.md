# Rule files management server

Server for adding/removing both recording and alerting rule files from the Prometheus server.  

## Deployment
This component is expected to be deployed [(see the blueprint)](https://github.com/SODALITE-EU/iac-platform-stack/blob/e3a7579862910e2cdaa508e69829baf1b0a39271/docker-local/service.yaml#L652) along with Consul, Prometheus and Alertmanager components.

If you want to deploy this component as a standalone Docker container for research or debug purposes, you must provide the `docker run <image>` command with the following additional parameters:
* Volumes (`-v "rules-volume:/etc/prometheus/rules"`): When deployed inside the stack, the rule server shares the `/etc/prometheus/rules/` folder of the Prometheus instance through a Docker volume. The Flask app implementing the API expects such a folder to be available in the rule server filesystem:  
* Environment variables (`--env`):
  * `GUNICORN_WORKERS`: Number of threads managed by the Gunicorn WSGI server
  * `RULESERVER_PORT`: Listening port of the server for the add/remove requests

## Usage

### Rule file example

This is an example of a file defining a rule that triggers an alert when the CPU load of a host is over the 80% during more than 5 minutes.
```
groups:
- name: alert.rules
  rules:
  - alert: HostHighCpuLoad
    expr: 100 - (avg by(instance,os_id) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Host high CPU load (instance {{ $labels.instance }})"
      description: "CPU load is > 80%\n  VALUE = {{ $value }}\n  LABELS: {{ $labels }}"
```
You can get more information about [alerting rules for Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) in its documentation website.

### API for add/remove rule files

This server offers a simple API composed of two kinds of requests:

#### Add request
`curl --data-binary @rule-file-to-add.yml http://<ruleserver_ip>:<port>/rules/add/<file-id>`

After this request, the server copies the contents of `rule-file-to-add.yml` into a file named `rules-<file-id>.yml` and stores it into a Docker volume shared with the Prometheus component. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it.

#### Remove request
`curl http://<ruleserver_ip>:<port>/rules/remove/<file-id>`

After this request, the server looks for a file named `rules-<file-id>.yml` in the Docker volume shared with the Prometheus component and removes it if found. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it .
