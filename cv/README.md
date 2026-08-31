# CV

## Layout

```plaintext
cv/
  templates.json      which templates exist, and which ones ship
  .latexmkrc          shared build configuration
  assets/             files shared by every template
    publications.bib    papers
    oral.bib            talks
    poster.bib          posters
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

## Which templates ship

`templates.json` is the single source of truth for the template list; no
template is named in the workflow.

```json
{ "dir": "academic", "publish": true, "asset": "sota-shimozono-cv-academic.pdf" }
```

Every directory holding a `main.tex` must appear in it, and CI fails if the two
disagree in either direction. Without that check a new template could sit in
`cv/` unbuilt while the run stayed green, leaving a stale PDF on the release.

`publish: true` uploads the PDF to the rolling `cv-latest` release under
`asset`, which has to be unique because every template builds to `main.pdf`.
`publish: false` builds the template as a regression check and stops there.
The download URL does not change between builds:

```plaintext
https://github.com/sotashimozono/sotashimozono/releases/download/cv-latest/<asset>
```

The file is JSON rather than YAML or TOML because the workflow reads it with
`jq` and feeds the build matrix through `fromJSON`, neither of which needs a
setup step on the runner.

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
