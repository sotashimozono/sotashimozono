# Inherit the shared configuration in cv/.latexmkrc.
#
# Plain `do '../.latexmkrc'` is not used: Perl searches @INC for relative
# paths and would silently no-op, leaving the build without the biber and
# warnings-as-errors settings. Read and eval the file explicitly instead,
# so a missing or broken shared rc fails loudly.
my $shared = '../.latexmkrc';
die "cv/.latexmkrc not found: run latexmk from inside a template folder\n"
    unless -e $shared;
open my $fh, '<', $shared or die "cannot read $shared: $!\n";
my $rc = do { local $/; <$fh> };
close $fh;
eval $rc;
die "failed to load $shared: $@" if $@;
