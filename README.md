

# REST API Server Example with Flask Backend

We are going to build a simple REST API Server application.

## Synopsis

```

  python3 -m venv thisenv             # Or run this: virtualenv --python=/usr/bin/python3  thisenv
  .  ./thisenv/bin/activate
  pip install -r requirements.txt

  pip install csvkit

  # Optional: Do the following if the csv file contains "," as decimal separator.
  # csvformat -D ';' country.csv > c2.csv
  # cat c2.csv | tr  ',' '.' | tr ';' ',' > country.csv
  # use csvcut to select subset of columns.

  csvsql country.csv > country.sql
  echo "create database restflask ; use restflask; source country.sql " | mysql
  #  mysqlimport --ignore-lines=1  --fields-terminated-by=, --local restflask country.csv
  mysql --local-infile  restflask <<EOF
              LOAD DATA LOCAL INFILE 'country.csv' INTO TABLE country 
              FIELDS TERMINATED BY ',' 
              OPTIONALLY ENCLOSED BY '\"' 
              IGNORE 1 LINES; SHOW WARNINGS
  EOF

  Run the program:

  python country-rest-app.py

```
  



---

## Notes

* The program supports MySQL as data store, or you can also just use .csv file without using MySQL.

* The test-with-curl.sh program illustrates how to do unit testing using curl command.

* The pytestrest.py uses python requests module for testing.

* You can also run the python test through jupyter notebook:

```
  pip install jupyter 

  jupyter  notebook

  # Open empty cell; 

  %load pytestrest.py 

  # Now You can use the notebook to step through the tests.
  
  # Note: Or you can try more advanced jupyter lab interface instead of classic jupyter notebook

  pip install jupyterlab

  jupyter lab


```

## Example Outputs

```

	$ curl localhost:5000/country  | python -m json.tool

	{
		"countries": [
			"AFGHANISTAN",
			"ALBANIA",
			"ALGERIA",
			 ....
			 ....
			"WESTERN SAHARA",
			"YEMEN",
			"ZAMBIA",
			"ZIMBABWE"
		]
	}

	$ curl -s localhost:5000/props  | python -m json.tool
	{
		"Example_Name1": "Example_Value1",
		"Example_Name2": "Example_Value2"
	}

    $ curl -u flaskrestuser:flaskrestpwd -H "Content-Type: application/json"  \
           -X POST -d '{ "name" : "New Property", "value" : "New Value" }'  http://localhost:5000/prop

	$ curl -s localhost:5000/props  | python -m json.tool
	{
		"Example_Name1": "Example_Value1",
		"Example_Name2": "Example_Value2",
		"New Property": "New Value"
	}


```

## Links For Further Reading

* https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
* Countries of the world data set https://www.kaggle.com/fernandol/countries-of-the-world/downloads/countries-of-the-world.zip/1
* csvkit tool http://csvkit.readthedocs.org/en/latest/scripts/csvsql.html
* Json web tokens for Flask applications https://github.com/mattupstate/flask-jwt

## Notes

* For the web framework, we use Flask which is a micro web framework written in Python. 
  Flask is WSGI (Web Server Gateway Interface - Standard calling convention for Python web servers) compatible. 
  WSGI is akin to servlet-API for Java. It enables compatibility for web applications to choose different 
  WSGI compliant webservers later if need be.

## Acknowledgements

* This project includes dataset countries.csv downloaded from kaggle.com;


---
