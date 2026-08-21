# Shared build configuration for every CV template.
#
# Each template lives in its own folder as <folder>/main.tex and refers to
# shared files as ../assets/<file>. Those paths resolve relative to the
# working directory, so builds must run from inside the template folder:
#
#     cd base && latexmk main.tex
#
# Each folder carries a one-purpose .latexmkrc that loads this file, so the
# settings below apply wherever the build is started from.
$lualatex   = 'lualatex -shell-escape -interaction=nonstopmode -synctex=1 -file-line-error %O %S';
$pdf_mode   = 4;    # 1=pdflatex, 4=lualatex, 5=xelatex
$bibtex_use = 1.5;  # run biber/bibtex whenever a bib source is present

# Every template uses biblatex + biber. BibTeX proper cannot be used here:
# under openout_any=p it refuses to write outside the document tree, so it
# cannot target the repository-root out/, and running it from the document
# directory instead makes ../assets/... resolve one level too deep. Biber
# has neither restriction.

# An undefined citation is a LaTeX warning, not an error, so latexmk would
# otherwise exit 0 while shipping a broken bibliography. Fail the build instead.
$warnings_as_errors = 1;

# All build output goes under the repository-root out/, which .gitignore
# already excludes. Every template is named main.tex, so they are kept in
# per-template subdirectories; a single shared directory would have them
# overwrite each other's main.pdf.
use Cwd qw(getcwd);
use File::Basename qw(basename);
$out_dir = '../../out/' . basename(getcwd());

# Clean targets (in addition to latexmk defaults)
$clean_ext = 'bcf run.xml synctex.gz synctex(busy) idx ind ilg acn acr alg glg glo gls ist nav snm vrb xdv';
