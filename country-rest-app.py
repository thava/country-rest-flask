#!thisenv/bin/python

import six
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import pymysql
import pandas as pd
import csv

# If you want to use https ...
# import pyopenssl

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

# Initialize MySQL Connection.

my_connection = None
my_cursor = None
country_df = None
country_name2obj = None
country_col2obj = None

LOAD_FROM_CSV    = False
COUNTRY_CSV_FILE = 'country.csv'

def load_data():
    if (LOAD_FROM_CSV) :
        init_from_csv()
    else:
        init_from_mysql()

def  init_from_csv():
    global country_df, country_name2obj, country_col2obj

    country_df = pd.read_csv(COUNTRY_CSV_FILE)
    country_df.head()
    # Strip whitespace
    country_df = country_df.applymap(lambda x: x.upper().strip() if type(x) is str else x)
    # Replace multiple spaces by single space
    country_df = country_df.applymap(lambda x: ' '.join(x.split()) if type(x) is str else x)
    country_df.insert(0, 'ID', range(1000, 1000 + len(country_df)))
    name_df = country_df.set_index('country')        # Set country name as index instead of 0..N index.
    country_name2obj = name_df.to_dict('index')      # Can look up using country name. 
    country_col2obj  = name_df.to_dict()             # Can look up using one column. e.g. 'population', 'birthrate', etc


def  init_from_csv_basic():

    with open(COUNTRY_CSV_FILE, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 1
        for row in csvreader:
            row = [x.strip() for x in row]
            print(', '.join(row))
            count += 1
            if count > 4:
                break

def  init_from_mysql():
    global my_connection
    global my_cursor
    global country_df, country_name2obj, country_col2obj
    try:

        # my_connection = pymysql.connect(host = 'localhost', user = '', passwd = '', db = 'restflask')
        my_connection = pymysql.connect(read_default_file="./my.cnf")
        my_cursor = my_connection.cursor()
        print('Connected to MySQL Database successfully.\n')
        query = 'select * from country'
        country_df = pd.read_sql(query, my_connection)
        country_df = country_df.applymap(lambda x: x.upper().strip() if type(x) is str else x)
        # Replace multiple spaces by single space
        country_df = country_df.applymap(lambda x: ' '.join(x.split()) if type(x) is str else x)
        country_df.insert(0, 'ID', range(1000, 1000 + len(country_df)))
        name_df = country_df.set_index('country')        # Set country name as index instead of 0..N index.
        country_name2obj = name_df.to_dict('index')      # Can look up using country name. 
        country_col2obj  = name_df.to_dict()             # Can look up using one column. e.g. 'population', 'birthrate', etc

        # country_df = country_df.set_index(['country'])

        # df[df['stridx'].str.contains("Hello|Britain")] returns series of matching column
        # for i in range(0, len(df)):
        #     print df.iloc[i]['country'], df.iloc[i]['population']

        # my_cursor.execute(query)
        # country_table = my_cursor.fetchall()
        # Construct row lookup given country name in lower case.
        # count = 1
        # for row in country_df:
        #   print('Row \n')
        #   print(row)
        #   count += 1
        #   if count > 5:
        #      break
    except pymysql.Error as e:
        print("MySQL Connection initialization error. MySQL updates will be ignored. Error %d: %s" % (e.args[0], e.args[1]))

@auth.get_password
def get_password(username):
    if username == 'flaskrestuser':
        return 'flaskrestpwd'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

props = {
        'Example_Name1': 'Example_Value1',
        'Example_Name2': 'Example_Value2'
    }

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': '''Welcome to Demo Flask REST App!
       End-Point        Operation  Notes
       /country         GET        Get list of countries
       /country/<name>  GET        Get details of given country
       /props           GET        Get all defined properties (name/value pairs)
       /prop            POST       Post (name, value) pair. Protected End point.
                                   Should post with Json body. '''
       })

@app.route('/country', methods=['GET'])
def country_list():
    return jsonify( { 'countries' : country_df['country'].tolist() } )

@app.route('/props', methods=['GET'])
def get_props():
    return jsonify(props)

@app.route('/country/<string:country_name>', methods=['GET'])
def get_country(country_name):
    if country_name in country_name2obj :
        country = country_name2obj[country_name]
        country['country'] = country_name
        return jsonify(country_name2obj[country_name])
    abort(404)

@app.route('/prop/<string:prop>', methods=['GET'])
def get_value(prop):
    if prop in props :
        return jsonify({ prop : props[prop] })
    abort(404)

#
# Update given name value pair given as json body as request.
# Currently the name/value pairs are not persisted in database.
#
@app.route('/prop', methods=['POST'])
@auth.login_required
def create_prop():
    if not request.json or 'name' not in request.json:
        abort(400)

    name = request.json['name']
    value = request.json.get('value', "")

    props[name] = value
    # import pdb; pdb.set_trace()
    return jsonify( { name : value }), 201

#
# Delete given name value pair
# Currently the name/value pairs are not persisted in database.
#
@app.route('/prop', methods=['DELETE'])
@auth.login_required
def delete_prop():
    if not request.json or 'name' not in request.json:
        abort(400)

    name = request.json['name']
    if not name in props :
        result = { 'result' : 'Already deleted' }
    else:
        del props[name]
        result = { 'result' : 'Deleted' }
    # import pdb; pdb.set_trace()
    # You can either return 200 (OK) or 204 (OK and no content).
    return jsonify(result), 200

if __name__ == '__main__':
    init_from_csv()
    # load_data()
    app.run()
    # If you want to run with https ... This is for using adhoc certificate.
    # In production env, you can use nginx at the front to handle certificates and app can be unaware of it.
    # app.run(ssl_context='adhoc')

