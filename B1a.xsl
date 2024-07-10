<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="html" encoding="UTF-8"/>
 
  
    <xsl:template match="tei.TEI">   
    <html>
  <body>
    <h2>Mamys Briefe</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>adrnr</th>
        <th>Name</th>
        <th>Geschlecht</th>
      </tr>
      <xsl:for-each select="text/body/div/p">
        <tr>
          <td><xsl:value-of select="persName" /> </td>
        </tr>  
      </xsl:for-each>
      
    </table>
    
    
    
    
  </body>
  </html>  
 </xsl:template>
    
 
</xsl:stylesheet>



