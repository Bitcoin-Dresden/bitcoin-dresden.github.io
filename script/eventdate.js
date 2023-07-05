// You need to include rrule.js library to use this function
// used v2.7.1 in January 2023, see https://github.com/jakubroztocil/rrule/releases/latest for updates
//~ import * as RRule from 'https://jakubroztocil.github.io/rrule/dist/es5/rrule.js';
import * as RRule from 'https://bitcoin-dresden.de/script/rrule.min.js';

var now = new Date();
function getCETorCESTDateOffset() {
	var utcOffset = now.getTimezoneOffset();
	var cetOffset = utcOffset + 60;
	var cestOffset = utcOffset + 120;
	var cetOffsetInMilliseconds = cetOffset * 60 * 1000;
	var cestOffsetInMilliseconds = cestOffset * 60 * 1000;

	var cestDateStart = new Date();
	var cestDateFinish = new Date();
	var localDateTime = now.getTime();
	var cestDateStartTime;
	var cestDateFinishTime;
	var result;

	cestDateStart.setTime(Date.parse('29 March ' + now.getFullYear() + ' 02:00:00 GMT+0100'));
	cestDateFinish.setTime(Date.parse('25 October ' + now.getFullYear() + ' 03:00:00 GMT+0200'));

	cestDateStartTime = cestDateStart.getTime();
	cestDateFinishTime = cestDateFinish.getTime();

	if(localDateTime >= cestDateStartTime && localDateTime <= cestDateFinishTime) {
		result = cestOffsetInMilliseconds;
	} else {
		result = cetOffsetInMilliseconds;
	}

	return result;
}

var localTimeOffset=getCETorCESTDateOffset();

document.addEventListener("DOMContentLoaded", function(event) { 

	for(const tag of document.getElementsByTagName("time") ){
		if (tag.getAttribute('data-rrule') !== null) {
			var rule = rrule.RRule.fromString(tag.getAttribute('data-rrule').toUpperCase());
			var e = rule.after(now);
			tag.setAttribute('datetime', new Date(e - -localTimeOffset).toISOString());
			var f = new Intl.DateTimeFormat("de-DE", { //timeZoneName: "short", second: "numeric" | day: "2-digit" 
				 timeZone: "UTC", year: "numeric", month: "long", day: "numeric", weekday: "long"//, hour: "numeric", minute: "numeric"
				 }).format(e)//.replace(' um ',' ab ')
				 ;
			//~ console.log(f);
			//~ tag.innerHTML = " am " + f + "Uhr";
			var title = 'planmäßig '+rule.toText().replace('every day','jeden Tag').replace('every week','jede Woche').replace('every month','jeden Monat').replace('every year','jedes Jahr').replace('on the','am').replace('Monday','Montag').replace('Tuesday','Dienstag').replace('Wednesday','Mittwoch').replace('Thursday','Donnerstag').replace('Friday','Freitag').replace('Saturday','Samstag').replace('Sunday','Sonntag').replace('2nd','zweiten').replace('1st','ersten').replace('3rd','dritten').replace('4th','vierten') + " " + f.substr(f.lastIndexOf('ab '));
			//~ console.log(title);
			tag.setAttribute('title', title);
		}
	}

});
