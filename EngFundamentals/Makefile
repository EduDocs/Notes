all: book

book: book.tex
	pdflatex book.tex
	bibtex book
	makeindex book.idx
	pdflatex book.tex
	pdflatex book.tex
	sh makechap.sh

clean:
	rm -f *.idx *.aux *.dvi *.log *.ps book.pdf
