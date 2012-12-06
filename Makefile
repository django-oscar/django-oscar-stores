.PHONY: sandbox geoip

geoip:
	wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
	gunzip GeoLiteCity.dat.gz
	mv GeoLiteCity.dat sandbox/geoip

sandbox:
	rm sandbox/sandbox/sandbox.sqlite3 || true
	spatialite sandbox/sandbox/sandbox.sqlite3 "SELECT InitSpatialMetaData();" || true
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json
	./sandbox/manage.py loaddata countries.json
