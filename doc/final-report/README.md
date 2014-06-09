Final Report
====

How to compile it
----

- Be sure you have pandoc on your computer.
  - For mac: download DMG file at code.google.com/p/pandoc/downloads/
- Run "make all".


How to add your work
----

- Put your section under "src/". Never under "tex/".
- Modify "Makefile" to add rules for your section.
- Modify "template/template.tex" to add inputs for your section.


Directory Structure
----

.
├── Makefile          -- Modify this when added new sections
├── README.md
├── fixbib.sty
├── src                 -- All source files (md / tex / bib) are here
├── template            -- AAAI template files.
│   └── template.tex    -- Modify this when added new sections
└── tex                 -- Output only -- DO NOT MODIFY FILES IN THIS! 
