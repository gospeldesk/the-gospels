gospels.pdf: gospels.htm gospels.css
	../bin/prince gospels.htm \
		--style=gospels.css \
		--output=gospels.pdf \
		--no-default-style

gospels.no-bleed.pdf: gospels.htm gospels.css gospels.no-bleed.css
	../bin/prince gospels.htm \
		--style=gospels.no-bleed.css \
		--output=gospels.no-bleed.pdf \
		--no-default-style

gospels.htm: gospels.raw.htm cleanup.py doubles.txt paragraphs.txt next-line.txt
	python cleanup.py

gospels.raw.htm:
	cat webhtm/Mark.htm \
        webhtm/Matthew.htm \
        webhtm/Luke.htm \
        webhtm/John.htm \
        > gospels.raw.htm
