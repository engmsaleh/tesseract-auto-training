Tesseract auto-training
=======================

Project homepage: [github.com](https://github.com/zdenop/tesseract-auto-training)

Download current (devel) source: [tar.gz](https://github.com/zdenop/tesseract-auto-training/tarball/master) or [zip](https://github.com/zdenop/tesseract-auto-training/zipball/master)

Licence: Code is released under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Other files (e.g. fonts) can have its own licenses.


DESCRIPTION
-----------

This is attempt to create python scripts for automatic tesseract traning.
Scripts are based on script from project [tesseractindic tesseract_trainer](http://code.google.com/p/tesseractindic/source/browse/#svn/trunk/tesseract_trainer)


REQUIREMENTS
-----------

* Python (tested on 2.6.6)
* tesseract (tested on 3.00)


USAGE
-----

`python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>`

**Example:**
	`generate.py -font mitra -l beng -s 10 -a beng.alphabet/`
	`generate.py -font Courier -l eng -s 10 -a eng.alphabet/`
	`generate.py -font Arial -l slk -s 10 -a slk.alphabet/`
