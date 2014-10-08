## TODO
* Servi
    * rans
    * Use logging instead of qprint


* Templates
    * Remove static ips? (and use that tool that does *.dev?)

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