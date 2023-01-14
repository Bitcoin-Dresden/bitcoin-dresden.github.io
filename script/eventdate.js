// You need to include rrule.js library to use this function
// used v2.7.1 in January 2023, see https://github.com/jakubroztocil/rrule/releases/latest for updates
//~ import * as RRule from 'https://jakubroztocil.github.io/rrule/dist/es5/rrule.js';
import * as RRule from 'http://btc.bplaced.net/script/rrule.min.js';

document.addEventListener("DOMContentLoaded", function(event) { 

	for(const tag of document.getElementsByClassName("rrule") ){
		var now = new Date();
		var rule = rrule.RRule.fromString(tag.getAttribute('datetime').toUpperCase());
		var e = rule.after(now);
		tag.setAttribute('datetime', new Date(e - -now.getTimezoneOffset()*60000).toISOString());
		var f = new Intl.DateTimeFormat("de-DE", { //timeZoneName: "short", second: "numeric" | day: "2-digit" 
			 timeZone: "UTC", year: "numeric", month: "long", day: "numeric", weekday: "long", hour: "numeric", minute: "numeric" }).format(e).replace(' um ',' ab ');
		//~ console.log(f);
		tag.innerHTML = "nächster Termin am " + f + " Uhr";
		var title = rule.toText().replace('every day','jeden Tag').replace('every week','jede Woche').replace('every month','jeden Monat').replace('every year','jedes Jahr').replace('on the','am').replace('Monday','Montag').replace('Tuesday','Dienstag').replace('Wednesday','Mittwoch').replace('Thursday','Donnerstag').replace('Friday','Freitag').replace('Saturday','Samstag').replace('Sunday','Sonntag').replace('2nd','zweiten').replace('1st','ersten').replace('3rd','dritten').replace('4th','vierten') + " " + f.substr(f.lastIndexOf('ab '));
		//~ console.log(title);
		tag.setAttribute('title', title);
	}

});
