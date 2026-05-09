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
            loc_html = '<div class="event-location">' + (
                f'<a href="{location_link}">{html.escape(location)}</a>'
                if location_link else html.escape(location)
            ) + '</div>'
            topic_html = '<div class="event-title">' + (
                f'<a href="{topic_link}">{html.escape(topic)}</a>'
                if topic_link else html.escape(topic)
            ) + '</div>'
            dt_iso = dt.strftime("%Y-%m-%dT%H:%M:%S%:z")
            dt_hr = dt.strftime("%a %d.%m.%Y ab %H:%M Uhr")
            dt_html = (
                f'<div class="event-date"><time datetime="{dt_iso}">{dt_hr}</time></div>'
            )

            # for HTML print events not apparent yet
            if now < dt <= ( now + timedelta(days=90) ):

                events_html.append(
                    '<div class="event-card next">'
                    + f"<strong>{dt_html}</strong> {html.escape(desc)}"
                    + (f": {topic_html}" if topic_html else "")
                    + (f" im {loc_html}" if loc_html else "")
                    + '</div>'
                )

    # Write .ics
    Path(ICS_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(ICS_FILE).write_text(cal.serialize(), encoding="utf-8")

    # --- Write HTML index ---
    html_content = ""

    if Path(HEAD_FILE).exists():
        html_content += Path(HEAD_FILE).read_text(encoding="utf-8") + "\n"

    html_content += """
<!-- TERMINE -->
<section id="termine">

  <div class="container">
    <div class="section-label">Nächste Treffen</div>
    <h2>Stammtisch-Termine</h2>
    <div class="schedule-note">
      Wir treffen uns regelmäßig: <strong>In geraden Monaten am 2. Donnerstag ab 19:00 Uhr</strong>, 
      <strong>in ungeraden Monaten am 2. Mittwoch ab 17:30 Uhr</strong> (im LaVie), sowie 
      <strong>jeden 4. Donnerstag ab 19:00 Uhr</strong>. Die Zeiten können variieren.
    </div>

    <div class="events-grid">
""" + "\n".join(events_html) + """

    </div>

    <p style="color: var(--text-secondary); margin-top: 1.5rem; font-size: 0.9rem;">
      Thema ist alles rund um Bitcoin – außer Wechselkurse. Als Austauschmöglichkeit zwischen den Treffen gibt es Gruppen auf 
      <a href="https://t.me/BitcoinDresden" target="_blank">Telegram</a>, 
      <a href="https://matrix.to/#/#bitcoindresden:matrix.org">Matrix</a> und 
      <a href="https://simplex.chat/contact#/?v=2-7&smp=smp%3A%2F%2Fh--vW7ZSkXPeOUpfxlFGgauQmXNFOzGoizak7Ult7cw%3D%40smp15.simplex.im%2FVo6bfiY0rb-2IYx6R6R9LtkObbKguF0L%23%2F%3Fv%3D1-3%26dh%3DMCowBQYDK2VuAyEAoCKFTHTCgEdnvpm4IMwhRW7yc6yG8xsYHNkMRvwC1xI%253D%26srv%3Doauu4bgijybyhczbnxtlggo6hiubahmeutaqineuyy23aojpih3dajad.onion&data=%7B%22type%22%3A%22group%22%2C%22groupLinkId%22%3A%22falnhSgdHLTcP_lsP9DD3Q%3D%3D%22%7D">SimpleX</a>.
    </p>
  </div>
</section>
"""

    if Path(FOOT_FILE).exists():
        html_content += Path(FOOT_FILE).read_text(encoding="utf-8") + "\n"

    Path(HTML_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(HTML_FILE).write_text(html_content, encoding="utf-8")

if __name__ == "__main__":
    main()

"""
      <div class="event-card">
        <div class="event-date">Do, 23. April 2026 · 19:00 Uhr</div>
        <div class="event-title">Bitcoin Stammtisch</div>
        <div class="event-location"><a href="https://www.faehrgarten.de/">Fährgarten Johannstadt</a>, Käthe-Kollwitz-Ufer 23b</div>
      </div>
      <div class="event-card">
        <div class="event-date">Mi, 13. Mai 2026 · 17:30 Uhr</div>
        <div class="event-title">Bitcoin Stammtisch</div>
        <div class="event-location"><a href="https://laviecoffee.de/">LaVie Coffee</a>, Wallstraße 11</div>
      </div>
      <div class="event-card">
        <div class="event-date">Do, 28. Mai 2026 · 19:00 Uhr</div>
        <div class="event-title">Bitcoin Stammtisch</div>
        <div class="event-location"><a href="https://www.faehrgarten.de/">Fährgarten Johannstadt</a>, Käthe-Kollwitz-Ufer 23b</div>
      </div>
      <div class="event-card">
        <div class="event-date">Do, 11. Juni 2026 · 19:00 Uhr</div>
        <div class="event-title">Bitcoin Stammtisch</div>
        <div class="event-location"><a href="https://www.faehrgarten.de/">Fährgarten Johannstadt</a>, Käthe-Kollwitz-Ufer 23b</div>
      </div>
      <div class="event-card">
        <div class="event-date">Do, 25. Juni 2026 · 19:00 Uhr</div>
        <div class="event-title">Bitcoin Stammtisch</div>
        <div class="event-location"><a href="https://www.faehrgarten.de/">Fährgarten Johannstadt</a>, Käthe-Kollwitz-Ufer 23b</div>
      </div>
"""
