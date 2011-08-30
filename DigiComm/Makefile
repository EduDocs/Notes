all: book

book: book.tex
	latex book.tex
	makeindex book.idx
	latex book.tex
	dvips -Ppdf -G0 -o book.ps book.dvi
	ps2pdf -dEmbedAllFonts=true book.ps book.pdf

clean:
	rm -f *.idx *.aux *.dvi *.log *.ps book.pdf
