Prozorro Documentation for openprocurement.api
==============================================

.. image:: https://readthedocs.org/projects/prozorro-api-docs/badge/?version=latest
    :target: https://prozorro-api-docs.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Install for the docs development::

    1) docker-compose up

    2) wait until the installation ends
    (all the services run within containers but the all files are shared with host)

    3) docker-compose exec docs bash
    (Now you can execute any of the commands below)


Running tests to update http files::


    ./bin/py.test tests  # all
    ./bin/py.test tests/test_belowthreshold.py -k test_docs_milestones  # specific

Run build::

    ./bin/sphinxbuilder

For translation into *uk* (2 letter ISO language code), you have to follow the scenario:

 1. Pull all translatable strings out of documentation::

     cd docs/_build
     make gettext

 2. Update translation with new/changed strings::

     cd ../source
     ../../bin/sphinx-intl update -p ../_build/locale -l uk

 3. Update updated/missing strings in `docs/source/locale/<lang>/LC_MESSAGES/*.po` with your-favorite-editor/poedit/transifex/pootle/etc. to have all translations complete/updated.

 4. Compile the translation::

      ../../bin/sphinx-intl build

