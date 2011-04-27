gospels.pdf: gospels.htm gospels.css
	../bin/prince gospels.htm \
		--style=gospels.css \
		--output=gospels.pdf \
		--no-default-style

gospels.htm: gospels.raw.htm cleanup.py doubles.txt paragraphs.txt next-line.txt
	python cleanup.py

gospels.raw.htm:
	cat webhtm/Mark.htm \
        webhtm/Matthew.htm \
        webhtm/Luke.htm \
        webhtm/John.htm \
        > gospels.raw.htm
