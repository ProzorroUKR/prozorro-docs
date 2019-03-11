Prozorro Documentation for openprocurement.api
==============================================

.. image:: https://readthedocs.org/projects/prozorro-api-docs/badge/?version=latest
    :target: https://prozorro-api-docs.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Install for the docs development::

    1) `./bootstrap.sh` install requirements

    2) add "couchdb" to be resolved to localhost in /etc/hosts

    3) `docker-compose up -d` (to run couchdb if you don't have one)


Running tests to update http files::


    ./bin/py.test tests  # all
    ./bin/py.test tests/test_belowthreshold.py -k test_docs_milestones  # specific

Run build::

    ./bin/sphinx-build docs/source/ html

    or

    cd docs; make html SPHINXBUILD=../bin/sphinx-build

For translation into *uk* (2 letter ISO language code), you have to follow the scenario:

 1. Pull all translatable strings out of documentation::

     make gettext  SPHINXBUILD=../bin/sphinx-build


 2. Update translation with new/changed strings::

     ../bin/sphinx-intl update -p build/locale -l uk

 3. Update updated/missing strings in `docs/source/locale/<lang>/LC_MESSAGES/*.po` with your-favorite-editor/poedit/transifex/pootle/etc. to have all translations complete/updated.

 4. Compile the translation::

      ../../bin/sphinx-intl build

