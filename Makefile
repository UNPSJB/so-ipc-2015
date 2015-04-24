BASEFILE=SO_TP4_Guia
all: slides

slides: ${BASEFILE}.slides.html

latex: ${BASEFILE}.tex

pdf: SO_TP4_Guia.pdf 

slides-open:
	open ${BASEFILE}.slides.html

html: ${BASEFILE}.html

%.slides.html: %.ipynb
	ipython nbconvert --to slides $^


%.html: %.ipynb
	ipython nbconvert --to html $^

%.tex: %.ipynb
	ipython nbconvert --to latex $^

%.pdf: %.tex
	pdflatex $^
	# Remplazar los query de las url estaticas puestos para invalidar cache
	sed -i '' 's/png\?.*\}/png\}/g'  *.tex
