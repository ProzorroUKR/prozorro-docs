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


SOURCE="src/openprocurement.tender.competitivedialogue/docs/source"
TARGET_DIR='docs/source/competitivedialogue'
rm -rf "$TARGET_DIR/tutorial"
rm -rf "$TARGET_DIR/multiple_lots_tutorial"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE/tutorial" "$TARGET_DIR"
cp -R "$SOURCE/multiple_lots_tutorial" "$TARGET_DIR"


SOURCE="src/openprocurement.tender.esco/docs/source"
TARGET_DIR='docs/source/esco'
rm -rf "$TARGET_DIR/tutorial"
rm -rf "$TARGET_DIR/multiple_lots_tutorial"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE/tutorial" "$TARGET_DIR"
cp -R "$SOURCE/multiple_lots_tutorial" "$TARGET_DIR"

SOURCE="src/openprocurement.planning.api/docs/source/tutorial/."
TARGET_DIR='docs/source/planning/tutorial'
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE" "$TARGET_DIR"
