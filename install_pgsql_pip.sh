user_runas="pgsql"

if [ "$(whoami)" == "${user_runas}" ]; then
   echo "Running as user: ${user_runas}"
else
   echo "Aborting script; not running as user ${user_runas}"
   exit 1
fi

mkdir -p /home/pgsql/pgcheck
cd /home/pgsql/pgcheck
virtualenv pgcheckenv
source pgcheckenv/bin/activate
pip install flask psycopg2 ConfigParser uwsgi
