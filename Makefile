BASEFILE=SO_TP4_Guia
all: slides

slides: ${BASEFILE}.slides.html

slides-open:
	open ${BASEFILE}.slides.html

html: ${BASEFILE}.html

%.slides.html: %.ipynb
	ipython nbconvert --to slides $^


%.html: %.ipynb
	ipython nbconvert --to html $^
