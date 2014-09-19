#! /usr/bin/env zsh

rm /Users/rrosen/dev/serviplate/requirements*
echo '{"template_version" : "2.0.0"}' > /Users/rrosen/dev/serviplate/servi_data.json
echo 'CHANGED' >> /Users/rrosen/dev/serviplate/Vagrantfile
rm /Users/rrosen/dev/serviplate/apache_config/sites-available/THISSITE.conf 
echo 'CHANGED' >> /Users/rrosen/dev/serviplate/ansible_config/roles/projectSpecific/tasks/main.yml
echo 'CHANGED' >> /Users/rrosen/dev/serviplate/ansible_config/roles/baseUbuntu/tasks/main.yml
echo 'test.sh done' 
echo

