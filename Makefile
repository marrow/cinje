PROJECT = cinje
USE = development

.PHONY: all develop clean veryclean test release

all: clean develop test  ## Clean caches, refresh project metadata, execute all tests.

develop: ${PROJECT}.egg-info/PKG-INFO  ## Populate project metadata.

help:  ## Show this help message and exit.
	@echo "Usage: make <command>\n\033[36m\033[0m"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-18s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) | sort

clean:  ## Remove executable caches and ephemeral collections.
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf build htmlcov

veryclean: clean  ## Remove all project metadata, executable caches, and sensitive collections.
	rm -rvf *.egg-info .packaging/{build,dist,release}/*

lint:  ## Execute pylint across the project.
	pylint --rcfile=setup.cfg marrow

test: develop
	pytest

testloop:  ## Automatically execute the test suite limited to one failure.
	find marrow test -name \*.py | entr -c pytest --ff --maxfail=1 -q

release:  ## Package up and utilize Twine to issue a release.
	./setup.py sdist bdist_wheel ${RELEASE_OPTIONS}
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

${PROJECT}.egg-info/PKG-INFO: setup.py setup.cfg
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	
	@# General
	@[ ! -e /private ] && pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -e ".[${USE}]" || true
	
	@# macOS Specific
	@[ -e /private ] && env LDFLAGS="-L/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib -L$(brew --prefix openssl@1.1)/lib -L$(brew --prefix)/lib" \
		CFLAGS="-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include -I$(brew --prefix openssl@1.1)/include -I$(brew --prefix)/include" \
		pip install -e '.[development]'

