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
    <clubs>
      <xsl:apply-templates select="club"/>
    </clubs>
  </xsl:template>

  <xsl:template match="club">
      <club>
        <nom><xsl:value-of select="nom"/></nom>
        <ville><xsl:value-of select="ville"/></ville>
        <rencontres>
          <xsl:apply-templates select="rencontres">
            <xsl:with-param name="clubid" select="@id"/>
          </xsl:apply-templates>
        </rencontres>
      </club>
  </xsl:template>

  <xsl:template match="rencontres">
    <xsl:param name="clubid"/>
    <domicile>
      <xsl:apply-templates select="rencontre">
        <xsl:with-param name="clubid2" select="clubid"/>
        <xsl:with-param name="domicile" select="dom"/>
      </xsl:apply-templates>
    </domicile>
    <exterieur>
      <xsl:apply-templates select="rencontre">
        <xsl:with-param name="clubid2" select="clubid"/>
        <xsl:with-param name="domicile" select="ext"/>
      </xsl:apply-templates>
    </exterieur>
  </xsl:template>

  <xsl:template match="rencontre">
        <xsl:param name="clubid2"/>
        <xsl:param name="domicile"/>
        <xsl:if test="$domicile=dom">
          <xsl:if test="$clubid2=./receveur">
            <rencontre>
              <club>
                <xsl:apply-templates select="clubname">
                    <xsl:with-param name="clubid3" select="./invite"/>
                 </xsl:apply-templates>
              </club>
              <score><xsl:value-of select="score"/></score>
            </rencontre>
          </xsl:if>
        </xsl:if>

        <xsl:if test="$domicile=ext">
          <xsl:if test="$clubid2=./invite">
            <rencontre>
              <club>
                <xsl:apply-templates select="clubname">
                    <xsl:with-param name="clubid3" select="./receveur"/>
                 </xsl:apply-templates>
              </club>
              <score><xsl:value-of select="score"/></score>
            </rencontre>
          </xsl:if>
        </xsl:if>
  </xsl:template>

  <xsl:template match="clubname">
        <xsl:param name="clubid3"/>
        <xsl:value-of select="//club[./@id=clubid3]/nom"/>
  </xsl:template>

</xsl:stylesheet>

