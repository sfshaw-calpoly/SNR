CPYTHON=python3
CPYTHON39=python3.9
PYPY=pypy3
PYTHON=$(CPYTHON)

SETUP_PY=setup.py
PY_SETUP=$(PYTHON) $(SETUP_PY)

BUILD_DIR=build
DIST_DIR=dist
SRC_DIR=snr
TEST_DIR=$(SRC_DIR)/test


TEST_FLAGS=test -d

.PHONY: dev develop check build install dist test
d: dev
dev: develop
	$(PYTHON) $(SRC_DIR)/dev.py

develop:
	$(PY_SETUP) develop --user

console:
	$(PYTHON) $(SRC_DIR)/io/console/console.py

check:
	$(PY_SETUP) check

build: check
	$(PY_SETUP) build

dist: check
	$(PY_SETUP) sdist

install: check
	$(PY_SETUP) install --user

t: test
test: check
	$(PYTHON) -m unittest -v

clean:
	$(PY_SETUP) clean
	rm -rf ./$(BUILD_DIR) ./$(DIST_DIR)

py:
	$(PYTHON)
