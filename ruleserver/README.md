# Rule files management server

Server for adding/removing both recording and alerting rule files from the Prometheus server.  

## Installation

### Stack-integrated

### Single container

## Usage

### API for add/remove rule files

This server offers a simple API composed of two kinds of requests:

#### Add request
`curl --data-binary @rule-file-to-add.yml http://<ruleserver_ip>:<port>/rules/add/<file-id>`

After this request, the server copies the contents of `rule-file-to-add.yml` into a file named `rules-<file-id>.yml` and stores it into a Docker volume shared with the Prometheus component. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it.

#### Remove request
`curl http://<ruleserver_ip>:<port>/rules/remove/<file-id>`

After this request, the server looks for a file named `rules-<file-id>.yml` in the Docker volume shared with the Prometheus component and removes it if found. The server forces the configuration of the Prometheus instance to reload by sending a SIGHUP signal to it.
