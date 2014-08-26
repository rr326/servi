# -*- mode: ruby -*-
# vi: set ft=ruby :


# Configuration parameters for Vagrant and Ansible
# IMPORTANT: you must define these here AND in ansible_config/playbook.yml
# because you may run the ansible playbook without Vagrant.
WEBDEV_UID=1100
WEBDEV_GID=900
LOCAL_DIR="src"
REMOTE_DIR="/var/www/weather"
REMOTE_LOG_DIR="/var/log/apache2/weather"
STATIC_IP="192.168.10.10"  # Note - add this to /etc/hosts


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64"


    # Static ip. Add to /etc/hosts to assign a name (like xxx.dev)
    config.vm.network "private_network", ip: STATIC_IP

    config.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
    end


    # File sharing - point to my development folder
    config.vm.synced_folder "apache_config/sites-available", "/etc/apache2/sites-available", create: true,
        owner: WEBDEV_UID, group: WEBDEV_GID, mount_options: ["dmode=775","fmode=664"]
    config.vm.synced_folder LOCAL_DIR, REMOTE_DIR, create: true,
        owner: WEBDEV_UID, group: WEBDEV_GID, mount_options: ["dmode=775","fmode=664"]

    # Run ansible with playbook.yml (next to Vagrantfile)
    config.vm.provision "ansible" do |ansible|
        ansible.extra_vars = {
            is_vagrant: true,
            apache_log_dir: REMOTE_LOG_DIR
        }
        ansible.playbook = "ansible_config/playbook.yml"
        # ansible.verbose = "vvvv"
    end

end
