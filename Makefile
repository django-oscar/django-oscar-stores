.PHONY: install sandbox geoip css

install:
	pip install -e . -r requirements.txt --process-dependency-links --allow-external django-oscar 

geoip:
	# Fetch GeoIP data
	wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
	gunzip GeoLiteCity.dat.gz
	mv GeoLiteCity.dat sandbox/geoip

sandbox: install
	-rm -rf sandbox/public/media/cache sandbox/public/media/uploads
	# command below will break if using PostGIS without a template database
	./sandbox/manage.py reset_db --router=default --noinput
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json countries.json
	./sandbox/manage.py loaddata sandbox/fixtures/stores.json
	./sandbox/manage.py thumbnail clear

css:
	lessc stores/static/stores/less/stores.less > stores/static/stores/css/stores.css
