#!/usr/bin/perl

for ($i=321; $i<487; $i++) {
    printf ("java -jar saxon-he-10.3.jar -o:A%d.html A%d.xml A78a.xsl\n",$i,$i)
}
