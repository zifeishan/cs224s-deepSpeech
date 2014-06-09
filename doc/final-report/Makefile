NAME=DeepSpeech

all: markdown pdf 

markdown: abstract intro related model algo eval conc

abstract: src/abstract.md
	pandoc src/abstract.md -o build/abstract.tex

intro: src/intro.md
	pandoc src/intro.md -o build/intro.tex

related: src/related.md 
	pandoc src/related.md -o build/related.tex

model: src/model.md
	pandoc src/model.md -o build/model.tex

algo: src/algo.md
	pandoc src/algo.md -o build/algo.tex

eval: src/eval.md
	pandoc src/eval.md -o build/eval.tex

conc: src/conc.md
	pandoc src/conc.md -o build/conc.tex

pdf: template/templateis13.tex
	cp template/interspeech2013.sty ./
	pdflatex template/templateis13.tex
	bibtex templateis13
	pdflatex template/templateis13.tex
	pdflatex template/templateis13.tex
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f interspeech2013.sty
	mv templateis13.pdf cs224s-final-report.pdf

clean:
	rm -rf build/*
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f sig-alternate.cls
	