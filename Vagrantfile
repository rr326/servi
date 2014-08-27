# -*- mode: ruby -*-
# vi: set ft=ruby :

# Configuration variables in server_vars.yml
require 'yaml'
vars = YAML.load_file 'server_vars.yml'
vars["IS_VAGRANT"] = true

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64"

    config.vm.hostname = vars["HOST_NAME"]


    # Static ip. Add to /etc/hosts to assign a name (like xxx.dev)
    config.vm.network "private_network", ip: vars["STATIC_IP"]

    config.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
    end


    # File sharing - point to my development folder
    config.vm.synced_folder "apache_config/sites-available", "/etc/apache2/sites-available", create: true,
        owner: vars["WEBDEV_UID"], group: vars["WEBDEV_GID"], mount_options: ["dmode=775","fmode=664"]
    config.vm.synced_folder vars["LOCAL_DIR"], vars["REMOTE_DIR"], create: true,
        owner: vars["WEBDEV_UID"], group: vars["WEBDEV_GID"], mount_options: ["dmode=775","fmode=664"]

    # Run ansible with playbook.yml (next to Vagrantfile)
    config.vm.provision "ansible" do |ansible|
        ansible.extra_vars = {
            is_vagrant: vars["IS_VAGRANT"],
        }
        ansible.playbook = "ansible_config/playbook.yml"
        # ansible.verbose = "vvvv"
    end

end
