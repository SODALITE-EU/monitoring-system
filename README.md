# SODALITE monitoring system. 

Monitoring system for the SODALITE project. This component is based in the Prometheus monitoring solution, and thus, this repository will contain configuration files and a explanation of how it is used in this project and its architecture. 

![Simple monitoring system schema.](https://github.com/SODALITE-EU/monitoring-system/blob/master/monitoring_system.png)

The monitoring system will be composed of two kinds of elements:
- Prometheus server, on charge of discovering monitored instances and gathering measurments from all different exporters. 
- Exporters, on charge of measuring their targeted metrics accross the SODALITE project infractructure. These exporters are a mix between widely used ones, such as Node Exporter and some created specifically for this project, such as the [IPMI exporter](https://github.com/SODALITE-EU/ipmi-exporter), [HPC exporter](https://github.com/SODALITE-EU/hpc-exporter), etc. 

## Software requirements.

For this component, the software requirements are the ones of [Prometheus](https://prometheus.io/docs/prometheus/latest/installation/). For the other components, their requirements are listed in their respective repositories. 

## Installation. 

We installed Prometheus in our system building it from source, so any online tutorial could be used (we recommend [this one](https://www.digitalocean.com/community/tutorials/how-to-install-prometheus-on-ubuntu-16-04), but making sure the download links get the latest version available). 

Once installed, the file ```prometheus.yml``` should be modified to fit the enviroment to be monitored and placed in its corresponding place. 

## Usage. 

Once installed and configured, its functioning does not differ from any Prometheus installation. For the rest of the monitoring components, visit their respective docs. 