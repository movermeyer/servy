test:
	flake8
	nosetests --with-coverage --cover-package=servy ./tests/

publish: test docs
	python setup.py sdist bdist_wheel upload

clean:
	rm -rf build dist servy.egg-info

docs:
	rm -rf docs/_build/*
	python setup.py build_sphinx
	python setup.py upload_sphinx


.PHONY: test publish clean docs