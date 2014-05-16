<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <!-- for SVG exported by yed from GraphML: move edges behind nodes, i.e., write edges first, then nodes -->
    
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
    
    <xsl:template match="text()">
        <xsl:if test="normalize-space(.)!=''">
            <xsl:copy-of select="."/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="/|*[name()!='g']|comment()|@*|processing-instruction()">
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
