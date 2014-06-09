NAME=cs224s

all: init markdown pdf 

init:
	mkdir -p build

markdown: problem related model dataset eval conc

problem: src/problem.md
	pandoc src/problem.md -o build/problem.tex

related: src/related.md 
	pandoc src/related.md -o build/related.tex

model: src/model.md
	pandoc src/model.md -o build/model.tex

dataset: src/dataset.md 
	pandoc src/dataset.md -o build/dataset.tex

eval: src/eval.md
	pandoc src/eval.md -o build/eval.tex

conc: src/conc.md
	pandoc src/conc.md -o build/conc.tex

pdf: template/template.tex
	cp template/sig-alternate.cls ./
	pdflatex template/template.tex
	bibtex template
	pdflatex template/template.tex
	pdflatex template/template.tex
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f sig-alternate.cls
	mv template.pdf proposal.pdf
	echo 'Compiled document: proposal.pdf'

clean:
	rm -rf build/*
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f *.log *.aux *.out *.bbl *.blg
	rm -f sig-alternate.cls
	