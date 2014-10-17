# -*- mode: ruby -*-
# vi: set ft=ruby :
require('time')

# Have servi give all config params
json_config = `servi -v0 utils --combined_rendered_servifile`
extra_vars = JSON.parse(json_config)
# require('pp') ; print(PP.pp(extra_vars)) ; abort('Debugging')

extra_vars["IS_VAGRANT"] = true
host_vars = extra_vars["HOSTS"]["vagrant"]["vars"]

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    if ENV['servi_box'].to_s.empty?
        config.vm.box = "ubuntu/trusty64"
        config.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64"
    else
        # 'servi_box' environment variable is not empty
        # This is set by 'servi usebox'.
        print "**************************\n"
        print "Using servi_box: "+ENV['servi_box']+"\n"
        print "**************************\n\n"
        config.vm.box = ENV['servi_box']
    end
    
    config.vm.hostname = host_vars["HOST_NAME"]

    config.vm.network "private_network", ip: extra_vars["STATIC_IP"]
    config.ssh.guest_port = 22

    config.vm.provider "virtualbox" do |v|
      v.memory = 512  # wordpress: 1024
      v.cpus = 2
      v.name = host_vars['HOST_NAME']+'_'+Time.now.utc.iso8601
    end
    
    config.vm.synced_folder "apache_config/sites-available", "/etc/apache2/sites-available", create: true,
        owner:  extra_vars["WEBDEV_UID"], group:  extra_vars["WEBDEV_GID"], mount_options: ["dmode=775","fmode=664"]
    config.vm.synced_folder  extra_vars["LOCAL_DIR"], "/var/www/#{ extra_vars['SITE_SUFFIX']}", create: true,
        owner:  extra_vars["WEBDEV_UID"], group:  extra_vars["WEBDEV_GID"], mount_options: ["dmode=775","fmode=664"]
    
    config.vm.provision "ansible" do |ansible|
        #ansible.verbose =  "vvvv"
        ansible.inventory_path = `which servi_inventory`.strip
        ansible.limit = "vagrant"
        ansible.playbook = "ansible_config/playbook.yml"
    end
end
