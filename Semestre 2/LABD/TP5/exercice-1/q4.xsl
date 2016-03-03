<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml"
    >
<xsl:output method="xml" indent="yes" encoding="UTF-8" omit-xml-declaration="no"/>
  <xsl:template match="/">
    <xsl:apply-templates select="championnat/journees/journee">
      <xsl:with-param name="numj" select="18"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="journee">
    <xsl:param name="numj"/>
      <xsl:if test="$numj=./@num">
        <xsl:copy-of select="."/>
      </xsl:if>
  </xsl:template>

</xsl:stylesheet>
