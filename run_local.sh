#!/usr/bin/env bash
set -e

BUILD_DIR=${BUILD_DIR:-public}
ICS_FILE=${ICS_FILE:-$BUILD_DIR/events.ics}
HTML_FILE=${HTML_FILE:-$BUILD_DIR/index.html}

mkdir -p "$BUILD_DIR"

echo "Generating events..."
ICS_FILE="$ICS_FILE" HTML_FILE="$HTML_FILE" python build_events.py
cp "${ICS_FILE}" ./
cp "${HTML_FILE}" ./
rm -rf "${BUILD_DIR}"

#~ echo "Done:"
#~ echo " - $ICS_FILE"
#~ echo " - $HTML_FILE"
