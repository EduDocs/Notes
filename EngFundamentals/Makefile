all: book

book: book.tex
	pdflatex book.tex
	makeindex book.idx
	pdflatex book.tex

clean:
	rm -f *.aux *.dvi *.log *.ps book.pdf
