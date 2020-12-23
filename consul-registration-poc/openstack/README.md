# OpenStack Prometheus+Consul+Exporter PoC

Here you can find the blueprints and playbooks needed to deploy in the testbed using xOpera:

1. The [Consul instance](consul-server) needed to register Prometheus-valid exporters as services
1. A [Prometheus instance](prometheus-server) able to discover on-the-fly any Prometheus-valid exporter registered on Consul
1. An [automagically monitored VM](node-exporter): its creation playbook includes additional tasks for installing a Prometheus node-exporter and registering it as a service into the Consul server
