MChron
======

This system will collect information from a SQLite3 database as filled
by proprietary software Sitrad by Full Gauge and make a report to
send via email.

1. Collect the data from the SQLite3 database
2. Create the elements of the report (v.g. graphics, text)
3. Form the PDF file
4. Send it by email

A configuration file will list

1. Which elements bellong to each graphic
2. Which elements should be sumarize in the text of the report
3. Email addresses that must be sent.

This product will not take care of its timing.  It should be
left to the operating system to call this program at regular intervals.

.