.PHONY: sandbox geoip

install:
	python setup.py develop
	pip install -r requirements.txt

geoip:
	wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
	gunzip GeoLiteCity.dat.gz
	mv GeoLiteCity.dat sandbox/geoip

sandbox: install
	-rm sandbox/sandbox/sandbox.sqlite3
	-spatialite sandbox/sandbox/sandbox.sqlite3 "SELECT InitSpatialMetaData();"
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json countries.json
