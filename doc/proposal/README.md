Proposal Directory
====

How to compile it
----

- Be sure you have pandoc on your computer.
  - [Install pandoc with binary](https://code.google.com/p/pandoc/downloads/list)
- Run "make all".


How do I add my work
----

- Put your section under "src/". Never under "build/".
- Modify "Makefile" to add rules for your section.
- Modify "template/templateacm.tex" to add inputs for your section.
- We can also change to other templates.

Directory Structure
----

    .
    ├── Makefile    -- Modify this when added new sections
    ├── README.md
    ├── build       -- Output only. DO NOT MODIFY FILES, WILL BE OVERWRITTEN!
    │   ├── conc.tex
    │   ├── dataset.tex
    │   ├── intro.tex
    │   ├── model.tex
    │   └── related.tex
    ├── proposal.pdf    -- generated output
    ├── src         -- All source files (md / tex / bib) are here
    │   ├── conc.md
    │   ├── dataset.md
    │   ├── intro.md
    │   ├── model.md
    │   ├── related.bib
    │   └── related.md
    └── template    -- Modify this when added new sections
        ├── sig-alternate.cls
        └── templateacm.tex

