.PHONY: install sandbox geoip

install:
	python setup.py develop
	pip install -r requirements.txt

geoip:
	wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
	gunzip GeoLiteCity.dat.gz
	mv GeoLiteCity.dat sandbox/geoip

sandbox: install
	-rm -rf sandbox/public/media/cache sandbox/public/media/uploads
	./sandbox/manage.py reset_db --router=default --noinput
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json countries.json \
		sandbox/fixtures/stores.json
	./sandbox/manage.py thumbnail clear
