#!/usr/bin/perl

my $brfnr = $ARGV[0];
printf "erzeuge html von Brief Nr. %d\n",$brfnr;

`java -jar saxon-he-10.3.jar -o:A$brfnr.html A$brfnr.xml A78a.xsl`;
