# Servi

Servi helps developer build *production* quality environments, easily and quickly. And you can then mirror your production environment for development, ensuring that when you push to production, everything works.


## What it is
Servi is mostly a bunch of Ansible templates, integrated with a Vagrant setup, and a few command line tools for making it easier for you to use. It has baked-in assumptions and best[1]-practices. 

It's a little like Yeoman, for a simple production-quality environment.
        

## Who is it for
Developers who build 2+ small sites (single-server) or hobby projects. If your needs are more complicated, servi probably won't help much.


## Motivation
Let's say you want to build a website for yourself, for your company, or for a client. You can scaffold out a project instantly with Yeoman. You can spin up a simple virtual machine with Vagrant. You can get it all working pretty simply and quickly.  Damn, you're good.

Ok, let's push this baby out. $5 for a hosted server. Sweet.  Let's push our code up there. 

Oh wait. I probalby need to secure my server, since badguys abound. Let's google 'Ubuntu hardening'.  Woa - there's a lot of stuff to do! Ok, go down the list.  Oh wait - let's install Apache. Oh, and let's harden that a bit. Woa - another long list!  What about getting my email setup so I get notified of problems? Another search and setup routine. What if I start running out of diskspace? Another setup. What about setting up my standard zsh environment? Some more stuff.  You get the picture.

Then, let's say you want to spin up a different project.  Do you just copy a snapshot and move build from there? What if this is a different client. Are you SURE your previous image is clean? And what about all the cruft that accumulated as you added and removed things? Wouldn't it be nice to start from scratch?

So that's basically the idea behind servi.  Build a production-quality, reasonably hardened server setup. Make it work easily in with your development setup. Make it easy to modify your core template files and update your projects. Keep everything in your VCS. 


## Disclaimer
Ideally, servi should be written by team of experts who know how to build a good server and know best practices. But unfortunately those guys are busy writing kernals, or developing frameworks, or whatever it is they do.  Instead, it's written by a guy without all that excellent background. So I did my best with a lot of google searching, but I'm sure I missed things or made dumb decisions. Luckily all the ansible templates are super easy to read, so go ahead and clean them up and improve them. (And send me a pull request!)

## Example
Set up a new project and get it running locally (on a virtual machine)

    mkdir myproject
    cd myproject
    servi init .
    <edit ~/Servifile_globals.yml and ./Servifile.yml>
    <add static ip to /etc/hosts>
    vagrant up
    <browser: goto static ip - woa - hello world is running!>
    
Ok - now let's go live.  You need to set up a cloud server with JUST enough configuration to allow ansible to talk to it (ssh key, main account, authorized_keys, and passwordless sudo)

    servi rans <host_name>
   
Browser: goto host_name, and you are up!  And you know it works, since it worked locally.

Ok, now lets modify our templates.
    
    cd <my fork of servi>
    <edit servi_templates/*>
    
    cd myproject
    servi update
    
    vagrant provision
    <now my local machine is updated.>
    
    servi rans <host_name>
    <now your remote machine is updated>
    

## Details
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
