all: book

LATEXMK = latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=. -auxdir=auxdir

book: book.tex
	mkdir -p auxdir
	$(LATEXMK) book.tex
	sh auxdir/makechap.sh

clean:
	$(LATEXMK) -C book.tex
	rm -rf auxdir
