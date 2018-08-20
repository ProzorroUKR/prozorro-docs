Prozorro Documentation for openprocurement.api
==============================================
.. image:: https://readthedocs.org/projects/prozorro-api-docs/badge/?version=latest
    :target: https://prozorro-api-docs.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This docs are also built from http-files after travis runs of the following reps:
openprocurement.api
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.api.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.api
openprocurement.tender.openua
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openua.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openua
openprocurement.tender.openuadefense
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openuadefense.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openuadefense
openprocurement.tender.openeu
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openeu.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.tender.openeu
openprocurement.tender.limited
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.tender.limited.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.tender.limited
openprocurement.contracting.api
.. image:: https://travis-ci.org/ProzorroUKR/openprocurement.contracting.api.svg?branch=master
    :target: https://travis-ci.org/ProzorroUKR/openprocurement.contracting.api

----------------------------------------------

Install for the docs development::

  ./bootstrap.sh
  ./bin/buildout

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

