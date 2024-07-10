<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="html" encoding="UTF-8"/>
  
 
  <xsl:template match="root">
    <html>
      <head>
        
        <title>Test Document</title>
        </head>
      <body>
        <link rel="stylesheet"  href="../A2.css">
      <xsl:apply-templates/>
        </link> 
</body>
    </html>
  </xsl:template>  
  
  <xsl:template match="text/div">
    <xsl:apply-templates/>
  </xsl:template>  
  
    <xsl:template match="lb">
      <br>
      <xsl:apply-templates/>
        </br>
  </xsl:template>  
  

  
  <xsl:template match="persName">

      <xsl:variable name="adrnr"  select="@key"/>
      <xsl:variable name="anr"  select="substring($adrnr,3)"/>
     <a href="../../../ahn/ahn.php?anr={$anr}">
    <xsl:apply-templates/>
</a>
    
  </xsl:template>  
  
    <xsl:template match="pb">

      <xsl:variable name="ref"  select="@facs"/>
      <xsl:variable name="original"  select="substring($ref,2)"/>
     <img src="../images/Mamy/{$original}.jpg">
    <xsl:apply-templates/>
</img>
    
  </xsl:template>  
  
  
 
 
</xsl:stylesheet>
