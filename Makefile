gospels.pdf: all.htm gospels.css
	../bin/prince all.htm \
		--style=gospels.css \
		--output=gospels.pdf \
		--no-default-style

preface.pdf: preface.htm gospels.css
	../bin/prince preface.htm \
		--style=gospels.css \
		--output=preface.pdf \
		--no-default-style

gospels.no-bleed.pdf: gospels.htm gospels.css gospels.no-bleed.css
	../bin/prince gospels.htm \
		--style=gospels.no-bleed.css \
		--output=gospels.no-bleed.pdf \
		--no-default-style

all.htm: preface.htm gospels.htm
	cat preface.htm gospels.htm > all.htm

gospels.htm: gospels.raw.htm cleanup.py doubles.txt paragraphs.txt next-line.txt phrases.txt
	python cleanup.py

gospels.raw.htm:
	cat webhtm/Mark.htm \
	    webhtm/Matthew.htm \
	    webhtm/Luke.htm \
	    webhtm/John.htm \
	    > gospels.raw.htm
