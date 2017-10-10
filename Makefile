engine:
	env/bin/python -m donna.engine

mongo:
	mongod --dbpath temp/data

client:
	env/bin/python -i client.py
