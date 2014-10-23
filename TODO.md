#TODO

# Instructions for a new server
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








## TODO
* Unused roles needs to trace dependencies!
    - eg: myssqlSetup uses mysql
* Unused roles more (or less!) clever role search (eg: {role: xx, data:yy})
* Update - remove cleverness and just do a simple diff?

* Renderservifiles - have host name field and have it import that data
    * eg: servi utils -r vagrant
* SSL

* Add config check - make sure I have all parameters expected

* Servi
    * Add stats for init and update
    * Get -f/-v to work on either side of command
* Templates
    * Remove static ips? (and use that tool that does *.dev?)
* Vagrant - append VAGRANT to hostname

* /etc/cron.daily/apt: Package 'resolvconf' has conffile prompt and needs to be upgraded manually
    http://askubuntu.com/questions/104899/make-apt-get-or-aptitude-run-with-y-but-not-prompt-for-replacement-of-configu


* Backups - is it making unnecessary backups?

* Documentation after init
    * etc/hosts
    * Modify Servifile.yml
    * Whatever your 'sitesuffix' is, make sure you create sitesuffix.conf in apache
    * vagrant reload
    * vagrant provision

* Testing
    * Update 'update' and other tests to fully test the warning logic(ie: what is actually printed)

* Monit:
    * When initialized, it sends an apache warning (should be off on Vagrant)
    * Getting chron error (see below) - Is this current or old?

# Instructions
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

# Monit error
    ---------- Forwarded message ----------
    From: <rrosen326@gmail.com>
    Date: Wed, Oct 8, 2014 at 5:39 AM
    Subject: monit alert -- Does not exist apache
    To: rrosen326@gmail.com


    Does not exist Service apache

            Date:        Wed, 08 Oct 2014 12:39:15
            Action:      restart
            Host:        serviplate.xx.com
            Description: process is not running

    Your faithful employee,
    Monit


# Chron error
    THIS IS A WARNING MESSAGE ONLY.

    YOU DO NOT NEED TO RESEND YOUR MESSAGE.

    Delivery to the following recipient has been delayed:

         root@xx.com

    Message will be retried for 2 more day(s)

    Technical details of temporary failure:
    The recipient server did not accept our requests to connect. Learn more at http://support.google.com/mail/bin/answer.py?answer=7720
    [(0) xx.com. [69.172.201.208]:25: Connection timed out]

    ----- Original message -----

    DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
            d=gmail.com; s=20120113;
            h=from:to:subject:content-type:message-id:date;
            bh=+fzia+p2wkrgScNRbD3Sp6ogj+9pUfxByJvqt5+OoE4=;
            b=GEk8GbRhb/10ZD4XOhH4tfLKncfoNrQ7K7bNAH9G/2o3UlO8j8TP1l5GxLtFyiiezz
             1Ymbcpyexbz1/z3pCADTzll6dchLDfJM78hDGGEmXfGn2xqwgjBveFEDHOHhRT1UF7Fs
             24WMbdJnxVTin++YnJ/VXsseK0O99/sxCv43i4n1qrhZ2hwyGq+3itmpN5GjSil1LpTY
             EQYtyl98oJJubak/wzo7S/MmbJXmEQ8roMc0hH3CWgimd8qtoA4fQ48yaFZ7xf8R/Avd
             fkeH38WoCW4CKbqYDDX6q2R8UwjLfjPNba4bZcT+R2CfT6555C20mr6SpLGbawLSvMcy
             DPrQ==
    X-Received: by 10.70.42.47 with SMTP id k15mr1999357pdl.79.1412663202767;
            Mon, 06 Oct 2014 23:26:42 -0700 (PDT)
    Return-Path: <rrosen326@gmail.com>
    Received: from serviplate.xx.com (c-76-121-170-6.hsd1.wa.comcast.net. [76.121.170.6])
            by mx.google.com with ESMTPSA id ei1sm14948541pbd.46.2014.10.06.23.26.41
            for <root@xx.com>
            (version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);
            Mon, 06 Oct 2014 23:26:42 -0700 (PDT)
    From: Cron Daemon <rrosen326@gmail.com>
    X-Google-Original-From: root@xx.com (Cron Daemon)
    Received: by serviplate.xx.com (Postfix, from userid 0)
            id 3A1F5211BE; Tue,  7 Oct 2014 06:26:36 +0000 (UTC)
    To: root@xx.com
    Subject: Cron <root@serviplate2> test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
    Content-Type: text/plain; charset=ANSI_X3.4-1968
    X-Cron-Env: <SHELL=/bin/sh>
    X-Cron-Env: <PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin>
    X-Cron-Env: <HOME=/root>
    X-Cron-Env: <LOGNAME=root>
    Message-Id: <20141007062636.3A1F5211BE@serviplate.xx.com>
    Date: Tue,  7 Oct 2014 06:26:36 +0000 (UTC)

    /etc/cron.daily/apt:
    verbose level 1
    system is on main power.
    sleeping for 51 seconds
    system is on main power.
    check_stamp: interval=86400, now=1412640000, stamp=1412294400, delta=345600 (sec)
    apt-key net-update (failure)
    download updated metadata (success).
    send dbus signal (success)
    check_stamp: interval=0
    download upgradable (not run)
    check_stamp: interval=86400, now=1412640000, stamp=1412294400, delta=345600 (sec)
    Package 'resolvconf' has conffile prompt and needs to be upgraded manually
    unattended-upgrade (success)
    check_stamp: interval=0
    autoclean (not run)
    aged: ctime <30 and mtime <30 and ctime>2 and mtime>2
    end remove by archive size: size=124164 < 512000

# Servi usebox errors

    --> servi -v4 usebox                                                                                                                                                    [master]
    Servi - Running: usebox

    Master Directory: /Users/rrosen/dev/berkeley
    Template Directory: /Users/rrosen/dev/servi/servi_templates

    ***** ERROR *****
    Existing saved servi_box has a version less than existing template version.
    Either run "servi buildbox" or run "servi usebox --force."
    Template version: 0.1.24
    servi_box: servi_box_0_0_0.box
    Use -f / --force to override.

    **Servi Aborting**

    ***** ERROR *****
    Existing saved servi_box has a version less than existing template version.
    Either run "servi buildbox" or run "servi usebox --force."
    Template version: 0.1.24
    servi_box: servi_box_0_0_0.box
    Use -f / --force to override.

    **Servi Aborting**
    .-(~/dev/berkeley)--------------------------------------------------------------------------------------------------------------------------------------------(rrosen@RossMacbook)-
    `--> servi update                                                                                                                                                        [master]
    Servi - Running: update

    Master Directory: /Users/rrosen/dev/berkeley
    Template Directory: /Users/rrosen/dev/servi/servi_templates

    Warning
    The following files from the template were changed but
    are on your SERVI_IGNORE_FILES list and will not be updated:
    ['Servifile.yml', 'ansible_config/roles/projectSpecific/tasks/main.yml']

    Updating repository with Servi template version: 0.1.24
    .-(~/dev/berkeley)--------------------------------------------------------------------------------------------------------------------------------------------(rrosen@RossMacbook)-
    `--> servi -f usebox                                                                                                                                                     [master]

    ***** ERROR *****
    servi: error: unrecognized arguments: -f

    usage: servi [global options] COMMAND [command options]

    Servi Main Commands

    optional arguments:
      -h, --help            show this help message and exit
      -v {0,1,2,3,4}, --verbose {0,1,2,3,4}
                            4: debug, 3: info, 2: warn, 1: error, 0: silent

    Commands:

        buildbox            Build a vagrant base box based on the current
                            template.
        diff                Diff changes betweeen your server config and servi's.
                            Note - set the DIFFTOOL parameter in Servifile.yml
        init                Init project
        lans                Local ANSible - Run ansbile on your local (vagrant)
                            setup.
        update              Update project with latest template
        usebox              Use a vagrant base box that you already created with
                            'servi buildbox'.
        zz                  Developer functions for maintaining servi. (you
                            shouldn't need this)


    **Servi Aborting**
    .-(~/dev/berkeley)--------------------------------------------------------------------------------------------------------------------------------------------(rrosen@RossMacbook)-
    `--> servi usebox                                                                                                                                                        [master]
    Servi - Running: usebox

    Master Directory: /Users/rrosen/dev/berkeley
    Template Directory: /Users/rrosen/dev/servi/servi_templates

    ***** ERROR *****
    Existing saved servi_box has a version less than existing template version.
    Either run "servi buildbox" or run "servi usebox --force."
    Template version: 0.1.24
    servi_box: servi_box_0_0_0.box
    Use -f / --force to override.

    **Servi Aborting**

    ***** ERROR *****
    Existing saved servi_box has a version less than existing template version.
    Either run "servi buildbox" or run "servi usebox --force."
    Template version: 0.1.24
    servi_box: servi_box_0_0_0.box
    Use -f / --force to override.

    **Servi Aborting**
    .-(~/dev/berkeley)--------------------------------------------------------------------------------------------------------------------------------------------(rrosen@RossMacbook)-
    `--> servi usebox -f                                                                                                                                                     [master]
    Servi - Running: usebox

    Master Directory: /Users/rrosen/dev/berkeley
    Template Directory: /Users/rrosen/dev/servi/servi_templates
    **************************
    
# Vagrant Networking Notes

Vagrant Networking Notes
config.vm.network "private_network", ip: extra_vars["STATIC_IP"]
  - Setup private network
<No forwarded port>
  - It will automatically create an ssh forward (eg: 2222 -> 22) and correct for collisions (for 127.0.0.1)
config.ssh.guest_port = 22
  - This will have vagrant automatically use the proper forwarded port (eg: 2222) when trying to talk to guest 22
Servifile:
vagrant:
     hosts:
       - 192.168.10.12  # For ansible inventory. Use this ip so you don't get into port collisions (Vagrant knows the forwarded port so it can always use 127.0.0.1:<forwarded>  Ansible doesn't. so we need (knownip:22)
     vars:
         HOST_NAME: vagrant-berkeley
         SERVER_NAME: vagrant-berkeley
         IS_VAGRANT: True
         ansible_ssh_port: 22  # Force ansible to use 22, otherwise Vagrant has it use a wrong port - 2222, even if it happens to be forwarded to 2200
