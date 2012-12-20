Libre Greek -- Libre Office extension
=====================================

This is an effort to collect the best support material for the
Greek language that the Greek FOSS community has produced so far
for Libre Office into a single project to make them easier to
find and maintain.

I 'm starting with:

      * The combined English/Greek dictionary from the Firefox
        extension of Kostas Papadimas (updated with latest wordlist
        from elspell project)

      * Thesaurus from the new OpenThesaurus.gr 

      * Hyphenation rules for Greek by InterZone

      * The OpenOffice templates that were translated to Greek
        during Greek Coding Camp 2009.

      * Autocorrect files from Lefteris Thanos.

And the hope is to continue with more material like grammar
correction etc etc.

Although credit for the content goes to the respective authors,
the packaging is done by us, Squibby Linux Team and we take full
responsibility for it, so please forward any issues / complaints
to us (public at chania-lug.gr).

Build
=====

cd autocorrect ; make ; make install

cd ../makedict ; make ; make install

cd ..;           make 

and use the resulting libregreek.oxt extension
