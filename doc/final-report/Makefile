NAME=DeepSpeech

all: markdown pdf 

markdown: abstract introduction model features architecture experiments related conclusion

abstract: src/abstract.md
	pandoc src/abstract.md -o build/abstract.tex

introduction: src/introduction.md
	pandoc src/introduction.md -o build/introduction.tex

related: src/related.md 
	pandoc src/related.md -o build/related.tex

model: src/model.md
	pandoc src/model.md -o build/model.tex

features: src/features.md
	pandoc src/features.md -o build/features.tex

architecture: src/architecture.md
	pandoc src/architecture.md -o build/architecture.tex

experiments: src/experiments.md
	pandoc src/experiments.md -o build/experiments.tex

conclusion: src/conclusion.md
	pandoc src/conclusion.md -o build/conclusion.tex

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
	