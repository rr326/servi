#TODO

1. P0

1. P1
    * SSL
    * /etc/cron.daily/apt: Package 'resolvconf' has conffile prompt and needs to be upgraded manually
        http://askubuntu.com/questions/104899/make-apt-get-or-aptitude-run-with-y-but-not-prompt-for-replacement-of-configu

1. P2

1. P3
    * Renderservifiles - have host name field and have it import that data
        * eg: servi utils -r vagrant
    * Add config check - make sure I have all parameters expected
    * Templates
        * Remove static ips? (and use that tool that does *.dev?)


## Documentation after init
    * etc/hosts
    * Modify Servifile.yml
    * Whatever your 'sitesuffix' is, make sure you create sitesuffix.conf in apache
    * vagrant reload
    * vagrant provision


## Instructions
(not verified)

    mkdir serviplate
    cd serviplate
    servi init .
    echo 'Edit Servifile.yml'
    subl Servifile.yml
    echo 'Edit /etc/hosts'
    subl /etc/hosts
    echo 'Copy sample apache config then edit'
    cp apache_config/sites-available/mysite.conf apache_config/sites-available/serviplate.conf
    subl apache_config/sites-available/serviplate.conf
    echo 'build box (not necessary, but good for future servi installs)'
    servi buildbox
    echo 'now use box (which will also do a vagrant provision)'
    servi usebox
    servi pushto <host>
    echo 'You are up! Now check out your new site: http://<whateverurlyouputin /etc/hosts>'
    echo 'now modify ansible_config/roles/projectSpecific/* to set up your server for your specific project'
    echo 'ROSS>> Also add everything to git'

    Also talk about setting up the intial box (eg: Dig ocean)
        * SSH (root)
        * Create orig user (and set up ssh)
        * Sudoers
        * brew install rsync, rsync --version
        * export PATH=$PATH (use new rsync)

## Instructions for a new server
ssh -i ~/.ssh/rrosen326_rsa -l root
useradd -m -G sudo rrosen326
visdo
    (Change this line to add 'NOPASSWD')
    %sudo   ALL=(ALL:ALL) NOPASSWD:ALL
cd /home/rrosen326
mkdir .ssh
cd .ssh
nano authorized_keys
    Copy your public key here
Test it:
ssh -i ~/.ssh/rrosen326_rsa -l rrosen326
sudo ls /  # No password should be asked
