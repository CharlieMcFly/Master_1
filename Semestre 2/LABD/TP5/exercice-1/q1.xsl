<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml"
    >
<xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="no"/>

  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <body>
        <h3>Un club de Ligue 1 <br/> saison
        	<xsl:value-of select="(/championnat/@annee)-1"/>-<xsl:value-of select="/championnat/@annee"/> :
        </h3>
        <p/>
        <xsl:value-of select=".//ville[1]"/>
    </body>
   </html>
  </xsl:template>

</xsl:stylesheet>
