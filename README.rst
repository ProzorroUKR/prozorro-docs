Prozorro Documentation for openprocurement.api
==============================================

.. image:: https://readthedocs.org/projects/prozorro-api-docs/badge/?version=latest
    :target: https://prozorro-api-docs.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Install
-------

1. Install requirements by running::

    ./bootstrap.sh

2. Add "couchdb" to be resolved to localhost in /etc/hosts::

    echo "127.0.0.1 couchdb" >> /etc/hosts

3. To run couchdb if you don't have one::

    docker-compose up -d

Update
------
Running tests to update http files::

    ./venv/bin/py.test tests  # all
    ./venv/bin/py.test tests/test_belowthreshold.py -k test_docs_milestones  # specific

Build
-----

Run::

    ./venv/bin/sphinx-build docs/source/ html

or::

    cd docs

    make html SPHINXBUILD=../venv/bin/sphinx-build

Translation
-----------

For translation into *uk* (2 letter ISO language code), you have to follow the scenario:

1. Pull all translatable strings out of documentation::

    cd docs

    make gettext SPHINXBUILD=../venv/bin/sphinx-build

2. Update translation with new/changed strings::

    cd docs

    ../venv/bin/sphinx-intl update -p build/locale -l uk -w 0

3. Update updated/missing strings in `docs/source/locale/<lang>/LC_MESSAGES/*.po` with your-favorite-editor/poedit/transifex/pootle/etc. to have all translations complete/updated.

4. Compile the translation::

    cd docs

    ../venv/bin/sphinx-intl build

