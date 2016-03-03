<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="2.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://labd/art"
	xpath-default-namespace="http://labd/art">

	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="/">
	<artistes>
		<xsl:for-each select="//artiste">
			<artiste>
				<xsl:variable name="nom" select="./nom"/>
				<xsl:variable name="prenom" select="./prénom"/>
				<nom>
					<xsl:value-of select="./nom"/>
				</nom>
				<prenom>
					<xsl:value-of select="./prénom"/>
				</prenom>
				<nb-oeuvres>
					<xsl:value-of select="count(document('catalogue-1.xml')//oeuvre[.//nom = $nom and .//prénom =$prenom])"/>
				</nb-oeuvres>
			</artiste>
		</xsl:for-each>
	</artistes>
	</xsl:template>

</xsl:stylesheet>
