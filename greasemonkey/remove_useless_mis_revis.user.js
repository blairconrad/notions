// ==UserScript==
// @name           Remove Useless MIS Revised Modules
// @namespace      mist.mitra.com
// @include        https://*mist.agfa.net*/MISCore/importsproduct/cvsmanager.asp*
// ==/UserScript==

var pattern = '_impax64gtrse_';

var versionNames = document.getElementsByTagName('SELECT');
var dropdown = null;
for( var i = 0; i < versionNames.length; i++ )
{
	if(versionNames[i].name == "VERSION_NAME")
	{
	    dropdown = versionNames[i];

		if (dropdown != null) 
		{
			var items = dropdown.length;
			var x = 0;
			var pointer = 0;
			while(x < items)
			{
            		    var element = dropdown[pointer];
	    		    if ( ( element.innerHTML.indexOf(pattern) < 0 ) &&
	    			 ( element.innerHTML != 'No version selected' ) )
                            {
		    		dropdown.removeChild(dropdown[pointer]);
                            }
	    		    else
	    		    {
		    		pointer = pointer + 1;
	    		    }
	    		    x++;
			}
		}
	}
}


