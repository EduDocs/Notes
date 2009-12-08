all: book

book: book.tex
	pdflatex book.tex
	makeindex book.idx
	pdflatex book.tex

clean:
	rm -f *.idx *.aux *.dvi *.log *.ps book.pdf
