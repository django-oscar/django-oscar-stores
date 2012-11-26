.PHONY: sandbox


sandbox:
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate 
