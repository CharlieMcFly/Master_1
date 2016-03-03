<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml"
    >
<xsl:output method="xml" indent="yes" encoding="UTF-8" omit-xml-declaration="no"/>
  <xsl:template match="/">
    <xsl:apply-templates select="championnat/clubs"/>
  </xsl:template>

  <xsl:template match="clubs">
    <clubs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <xsl:copy-of select="./club"/>
    </clubs>
  </xsl:template>

</xsl:stylesheet>
