all: libregreek.oxt

libregreek.oxt:
	@cd libregreek ; zip -r -q ../libregreek.oxt .

clean:
	@rm -f libregreek.oxt

.PHONY: clean
