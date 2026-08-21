# CV

## Layout

```plaintext
cv/
  .latexmkrc          shared build configuration
  assets/             files shared by every template
    references.bib      publications (single source of truth)
    few-ref.bib         sample bibliography (upstream template data)
    many-ref.bib        sample bibliography (upstream template data)
    dwight.png          sample portrait (upstream template data)
  base/main.tex       general CV
  academic/main.tex   academic CV
  fancy/main.tex      upstream sample
  office/main.tex     upstream sample
```

One folder per document, each holding a `main.tex`. Shared files live in
`assets/` and are referenced as `../assets/<file>`.

## Building

Run latexmk from inside the template folder:

```sh
cd base && latexmk main.tex
```

`../assets/...` paths resolve relative to the working directory, so the build
must start there. Each folder carries a small `.latexmkrc` that loads the
shared `cv/.latexmkrc`, so the settings apply wherever the build is started.

Output goes to the repository-root `out/<template>/`, which `.gitignore`
excludes. Every template is named `main.tex`, hence the per-template
subdirectory.

## Constraints worth knowing

**Bibliographies use biblatex + biber, never BibTeX.** Under TeX Live's
default `openout_any = p`, BibTeX refuses to write outside the document tree,
so it cannot target the repository-root `out/`. Running it from the document
directory instead makes `../assets/...` resolve one level too deep. Biber has
neither restriction.

**The build fails on warnings.** `$warnings_as_errors = 1` is set because an
undefined citation is only a LaTeX warning: without it, latexmk exits 0 while
producing a CV with a raw citation key printed in place of the reference.

**Do not use `\pdfgentounicode`.** It is a pdfTeX primitive that does not
exist in LuaTeX, so it raises an undefined control sequence and typesets a
stray `=1` at the top of the page. LuaTeX embeds ToUnicode maps anyway.

## Acknowledgements

Templates are derived from [rover-resume](https://github.com/subidit/rover-resume).
`fancy/` and `office/` are close to the original; `base/` and `academic/` have
been rewritten.
