# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

$provision = <<SCRIPT
#!/usr/bin/env bash
set -eu

apt-get update
apt-get install -y -q python-dev \
                      rabbitmq-server \
                      debconf-utils

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password ruthpasswort'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password ruthpasswort'
sudo apt-get -y install mysql-server \
                        libmysqlclient-dev

cat << "EOF" | mysql -uroot -pruthpasswort
DROP DATABASE IF EXISTS tasker;
GRANT ALL ON *.* TO 'tasker'@'%';
DROP USER 'tasker'@'%';

CREATE database tasker;
CREATE USER 'tasker'@'%' IDENTIFIED BY '#{ENV["MYSQL_PASSWD"]}';
GRANT ALL ON tasker.* TO 'tasker'@'%';
FLUSH PRIVILEGES;
EOF

rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart

cd /vagrant
python bootstrap.py
./bin/buildout
./bin/initialize -d -r
./bin/supervisord

sleep 3
./bin/supervisorctl status
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "apidev"
  config.ssh.forward_agent = true
  config.vm.network "forwarded_port", guest: 8888, host: 8888
  config.vm.provision "shell", inline: $provision
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
end
