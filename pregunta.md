My production environment is an Ubuntu 13.10 machine.  My production environment are Windows boxes (Both Win XP and Windows 7)<sup>1</sup>

I am trying to format date strings using python's `time.strftime` with `locale` set to Spanish; when forming a document using `reportlab`.
In development (Linux) I use `es_CO.utf8` while I understand than in production (Windows) I should use `esp_`_something_.
I've tried with just `esp` and apparently it works (the `locale.setlocale` command does not reject it).
However, when sending the string formated by `strftime`, if it cointains a non ASCII character (such as _«é»_ in _«miércoles»_ [Wednesday]) the method `reportlab.pdfgen.Canvas.drawString` is failing.

<sup>1.</sup> <sub>which are out of town and in remote locations, so I can access via LogMeIn through RF links or 3.5G, or by going physically to a place where I don't have all the available resources, so you probably understand that I would like to avoid as much tests as possible.</sub>
