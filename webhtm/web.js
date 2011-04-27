/* Javascript code for the World English Bible. http://WorldEnglishBible.org/ */
/* For "javascript disabled" message in HTML file */
function jsmissingbegin()
{
	document.write("<div style=\"display: none\">");
}
function jsmissingend()
{
	document.write("</div>");
}
function cj(chapter, verse)
{ /* Write a chapter-verse marker within a quotation of Jesus Christ */
	document.write("</span> <a name=\"C"+chapter+"V"+verse+"\" class=\"cv\">"+chapter+":"+verse+"</a> <span class=\"j\">");
}
function cb(chapter, verse)
{ /* Write a chapter-verse marker */
	document.write("</span> <a name=\"C"+chapter+"V"+verse+"\" class=\"cv\">"+chapter+":"+verse+"</a> <span class=\"b\">");
}
function xd()
{
    document.write("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
}
