.PHONY: clean-pyc test upload-docs

all: clean-pyc test

test:
	cd example_project; ./manage.py test native_tags

dist:
	python setup.py sdist

rmpyc:
	rm -rf `find . -name '*.pyc'`; rm -rf `find . -name '*.pyo'`

html:
	cd docs; make html
	cp -r docs/build/html/* export/
	rm -rf export/sphinx_sources export/sphinx_static
	mv export/_sources export/sphinx_sources
	mv export/_static export/sphinx_static
	perl -i -pe 's/_static/sphinx_static/g' `find export/ -name '*.html'`
	perl -i -pe 's/_sources/sphinx_sources/g' `find export/ -name '*.html'`

upload:
	cd export/; git pull origin master; git commit -a -m 'doc update'; git push origin master

tex:
	cd docs; make latex; make all-pdf

#cd docs/_build/; mv html flask-docs; zip -r flask-docs.zip flask-docs; mv flask-docs html
#scp -r docs/_build/dirhtml/* pocoo.org:/var/www/flask.pocoo.org/docs/
#scp -r docs/_build/latex/Flask.pdf pocoo.org:/var/www/flask.pocoo.org/docs/flask-docs.pdf
#scp -r docs/_build/flask-docs.zip pocoo.org:/var/www/flask.pocoo.org/docs/
