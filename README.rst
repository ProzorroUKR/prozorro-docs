Prozorro Documentation files for openprocurement.api
====================================================


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

 5. Build translated documentations::

     ../../bin/sphinxbuilder

