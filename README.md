<img align="right" src="img/servi_small.png?raw=true" style="position: relative; z-index: 1000;">

# Servi

Servi helps developers build *production* quality environments, easily and quickly. And you can then mirror your production environment for development, ensuring that when you push to production, everything works.

## What it is 
Servi is mostly a bunch of Ansible templates, integrated with a Vagrant setup, and a few command line tools for making it easier for you to use. It has baked-in assumptions and best-practices. 

It's a little like [Yeoman](http://yeoman.io/), but for setting up your server.


## Who is it for
Developers who build single-server sites or hobby projects. If your needs are more complicated, servi probably won't help much.


## Motivation
Let's say you want to build a website for yourself, for your company, or for a client. You can scaffold out a project instantly with Yeoman. You can spin up a simple virtual machine with Vagrant. You can get it all working pretty simply and quickly.  Damn, you're good.

Ok, let's push this baby out. $5 for a hosted server. Sweet.   

Oh wait. I probalby need to secure my server, since badguys abound. Let's google 'Ubuntu hardening'.  Woa - there's a lot of stuff to do! Ok, go down the list.  Oh wait - let's install Apache. Oh, and let's harden that a bit. Woa - another long list!  What about getting my email setup so I get notified of problems? Another search and setup (and debug!) routine.  What about getting notified if I run out of disk space? Another setup. What about setting up my standard zsh environment? Some more stuff.  You get the picture.

Then, let's say you want to spin up a different project.  Do you just copy a snapshot and build from there? What if this is a different client. Are you SURE your previous image is clean? And what about all the cruft that accumulated as you added and removed things? Wouldn't it be nice to start from scratch?

So that's basically the idea behind servi.  Build a production-quality, reasonably hardened server setup. Make it work easily in with your development setup. Make it easy to modify your core template files and update your projects. Keep everything in your VCS. 

BTW - here's a good article (with a ninja squirrel!) on why it's useful to use something like Ansible instead of doing it manually: [article](https://devopsu.com/blog/ansible-vs-shell-scripts/).  Though don't believe him that it's that easy - I've spent a LOT of time debugging Ansible-based problems!


## Disclaimer
Ideally, servi should be written by team of experts who know how to build a good server and know best practices. But unfortunately those guys are busy writing kernals, or developing frameworks, or whatever it is they do.  Instead, it's written by a guy without all that excellent background who still needed to set up some servers. So I did my best with a lot of google searching, but I'm sure I missed things or made dumb decisions. Luckily all the ansible templates are super easy to read, so go ahead and clean them up and improve them. (And send me a pull request!)

## Example
Set up a new project and get it running locally (on a virtual machine)

    $ mkdir myproject
    $ cd myproject
    $ servi init .
    # <edit ~/Servifile_globals.yml and ./Servifile.yml>
    # <add static ip to /etc/hosts>
    $ vagrant up
    # <browser: goto static ip - woa - hello world is running!>
    
Ok - now let's go live.  You need to set up a cloud server with JUST enough configuration to allow ansible to talk to it (ssh key, main account, authorized_keys, and passwordless sudo)

    $ servi rans <host_name>
   
Browser: goto host_name, and you are up!  And you know it works, since it worked locally.

Ok, now lets modify our templates.
    
    $ cd <my fork of servi>
    # <edit servi_templates/*>
    
    $ cd myproject
    $ servi update
    
    $ vagrant provision
    # <now my local machine is updated.>
    
    $ servi rans <host_name>
    # <now your remote machine is updated>
    

## Yet another framework?
NO! It's not a framework. It's mostly a comprehensive set of ansible templates. It's a little Vagrantfile.  Then there are two configuration files (Servifile_globals.yml and Servifile.yml).  These both get stored in your repo and are read directly by Ansible or Vagrant - so your project is complete. Want to walk away from servi? You're already done.

The servi tools just help you use all the templates, but they aren't necessary. Each of your projects is complete and servi-less*. 

*There is one complication - although I copy your ~/Servifile_globals.yml to your repo for tracking, I still read from ~. So to truly remove servi you'd just copy everything in Servifile_globals into your projects Servifile.yml. 


## Help?
Imagine a world where a novice could spin up a complete, secure, well-designed production server at the touch of a button.  Help make it so!  

I think servi could go from 'kinda cool' to 'totally awesome' with very little effort. I just need help putting the "best" in "best practices".  If you're an expert at linux or apache ops, please send feedback my way. (Actual pull requests would be better, but I'll take what I can get.)

## What's inside
* Ansible templates
    (These are only some of the configurations)
    * Ubuntu 14.04
    * Ssh
        * authorized_key set and no password auth
        * No root login
    * Automatic upgrades
    * Fail2ban
    * Main webdev user & group & permissions
    * passwordless sudoers
    * Postfix (out only)
    * UFW firewall
    * Apache setup and moderately hardened
    * Google pagespeed
    * logrotate for all /var/www/*
    * simple Monit monitoring for CPU, disk space, memory
    * Sublime text tunneling (type 'subl xxx' to open remote xxx in local     sublime)
    * Main user account with base .zshrc
    * Python virtualenvs for python 2 & 3
* Vagrant setup
    * Integrated - "vagrant up" and your production environment is now running locally
* Configuration
    * Global - ~/Servifile_globals.yml - config shared across all your servi projects
    * Project specific - ./Servfifile.yml - local to a project. Can override any global configuration
    * Passwords - set your passwords, keyfiles, etc. as environment variables and then look them up in a Servifile or ansible template: MAIN_RSA_KEY_FILE: "{{ lookup('env', 'MY_CRED_FILE') }}" 
* Main tools
    * init - copy base templates to your local directory
    * update - update existing proejct with any changes made to your templates
    * diff - diff your project with your templates
    * inventory - A dynamic inventory script used by ansible (it reads your Servifile configuration)   
* Convenience tools
    These aren't really necessary, but make using servi easier.
    * copy - copy a template file to your master location
    * lans - Local Ansible - run an ansible playbook (or all) on your local (/vagrant) machine
    * rans - Remote Ansible - run it on a remote host. These just set a lot of command line arguments ansible needs.
    * pushto - push your code to host X - With vagrant, it shares a local folder. With a production server, you need to push your code. This is a thin wrapper on rsync to make it easy.
    * usebox / buildbox - Most of your configuration is global, so you can build a vagrant base box and then use it for future projects to save time on the first provisioning.
    * utils --render_servifile - Read your configuration files and do any lookups, displaying the results. Helpful for debugging.
    * pre-commit-hook.git - Add to your repo to make sure you have a copy of your Servifile_globals.yml locally and an updated version of your servi_data.json manifiest

## Installation instructions
* [Install Ansible](http://docs.ansible.com/intro_installation.html)
* [Install Vagrant](https://docs.vagrantup.com/v2/installation/)
* Confirm Python 3.4
    * `python 3 --version` 
    * if < 3.4, then [upgrade your python](https://www.python.org/download/)
* [Fork servi](https://github.com/rr326/servi/fork)
    * You really want to fork servi (instead of cloning), since it is highly likely you will want to tweak your base templates and keep them in git.
    * If you've never forked, it's a piece of cake. [Github fork a repo](https://help.github.com/articles/fork-a-repo/)
* Clone your forked repo. eg: `git clone https://github.com/YOUR-USERNAME/servi`
* Install servi  
 Note - it is important to install with the 'develop' option below so that when you change your templates, any `servi xx` command will use your changed files.
    
     cd <your local forked directory>
     python3 setup.py develop  
* Test it
    * Step 1 - initialize
    
            $ mkdir mysite
            $ cd mysite
            $ servi init .
    * Step 2 - configure
        * Edit ~/Servifile_globals.yml
        * For now, don't worry about most. Just modify this one:  
        `MAIN_RSA_KEY_FILE: <path to your rsa key>`
        
    * Step 3 - Up!
        
            $ vagrant up
            $ sudo echo "192.168.10.9    mysite.dev" >> /etc/hosts
            # Make sure the below file exists and is your correct key
            $ export MY_CRED_FILE="~/.ssh/id_rsa.pub" 
            $ export MY_UN="<your username here>"
            $ curl mysite.dev  # Should see Hello, world!
            $ curl mysite.dev/flask  # Should see Hello, world!    
* Upgrade rsync (optional)
    * If you want to use `servi pushto` you need a current version of rsync. On a mac, do `brew upgrade rsync`

## Usage Instructions
After you've installed and confirmed everything is working, it's time to set servi up for your needs.

Note - to use servi effectively, you'll need to become fairly adept at Ansible.  Ansible isn't hard, it does take some time and getting used to. (And debugging!) [Ansible Docs](http://docs.ansible.com/)

### Passwords
Servi will need some passwords. You can certainly hardcode them into the Servifiles, but that's not a great idea.  Here's how I do it:

* In ~/.zshenv
     
        if [[ -r ~/.pwrc ]]; then
            . ~/.pwrc
        fi
* In ~/.gitignore_global

        .pwrc
    
* In ~/.pwrc (NOT part of any vcs repo!)

        export MY_UN='xxxx'
        export MY_CRED_FILE='<pathto ssh_rsa.pub>'
        export MY_GMAIL_UN='xxxx@gmail.com'
        export GMAIL_PW="xxxx"
        export MONIT_PW="xxx"
        export mysql_root_db_pass="xxxxxxx"
        export mysql_admin_un="xxxx"
        
### Initial configuration
Servi uses two configuration files:

1. ~/Servifile_globals.yml
2. <projectdir>/Servifile.yml

These Servifiles hold configuration for servi, ansible, and vagrant.  So anything you put in a Servifile is accessable from all three.  It turns out this is extremely handy.

Note that anything in the project Servifile overwrites a similar variable in Servifile_globals. The one exception is that dictionaries are additive - so if in globals you have `{HOSTS: {host1: ...}}` and in the project you have `{HOSTS: {vagrant: ...}}`, both 'host1' and 'vagrant' are in the dictionary.

The Servifiles are pretty self-explanatory and well-commented.  Edit them. 

### Test your configuration
Before you start customizing your project, make sure it all still works. Follow the 'Test it' steps above (under Installation instructions).

If it doesn't work, the first thing to test is if your configuration is turning out the way you think it is. Run `servi utils -r` to render your Servifiles.  Read the results carefully - are you getting what you think you should be getting?

### Customizing a project
Now that you've edited your configuration and tested it, let's customize it.

1. apache_config/sites_available/mysite.conf  
    1. Copy this to a new conf file (you'll delete the other one after everything works)
    1. Modify
1. ansible_config/roles/projectSpecific/*
    1. This is the main location to add project-specific configuration.
    1. If the project requires roles not in your main playbook, add [role dependencies](http://docs.ansible.com/playbooks_roles.html#role-dependencies) in meta/main.yml     
1. ansible_config/playbook.yml
    1. This is the main driver of ansible.
    1. Ideally you shouldn't have to modify this for a project. Instead, modify this globally (as part of your servi fork directory) and it will be part of all your servi projects.
    
### Customizing the servi (ansible) templates
I've done my best to create a solid, complete server, but you'll probably want to modify my choices.

1. ansible_config/*  
   This is where it all happens. You'll want to look through all of it and make the appropriate changes. EG:
   * playbook.yml - put new top-level roles here. Use ruby instead of python? Create a ruby role and remove teh python one. (No need to remove the python one from the repository - it won't get copied to your projects unless it is included in playbook.yml) Also, remove 'sampleFlask' - you don't want to have to delete that every time.
   * roles/hardenedApache - my sites are not very valuable so I didn't do any DDoS hardening.  Also modify templates/apache2.conf for globall config
   * rols/mainAccount/files/.zshrc - this is a pretty vanilla .zshrc. Put your own here. (or switch to bash if you prefer)
1. apache_config/sites_available/mysite.conf  
   Put your default virtual host config here
   
### Customizing servi itself
You probably don't need to do this, but it's easy to if you want to. You just need to know python 3.  Then look in servi/command.py to see how the simple plugin system works. And please add unit tests to the tests folder. (If you haven't used pytest, it's super easy, especially now that it's set up to run.)    

