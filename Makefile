.PHONY: install sandbox css

install:
	pip install -e . -r requirements.txt django-oscar

sandbox: install
	-rm -rf sandbox/public/media/cache sandbox/public/media/uploads
	./sandbox/manage.py migrate
	./sandbox/manage.py loaddata sandbox/fixtures/auth.json
	./sandbox/manage.py loaddata sandbox/fixtures/countries.json
	./sandbox/manage.py loaddata sandbox/fixtures/stores.json
	./sandbox/manage.py thumbnail clear

css:
	lessc stores/static/stores/less/stores.less > stores/static/stores/css/stores.css
