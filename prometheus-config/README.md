# SODALITE's Prometheus configuration file

This file contains several configuration files used to define the behavior of Prometheus. The ``prometheus.yml`` file defines what and how Prometheus monitors the required metrics. 

One of the main parts of the file is the specification of how Prometheus discovers and monitors freshly created Openstack instances. In addition, it also contains the required information to monitor Skydive, the custom exporter, etc. 

The Prometheus config file found in the main folder is only used for the docker deployments, while this one is used for Openstack deployments.