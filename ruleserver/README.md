# Rule files management server

Server for adding/removing both recording and alerting rule files from the Prometheus server.  

## Deployment
This component is expected to be deployed [(see the blueprint)](https://github.com/fabeirojorge-sw/iac-platform-stack/blob/f1d61d3c0c4563f7858e226fa096ac51d748860e/docker-local/service.yaml#L489) along with Consul, Prometheus and Alertmanager components.

If you want to deploy this component as a standalone Docker container for research or debug purposes, you must provide the `docker run <image>` command with the following additional parameters:
* Volumes (`-v "rules-volume:/etc/prometheus/rules"`): When deployed inside the stack, the rule server shares the `/etc/prometheus/rules/` folder of the Prometheus instance through a Docker volume. The Flask app implementing the API expects such a folder to be available in the rule server filesystem:  
* Environment variables (`--env`):
  * `GUNICORN_WORKERS`: Number of threads managed by the Gunicorn WSGI server
  * `RULESERVER_PORT`: Listening port of the server for the add/remove requests

## Usage

### API for add/remove rule files

This server offers a simple API composed of two kinds of requests:

#### Add request
`curl --data-binary @rule-file-to-add.yml http://<ruleserver_ip>:<port>/rules/add/<file-id>`

After this request, the server copies the contents of `rule-file-to-add.yml` into a file named `rules-<file-id>.yml` and stores it into a Docker volume shared with the Prometheus component. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it.

#### Remove request
`curl http://<ruleserver_ip>:<port>/rules/remove/<file-id>`

After this request, the server looks for a file named `rules-<file-id>.yml` in the Docker volume shared with the Prometheus component and removes it if found. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it.