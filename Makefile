#!/usr/bin/bash
all: vopros bilet


vopros:
	cd src && pdflatex voprosnik.tex


bilet:
	python split_questions.py >BILETY.tex
	pdflatex BILETY.tex

clean:
	rm *.log *.aux
	cd src && rm *.log *.aux
