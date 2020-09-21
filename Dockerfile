FROM ubuntu:18.04
RUN apt-get update && apt-get -y install sudo && apt-get -y install curl 

RUN sudo useradd --no-create-home --shell /bin/false prometheus

RUN sudo mkdir /etc/prometheus
RUN sudo mkdir /var/lib/prometheus

RUN sudo chown prometheus:prometheus /etc/prometheus
RUN sudo chown prometheus:prometheus /var/lib/prometheus

RUN curl -LO https://github.com/prometheus/prometheus/releases/download/v2.20.1/prometheus-2.20.1.linux-amd64.tar.gz

RUN tar xvf prometheus-2.20.1.linux-amd64.tar.gz

RUN sudo cp prometheus-2.20.1.linux-amd64/prometheus /usr/local/bin/

RUN sudo cp prometheus-2.20.1.linux-amd64/promtool /usr/local/bin/

RUN sudo chown prometheus:prometheus /usr/local/bin/prometheus

RUN sudo chown prometheus:prometheus /usr/local/bin/promtool

RUN sudo cp -r prometheus-2.20.1.linux-amd64/consoles /etc/prometheus

RUN sudo cp -r prometheus-2.20.1.linux-amd64/console_libraries /etc/prometheus

RUN sudo chown -R prometheus:prometheus /etc/prometheus/consoles

RUN sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries

RUN rm -rf prometheus-2.20.1.linux-amd64 prometheus-2.20.1.linux-amd64.tar.gz

COPY prometheus-config/prometheus.yml /etc/prometheus/prometheus.yml

RUN sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml

RUN mkdir -p /prometheus && chown -R nobody:nogroup etc/prometheus /prometheus

<<<<<<< HEAD
#RUN sudo -u prometheus /usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries
=======
#RUN sudo -u prometheus /usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries
>>>>>>> master
