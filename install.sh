##########################################
# Installation script for CentOS/RHEL OS
#
# Author: Matthew Tan
# Version: 0.1
# Date: June 2, 2018
##########################################
## Install server wide packages
## PIP, Virtualenv, and NGINX
yum install python2-pip python-virtualenv nginx
##
## Check for pgsql user
user_runas="pgsql"
check_user=$(grep "${user_runas}" /etc/passwd)
if [ -z ${check_user} ]; then 
   echo "User ${user_runas} is not found. Creating user ${user_runas}"
   useradd pgsql
else 
   echo "User ${user_runas} is found"
fi

## Copy install script to tmp directory
cp install_pgsql_pip.sh /tmp/install_pgsql_pip.sh
chmod a+x /tmp/install_pgsql_pip.sh

sudo -i -u ${user_runas} bash -c "/tmp/install_pgsql_pip.sh"

usermod -a -G pgsql nginx
cd /etc/systemd/system
cp systemd/pgsql.service .

systemctl start pgsql.service
systemctl enable pgsql.service

cp nginx/nginx.conf /etc/nginx/nginx.conf
cp nginx/pgsql.conf /etc/nginx/conf.d/pgsql.conf

systemctl restart nginx.service

firewall-cmd --permanent --add-service=http
firewall-cmd --reload


cd /home
chmod 710 pgsql

setenforce 0
curl http://localhost/status

cd /var/log/audit
grep nginx audit.log | audit2allow -M nginx
semodule -i nginx.pp
setenforce 1


