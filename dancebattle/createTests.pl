#!/usr/bin/perl

my $i = 5;

for (0..19) {
    my $cmd = "java Test $i $_ > tests/$i.$_.in";
    print "$cmd\n";
    system($cmd);
}
