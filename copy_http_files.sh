#!/bin/sh

TARGET_DIR='docs/source/http'
SOURCE='src/openprocurement.tender.belowthreshold/docs/source'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE/tutorial" "$TARGET_DIR"
cp -R "$SOURCE/qualification" "$TARGET_DIR"
cp -R "$SOURCE/complaints" "$TARGET_DIR"


SOURCE="src/openprocurement.contracting.api/docs/source/tutorial/."
TARGET_DIR='docs/source/contracting/http'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE" "$TARGET_DIR"


SOURCE="src/openprocurement.tender.openuadefense/docs/source/tutorial/."
TARGET_DIR='docs/source/defense/http'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE" "$TARGET_DIR"


SOURCE="src/openprocurement.tender.limited/docs/source"
TARGET_DIR='docs/source/limited/http'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE/tutorial" "$TARGET_DIR"
cp -R "$SOURCE/multiple_lots_tutorial" "$TARGET_DIR"


SOURCE="src/openprocurement.tender.openeu/docs/source"
TARGET_DIR='docs/source/openeu/http'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE/tutorial" "$TARGET_DIR"
cp -R "$SOURCE/multiple_lots_tutorial" "$TARGET_DIR"


SOURCES="src/openprocurement.tender.openua/docs/source/tutorial/."
TARGET_DIR='docs/source/openua/http'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCES" "$TARGET_DIR"


ARRAY=("array=('src/openprocurement.tender.cfaua/docs/source/tutorial/.' 'docs/source/cfaua/tutorial')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/tutorial/.' 'docs/source/agreementcfaua/tutorial')")
for element in "${ARRAY[@]}"; do
    eval $element
    SOURCES=${array[0]}
    TARGET_DIR=${array[1]}
    rm -rf "$TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    cp -R "$SOURCES" "$TARGET_DIR"
done


ARRAYFILES=("array=('src/openprocurement.agreement.cfaua/docs/source/tutorial.rst' 'docs/source/agreementcfaua/tutorial.rst')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/tutorial.mo' 'docs/source/locale/uk/LC_MESSAGES/agreementcfaua/tutorial.mo')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/tutorial.po' 'docs/source/locale/uk/LC_MESSAGES/agreementcfaua/tutorial.po')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/standard/base_change.rst' 'docs/source/standard/base_change.rst')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/standard/base_change.mo' 'docs/source/locale/uk/LC_MESSAGES/standard/base_change.mo')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/standard/base_change.po' 'docs/source/locale/uk/LC_MESSAGES/standard/base_change.po')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/standard/change.rst' 'docs/source/standard/change.rst')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/standard/change.mo' 'docs/source/locale/uk/LC_MESSAGES/standard/change.mo')"
       "array=('src/openprocurement.agreement.cfaua/docs/source/locale/uk/LC_MESSAGES/standard/change.po' 'docs/source/locale/uk/LC_MESSAGES/standard/change.po')")


for element in "${ARRAYFILES[@]}"; do
    eval $element
    SOURCE=${array[0]}
    TARGET_DIR=${array[1]}
    rm -rf "$TARGET_DIR"
    cp "$SOURCE" "$TARGET_DIR"
done