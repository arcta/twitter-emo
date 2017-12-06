#!/bin/bash

########################################################################
# install kafka with dependencies
########################################################################
sudo apt install --yes zookeeperd
sudo systemctl status zookeeper

if [ "$(which sbt)" != "" ]; then
    echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
    sudo apt-get update
    sudo apt-get install --yes sbt
fi

sudo adduser --system --no-create-home --disabled-password --disabled-login kafka
wget http://www-us.apache.org/dist/kafka/1.0.0/kafka_2.11-1.0.0.tgz
#curl http://kafka.apache.org/KEYS | gpg --import
#wget https://dist.apache.org/repos/dist/release/kafka/1.0.0/kafka_2.11-1.0.0.tgz.asc
#gpg --verify kafka_2.11-1.0.0.tgz.asc kafka_2.11-1.0.0.tgz

sudo mkdir /opt/kafka
sudo tar -xvzf kafka_2.11-1.0.0.tgz --directory /opt/kafka --strip-components 1
rm kafka_2.11-1.0.0.tgz kafka_2.11-1.0.0.tgz.asc
sudo nano /opt/kafka/config/server.properties
sudo chown -R kafka:nogroup /opt/kafka

########################################################################
# Attention: depends on the environment
# SIGTERM may or may not be OK (SuccessExitStatus=143)
########################################################################
sudo tee /etc/systemd/system/kafka.service <<EOF
[Unit]
Description=High-available, distributed message broker
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
ExecStop=/opt/kafka/bin/kafka-server-stop.sh
Restart=on-failure
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable kafka.service
sudo systemctl start kafka
sudo systemctl status kafka
