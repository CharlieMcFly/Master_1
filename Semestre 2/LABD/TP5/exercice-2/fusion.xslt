<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="2.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://labd/art"
	xpath-default-namespace="http://labd/art">

	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="/">
		<art  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			<artistes>
				<xsl:for-each select="//artiste">
					<artiste>
						<xsl:variable name="nom" select="./nom"/>
						<xsl:variable name="prenom" select="./prénom"/>
						<nom>
							<xsl:value-of select="./nom"/>
						</nom>
							<xsl:copy-of select="./période"/>
							<xsl:for-each select="document('catalogue-1.xml')//oeuvre[.//nom = $nom and .//prénom =$prenom]">
								<oeuvre>
									<titre>
										<xsl:value-of select="./titre"/>
									</titre>
									<genre>
										<xsl:value-of select="./genre"/>
									</genre>
									<date>
										<xsl:value-of select="./date"/>
									</date>
								</oeuvre>
							</xsl:for-each>
					</artiste>
				</xsl:for-each>
			</artistes>
			<mouvements>
				<xsl:for-each select="//mouvement">
					<xsl:variable name="nommvt" select="./nom"/>
					<mouvement>
						<xsl:copy-of select="//mouvement"/>
					</mouvement>
				</xsl:for-each>
			</mouvements>
		</art>
	</xsl:template>
</xsl:stylesheet>
