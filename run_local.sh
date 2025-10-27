#!/usr/bin/env bash
set -e

BUILD_DIR=${BUILD_DIR:-public}
ICS_FILE=${ICS_FILE:-$BUILD_DIR/events.ics}
HTML_FILE=${HTML_FILE:-$BUILD_DIR/index.html}

mkdir -p "$BUILD_DIR"

printf "Generating events…"
# search string with date
s=$(date --iso-8601|cut -d"-" -f1-2)
# add if missing
grep "$s" events.csv >/dev/null && printf " added none.\n" || { printf "\n"; eventdate.sh xbtdd $(printf "$s"|tr "-" " ") >> events.csv; }
# write to ics and html
printf "Building ICS and HTML…"
ICS_FILE="$ICS_FILE" HTML_FILE="$HTML_FILE" python build_events.py
cp "${ICS_FILE}" ./
cp "${HTML_FILE}" ./
rm -rf "${BUILD_DIR}"
printf " done.\n"
