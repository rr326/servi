# Install OWASP Core Rule Set
# http://www.thefanclub.co.za/how-to/how-install-apache2-modsecurity-and-modevasive-ubuntu-1204-lts-server

cd /tmp

# This fails!
# wget -O SpiderLabs-owasp-modsecurity-crs.tar.gz https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/master
# tar -zxvf SpiderLabs-owasp-modsecurity-crs.tar.gz
# cp -R SpiderLabs-owasp-modsecurity-crs-*/* /etc/modsecurity/
# Need an earlier version of owasp: http://bentoslack.com/syntax-error-on-line-52-of-etcmodsecurityactivated_rulesmodsecurity_crs_20_protocol_violations-conf-solved/

wget https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/v2.2.5#sthash.j9qEuecO.dpuf
tar xvf v2.2.5
cp -r SpiderLabs-owasp-modsecurity-crs-5c28b52/* /etc/modsecurity/ 


rm SpiderLabs-owasp-modsecurity-crs.tar.gz
rm -R SpiderLabs-owasp-modsecurity-crs-*
mv /etc/modsecurity/modsecurity_crs_10_setup.conf.example /etc/modsecurity/modsecurity_crs_10_setup.conf


cd /etc/modsecurity/base_rules
for f in * ; do sudo ln -sf /etc/modsecurity/base_rules/$f /etc/modsecurity/activated_rules/$f ; done

cd /etc/modsecurity/optional_rules
for f in * ; do sudo ln -sf /etc/modsecurity/optional_rules/$f /etc/modsecurity/activated_rules/$f ; done 