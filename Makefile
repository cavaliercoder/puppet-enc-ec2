all: dist

dist:
	python setup.py sdist

install:
	pip install --upgrade .

clean:
	rm -vrf \
		puppet_enc_ec2.egg-info \
		build \
		dist

upload:
	python setup.py sdist upload

.PHONY: all dist install clean upload
