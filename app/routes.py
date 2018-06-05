import psycopg2
from app import app
from pgdatabase import PgDatabase

@app.route('/')
@app.route('/index')
def index():
    return "This is the Index Page"

@app.route('/master')
def mastercheck():
    try:
        db = PgDatabase()
        my_list = db.query("SHOW transaction_read_only")
        
        my_string = ''.join(my_list)
        if my_string=='off':
            ret_string='MASTER'
        else:
            ret_string='READONLY'

        db.close()

        return ret_string
    except Exception as e:
        print e
        return []

@app.route('/slave')
def slavecheck():
    try:
        db = PgDatabase()
        my_list = db.query("SELECT pg_is_in_recovery()::text")

        my_string = ''.join(my_list)
        if my_string=='true':
            ret_string='SLAVE'
        else:
            ret_string='NOTSLAVE'

        db.close()

        return ret_string
    except Exception as e:
        print e
        return []

@app.route('/status')
def statuscheck():
    masterstat = mastercheck()
    slavestat = slavecheck()

    initalstat = 'UNKNOWN'

    if masterstat == 'MASTER' and slavestat == 'NOTSLAVE':
        return masterstat
    elif masterstat == 'READONLY' and slavestat == 'SLAVE':
        return slavestat
    else:
        return initialstat


