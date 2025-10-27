import csv
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from ics import Calendar, Event
import html

CSV_FILE = "events.csv"
ICS_FILE = os.environ.get("ICS_FILE", "public/events.ics")
HTML_FILE = os.environ.get("HTML_FILE", "public/index.html")  # jetzt index.html

HEAD_FILE = "head.html"
FOOT_FILE = "foot.html"

def main():
    cal = Calendar()
    events_html = []

    now = datetime.now(timezone.utc)

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            if not row["Datetime"]:
                continue
            dt = datetime.fromisoformat(row["Datetime"])

            # Skip past events only after month is over
            if dt.month < ( now.month + (now.year - dt.year) * 12 ):
                continue

            duration = row["Duration"].strip() if row["Duration"] else ""
            desc = row["Description"].strip()
            location = row["Location"].strip() if row["Location"] else ""
            location_link = row["LocationLink"].strip() if row["LocationLink"] else ""
            topic = row["Topic"].strip() if row["Topic"] else ""
            topic_link = row["TopicLink"].strip() if row["TopicLink"] else ""

            # --- iCal event ---
            e = Event()
            e.begin = dt
            if duration:
                try:
                    minutes = int(duration)
                    e.duration = timedelta(minutes=minutes)
                except ValueError:
                    pass

            # Name: Topic or Description
            e.name = topic or desc

            # Description: Description + Topic (with link) + Location (with link)
            description_parts = [desc] if desc else []
            if topic:
                if topic_link:
                    description_parts.append(f"{topic} ({topic_link})")
                else:
                    description_parts.append(topic)
            if location:
                e.location = (f"{location}")
                if location_link:
                    description_parts.append(f"Adresse: {location} (Website zur Location: {location_link})")
                else:
                    description_parts.append(f"Adresse: {location}")
            description_parts.append(f"Bitcoin Dresden Website: https://bitcoin-dresden.de/")
            e.description = "; ".join(description_parts)

            # Location field (optional, only plain text)
            if location:
                e.location = location

            cal.events.add(e)

            # --- HTML list item ---
            loc_html = (
                f'<a href="{location_link}">{html.escape(location)}</a>'
                if location_link else html.escape(location)
            )
            topic_html = (
                f'<a href="{topic_link}">{html.escape(topic)}</a>'
                if topic_link else html.escape(topic)
            )
            dt_iso = dt.strftime("%Y-%m-%dT%H:%M:%S%:z")
            dt_hr = dt.strftime("%d.%m.%Y ab %H:%M Uhr")
            dt_html = (
                f'<time datetime="{dt_iso}">{dt_hr}</time>'
            )

            # for HTML print events not apparent yet
            if dt > now:

                events_html.append(
                    f"<li><strong>{dt_html}</strong> {html.escape(desc)}"
                    + (f": {topic_html}" if topic_html else "")
                    + (f" im {loc_html}" if loc_html else "")
                    + "</li>"
                )

    # Write .ics
    Path(ICS_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(ICS_FILE).write_text(cal.serialize(), encoding="utf-8")

    # --- Write HTML index ---
    html_content = ""

    if Path(HEAD_FILE).exists():
        html_content += Path(HEAD_FILE).read_text(encoding="utf-8") + "\n"

    html_content += "<ul><u>Konkrete Termine und Orte</u>\n" + "\n".join(events_html) + "\n</ul>\n"

    if Path(FOOT_FILE).exists():
        html_content += Path(FOOT_FILE).read_text(encoding="utf-8") + "\n"

    Path(HTML_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(HTML_FILE).write_text(html_content, encoding="utf-8")

if __name__ == "__main__":
    main()
