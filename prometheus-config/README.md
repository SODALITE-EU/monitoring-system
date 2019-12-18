# SODALITE's Prometheus configuration file

This file contains several configuration files used to define the behavior of Prometheus. The ``prometheus.yml`` file defines what and how Prometheus monitors the required metrics. 

One of the main parts of the file is the specification of how Prometheus discovers and monitors freshly created Openstack instances. In addition, it also contains the required information to monitor Skydive, the custom exporter, etc. 