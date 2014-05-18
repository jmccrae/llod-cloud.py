<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <!-- for SVG exported by yed from GraphML -->
	
	<!-- (a) bring nodes to front, then edges -->
    <xsl:template match="*[name()='g']">
        <xsl:copy>
            <xsl:for-each select="@*">
                <xsl:copy/>
            </xsl:for-each>
            <xsl:apply-templates select="text()|comment()|*[name()!='g']"/>
            <xsl:apply-templates select="*[name()='g' and not(contains(@id,'edge')) and not(contains(@id,'node'))]"/>
            <xsl:apply-templates select="*[name()='g' and contains(@id,'edge')]"/>
            <xsl:apply-templates select="*[name()='g' and contains(@id,'node')]"/>
        </xsl:copy>
    </xsl:template>
    
	<!-- (b) replace datahub API URLs by data URLs -->
	<xsl:template match="*[name()='a']">
		<xsl:text disable-output-escaping="yes">&lt;a</xsl:text>
			<xsl:for-each select="@*">
				<xsl:text> </xsl:text>
				<xsl:value-of select="name(.)" disable-output-escaping="yes"/>
				<xsl:text disable-output-escaping="yes">="</xsl:text>
				<xsl:choose>
					<xsl:when test="contains(name(),'href') and contains(.,'http://datahub.io/api')">
						<xsl:text>http://datahub.io/dataset/</xsl:text>
						<xsl:value-of select="substring-after(.,'id=')"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="."/>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:text disable-output-escaping="yes">"</xsl:text>
			</xsl:for-each>
			<xsl:text disable-output-escaping="yes">></xsl:text>
			<xsl:apply-templates/>
		<xsl:text disable-output-escaping="yes">&lt;/a></xsl:text>
	</xsl:template>
	
	<!-- (c) eliminate superfluous blank lines -->
    <xsl:template match="text()">
        <xsl:if test="normalize-space(.)!=''">
            <xsl:copy-of select="."/>
        </xsl:if>
    </xsl:template>
    
	<!-- (d) keep everything else -->
    <xsl:template match="/|*[name()!='g' and name()!='a']|comment()|@*|processing-instruction()">
        <xsl:copy>
            <xsl:for-each select="@*">
                <xsl:copy/>
            </xsl:for-each>
            <xsl:apply-templates/>
        </xsl:copy>
        <xsl:text>
        </xsl:text>
    </xsl:template>
</xsl:stylesheet>
