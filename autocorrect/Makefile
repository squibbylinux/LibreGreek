all: acor-el_GR.dat

acor-el_GR.dat:
	@cd acor-el ; zip -r -q ../acor_el-GR.dat .

install:
	@mv acor_el-GR.dat ../libregreek/autocorr/

clean:
	@rm -f acor_el-GR.dat

.PHONY: clean install
