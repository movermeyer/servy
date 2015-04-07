test:
	flake8
	nosetests --with-coverage --cover-package=servy ./tests/

docs:
	rm -rf docs/_build/*
