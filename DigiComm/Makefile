all: DigitalCommunication

DigitalCommunication: DigitalCommunication.tex
	latex DigitalCommunication.tex
	makeindex DigitalCommunication.idx
	latex DigitalCommunication.tex
	dvips -Ppdf -G0 -o DigitalCommunication.ps DigitalCommunication.dvi
	ps2pdf -dEmbedAllFonts=true DigitalCommunication.ps DigitalCommunication.pdf

clean:
	rm -f *.idx *.aux *.dvi *.log *.ps DigitalCommunication.pdf
