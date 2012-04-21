all: elen.dic

elen.dic: greek.wl english.wl
	@./capitals_no_accent greek.wl gcaps.wl
	@sort -u gcaps.wl > greekcaps.wl
	@cat greek.wl greekcaps.wl english.wl > elen.wl
	@echo $$(wc -l elen.wl | awk '{ print $$1; }') > elen.lnum
	@cat elen.lnum elen.wl > elen.dic

install: elen.dic
	@mv elen.dic ../libregreek/dicts/

clean:
	@rm -f elen.lnum elen.wl gcaps.wl greekcaps.wl

distclean: clean
	@rm -f elen.dic

.PHONY: distclean clean install
