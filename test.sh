#! /usr/bin/env zsh

rm /Users/rrosen/dev/serviplate/requirements*
echo '{"template_version" : "2.0.0"}' > /Users/rrosen/dev/serviplate/template_version.json
echo 'CHANGED' >> /Users/rrosen/dev/serviplate/Vagrantfile
rm /Users/rrosen/dev/serviplate/apache_config/sites-available/THISSITE.conf 
echo 'test.sh done' 
echo

