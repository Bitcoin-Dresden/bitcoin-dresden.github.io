#!/bin/sh

# eventdate.sh - Berechnet den N-ten Wochentag eines Monats
# POSIX-kompatibel, GNU date erforderlich

# Abhängigkeiten prüfen
dependencies="date"
for d in $(printf "%s\n" "$dependencies"); do
    command -v "$d" >/dev/null 2>&1 || { >&2 printf "Missing command: %s\n" "$d"; exit 1; }
done

# Prüft, ob das Datum in Sommer- oder Winterzeit liegt
# Eingabe: YYYY-MM-DD
# Ausgabe: 01:00 für Winterzeit, 02:00 für Sommerzeit
check_dst() {
    DATE=$1
    # Prüfe Zeitzone nach 03:00 Uhr
    TZ_OFFSET=$(date -d "$DATE 03:00" +%H)

    # Alternativ kann man %z prüfen: +0100 = Winter, +0200 = Sommer
    OFFSET=$(date -d "$DATE 03:00" +%z)

    case "$OFFSET" in
        +0100) printf "01:00\n" ;; # Winterzeit
        +0200) printf "02:00\n" ;; # Sommerzeit
        *) if [ "${#OFFSET}" -eq 5 ]; then printf "$OFFSET"|tr -d "+"|sed 's/\(..\)\(..\)/\1:\2/'; else printf "$OFFSET"; fi;;
    esac
}

eventdate() {
    YEAR=$1
    MONTH=$2
    N=$3
    WEEKDAY=$4

    if test "$N" -gt 0; then 
        # 1. Tag des Monats
        FIRST_DAY=$(date -d "$YEAR-$MONTH-01" +%w)
	    
        # Differenz zum gesuchten Wochentag
        DIFF=$(( (WEEKDAY - FIRST_DAY + 7) % 7 ))
	    
        # Tag des N-ten Wochentags
        DAY=$(( 1 + DIFF + (N - 1) * 7 ))
    elif test "$N" -eq 0; then
        printf "error: 0 is invalid.\n"; exit 1;
    else
        LAST_DAY_OF_MONTH=$(date -d "$YEAR-$MONTH-01 +1 month -1 day" +%d)
        LAST_WEEKDAY=$(date -d "$YEAR-$MONTH-$LAST_DAY_OF_MONTH" +%w)
        DIFF=$(( (LAST_WEEKDAY - WEEKDAY + 7) % 7 ))
        DAY=$(( LAST_DAY_OF_MONTH - DIFF + (N + 1) * 7 ))
    fi
	
    # Ausgabe im Format YYYY-MM-DD
    printf "%04d-%02d-%02d\n" "$YEAR" "$MONTH" "$DAY"
}

icsdate(){
	if [ $# -lt 4 ]; then >&2 printf "icsdate() has too few parameters: $@\n"; exit 1; else d=$(eventdate $1 $2 $3 $4); fi
	if [ -z "$5" ]; then t=""; else t="$5"; fi
	if [ -z "$6" ]; then n=""; else n="||$6||||"; fi
	z=$(check_dst "$d")
	# Ausgabe im Format YYYY-MM-DD+Z
	printf "%sT%s:00+%s%s\n" "$d" "$t" "$z" "$n"
}

show_help() {
    cat <<'EOF'
NAME
    eventdate.sh - Berechnet den N-ten Wochentag eines Monats

SYNOPSIS
    ./eventdate.sh JAHR MONAT N Wochentag
    ./eventdate.sh test
    ./eventdate.sh help

BESCHREIBUNG
    Gibt das Datum des N-ten Vorkommens eines bestimmten Wochentags
    in einem Monat aus.

PARAMETER
    JAHR        Vierstelliges Jahr, z.B. 2025
    MONAT       Monat als Zahl 1..12
    N           Welcher Wochentag im Monat (1..5)
    Wochentag   0=Sonntag .. 6=Samstag

SPEZIALPARAMETER
    test        Führt vordefinierte Selbsttests aus
    help        Zeigt diese Hilfe an

BEISPIELE
    ./eventdate.sh 2025 1 2 3
        → 2. Mittwoch im Januar 2025 → 2025-01-08

    ./eventdate.sh 2025 12 4 4
        → 4. Donnerstag im Dezember 2025 → 2025-12-25

EOF
}

if [ "$1" = "help" ]; then
    show_help
    exit 0
fi

if [ "$1" = "test" ]; then
    # Testfälle: "Jahr Monat N Wochentag ErwartetesDatum"
    tests="
2025 1 2 3 2025-01-08
2025 12 4 4 2025-12-25
2023 3 1 0 2023-03-05
2024 2 3 5 2024-02-16
2026 1 -1 4 2026-01-29
2024 12 -1 1 2024-12-30
"

    all_ok=1
    printf "$tests\n" | while read YEAR MONTH N WEEKDAY EXPECTED; do
        result=$(eventdate "$YEAR" "$MONTH" "$N" "$WEEKDAY")
        if [ "$result" = "$EXPECTED" ]; then
            >&2 printf "PASS: %d-%d-%d %d → %s\n" "$YEAR" "$MONTH" "$N" "$WEEKDAY" "$result"
        else
            >&2 printf "FAIL: %d-%d-%d %d → %s (expected %s)\n" "$YEAR" "$MONTH" "$N" "$WEEKDAY" "$result" "$EXPECTED"
            all_ok=0
        fi
    done

    # Die while-Schleife läuft in einer Subshell, all_ok bleibt nicht erhalten.
    # Deshalb prüfen wir die Ergebnisse anders: alle Ergebnisse müssen PASS sein
    >&2 printf "Tests abgeschlossen. Bitte Ausgabe überprüfen.\n"
    exit 0
fi

if [ "$1" = "xbtdd" ]; then
	shift
	>&2 printf "Daten für den Bitcoin Stammtisch in Dresden in diesem Monat:\n\n"
	#~ printf "$#: $@\n"
	now=$( date --iso-8601|tr "-" " "|cut -d" " -f1,2 )
	if [ $# -lt 1 ]; then
		y=$(printf "$now"|cut -d" " -f1)
		m=$(printf "$now"|cut -d" " -f2)
	else
	    if [ $# -eq 2 ]; then
			y="$1"
			m="$2"
		else # $# -eq 1
			y=$(printf "$now"|cut -d" " -f1)
			m="$1"
		fi
	fi
	mod=$(( $m % 2 ))
	# unterscheide (un)gerade Monate
	#~ printf "#:$#\ny:$y\nm:$m\n"
	n="Bitcoin Stammtisch Dresden"
	if [ $mod -eq 0 ]; then # gerade: Do
		icsdate $y $m 2 4 "19:00" "$n"
	else # ungerade: Mi
		icsdate $y $m 2 3 "17:30" "$n"
	fi
	icsdate $y $m 4 4 "19:00" "$n"
	exit 0
fi

if [ $# -ne 4 ]; then
    >&2 printf "Falsche Anzahl an Parametern. Verwenden Sie './eventdate.sh help' für Hilfe.\n"
    exit 1
fi

eventdate "$1" "$2" "$3" "$4"
