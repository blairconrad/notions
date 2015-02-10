// Conquer Club - Card Counter, Card Redemption Value, Status Indicator
// version 0.52 BETA!
//-----------------------------------------------------------------------------
//	Installation
//-----------------------------------------------------------------------------
// This is a Greasemonkey user script.
//
// To install, you need Greasemonkey: http://greasemonkey.mozdev.org/
// Then restart Firefox and revisit this script.
// Under Tools, there will be a new menu item to "Install User Script".
// Accept the default configuration and install.
//
// To uninstall, go to Tools/Manage User Scripts,
// select "Conquer Club", and click Uninstall.
//
//-----------------------------------------------------------------------------
//	Description
//-----------------------------------------------------------------------------
// * Adds card redemption values
// * Adds dynamic countdown timer
// * Adds statistics
// * Automatically Jumps to map.
//-----------------------------------------------------------------------------
//	Notes
//-----------------------------------------------------------------------------
// * The status indicator isn't always accurate. It goes yellow when a player
//   receives men, and red when they fortify, and back to green when a new round
//   is started.
// * Armies per turn DOES NOT INCLUDE BONUSES.. so no continent bonuses.
// * Strength =  # Armies + Potential Armies - ( 2/3 * # Countries )
//-----------------------------------------------------------------------------
//	Meta Data
//-----------------------------------------------------------------------------
// ==UserScript==
// @name		Conquer Club
// @namespace	http://personal.ecu.edu/tnt1202/conquerclub.user.js
// @description   Adds card counter, redemption value, and user status
// @include       http://*conquerclub.com*
// ==/UserScript==
//-----------------------------------------------------------------------------
//	USER SETTINGS
//-----------------------------------------------------------------------------
var OPTIONS = new Object();
OPTIONS['jumptomap'] = true;
OPTIONS['colorblind'] = false;
OPTIONS['focuscolor'] = '#C00';
//-----------------------------------------------------------------------------
//	DO NOT EDIT BELOW THIS ( unless you know what you are doing )
//-----------------------------------------------------------------------------
function gm_ConquerClubGame(OPTIONS){
	/*---- Check for Required Components ----*/
	var log = document.getElementById('log');
	var rightside = document.getElementById('right_hand_side');
	var dashboard = document.getElementById('dashboard');
	var map = document.getElementById('inner-map');

	//If we cannot find any of the following just quit out.
	if( !( log && rightside && dashboard && map ) ) return;

	/*---- Prototyping ----*/
	String.prototype.has = function(key) { return this.indexOf(key) > -1; }

	/*---- Object Stuff ----*/

	//Player Status
	var eStatus = { GREEN:0, YELLOW:1, RED:2, UNKNOWN:3, WINNER:4, LOSER:5 }

	//Player Class
	function Player( name, pid, color ){
		this._name = name;
		this._pid = pid;
		this._color = color;
		this._cards = 0;
		this._armies = 0;
		this._countries = 0;
		this.toString = function() { return this._name; }

		this.getArmiesPerTurn = function() { if( this._countries < 12 ) return 3; return Math.floor(this._countries/3); }
		this.getTurninP = function() { if( this._cards < 3 ) return 0; if( this._cards > 4 ) return 1; if( this._cards == 3 ) return 0.3341; return 0.778; }
		this.alert = function() {
			alert(	"Name:\t"			+	this._name		+
					"\nPID:\t"			+	this._pid		+
					"\nCards:\t"		+	this._cards		+
					"\nArmies:\t"		+	this._armies	+
					"\nCountries:\t"	+	this._countries +
					"\nArmies/Turn:\t"  +	this.getArmiesPerTurn()
			);
		}
	}
	
	//Game Enumerations
	var eGameType = { STANDARD:0, DOUBLES:2, TRIPLES:3 }
	var ePlayOrder = { NDTFREESTYLE: 0, FREESTYLE:1, SEQUENTIAL:2 }
	var eBonusCards = { NOCARDS:0, FLATRATE:1, ESCALATING:2 }
	//-------------------------------------------------------------------------
	//	VARIABLE DECLARATIONS
	//-------------------------------------------------------------------------

	/*---- Gameplay ----*/
	var num_turnins = 0;
	var num_players = 0;
	var m_gameType;
	var m_playOrder;
	var m_bonusCards;
	var RedemptionValue;

	/*---- Statistics ----*/
	var totalArmies = 0;
	var totalCountries = 0;

	/*---- Player ----*/
	var pl = new Array(); // will hold my players
	var NID = 0; // Neutral ID
	var pl_Colors = new Array("666","f00","090","00f","cc0","0cc","f0f");//Player Colors
	var pl_cbIDs = new Array("n","r","g","b","y","t","p"); //Color Blind Identifiers

	/*---- Clock ----*/
	var today = new Date();
	var time = new Array();// { hh, mm, ss }
	var timeStr;
	var timeLocStr = rightside.innerHTML.has('<span class="countdown-alert">')?'<h4>Time Remaining</h4><span class="countdown-alert">':'<h4>Time Remaining</h4>';
	var timeLoc;//location of the time
	var timeindexOffset;//location of the time + the index ( hr, min, or sec )
	var timeWIDTH = 18;
	var clockInterval;

	/*---- Misc ----*/
	var i;
	var tmp;
	var re;
	var pid; // player identifier
	var name; // tmp name

	//-------------------------------------------------------------------------
	//	FUNCTIONS
	//-------------------------------------------------------------------------
	
	// Altered to allow partial matches... player matches player1 ... 2 etc.
	var getElementsByClassName = function (oElm, strTagName, strClassName){
	    var arrElements = (strTagName == "*" && document.all)? document.all : oElm.getElementsByTagName(strTagName);
	    var arrReturnElements = new Array();
	    strClassName = strClassName.replace(/\-/g, "\\-");
	    var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s)");
	    var oElement;
	    for(var i=0; i<arrElements.length; i++){
	        oElement = arrElements[i];
	        if(oElement.className.has(strClassName)){
	            arrReturnElements.push(oElement);
	        }
	    }
	    return (arrReturnElements)
	}
	
	var countDown = function(){
		var hrs = document.getElementById('hrs');
		var mins = document.getElementById('min');
		var secs = document.getElementById('sec');

		if( --secs.value < 0 ){
			if( --mins.value < 0 ){
				if( --hrs.value < 0 ){
					hrs.value = 0;
					if( mins.value <= 0 && secs.value <= 0 ){
						clearInterval(clockInterval);//No more counting down
						//No weird negative #s
						mins.value = 0;
						secs.value = 0;

						document.getElementById('countdown').innerHTML = "<b><font color=red>NEW ROUND STARTED!<br />Click Refresh Map</font></b>";
						//window.location.reload();
						return;
					}
				}
				mins.value = 59;
			}
			secs.value = 59;
		}
	}
	var calcRedemption = function(){
		if( m_bonusCards == eBonusCards.ESCALATING ){
			if( num_turnins < 5 ) return num_turnins * 2 + 4;
			else return num_turnins * 5 - 10;
		} else if( m_bonusCards == eBonusCards.FLATRATE) return 7;
		return 0; //no cards
	}
	var calcArmiesNextTurn = function(countries){
		if( countries < 12 ) return 3;
		return Math.floor(countries/3);
	}

	/*---- Returns probability of a tunin - http://www.kent.ac.uk/IMS/personal/odl/riskfaq.htm#3.5 ----*/
	var getTurnInP = function(num_cards){
		if( num_cards < 3 ) return 0;
		if( num_cards > 4 ) return 1;
		if( num_cards == 3 ) return 0.3341;
		return 0.778; // has 4 cards
	}

	//-------------------------------------------------------------------------
	//	INIT
	//-------------------------------------------------------------------------

	/*---- Start Clock ----*/
	tmp = rightside.innerHTML.indexOf(timeLocStr);//to make sure there is a clock.
	if( tmp > -1 ){
		timeLoc = tmp + timeLocStr.length + 1;
		tmp = rightside.innerHTML;
		timeStr = tmp.substring(timeLoc,timeLoc + timeWIDTH);
		re = new RegExp( timeStr );//Replace time
		time = timeStr.split(/hrs\n|min\n|sec\n/);

		var formAttr = "style=text-align:right;width:1.2em;border:none;background:#eee; size=1 maxlength=2 type=text";
		timeStr = '<form><input '+formAttr+' id=hrs value='+time[0]+'> hrs <input '+formAttr+' id=min value='+time[1]+'> min <input '+formAttr+' id=sec value='+time[2]+'> sec</form>';

		rightside.innerHTML = tmp.replace(re,"<div id=countdown>" + timeStr + "</div>");

		clockInterval = window.setInterval(countDown,1000);
	}
	/*---- Create Divisions ----*/
	var stats = document.createElement('div');
	dashboard.parentNode.insertBefore(stats, log.previousSibling.previousSibling);
	stats.style.margin = '10px 0 0 0';

	/*---- Cleanup Log ----*/
	var log = log.innerHTML;
	log = log.split('<br>');//Splits Each line.

	/*---- Get Game Modes ----*/
	if( dashboard.innerHTML.has("Sequential") ) m_playOrder = ePlayOrder.SEQUENTIAL;
	else {
		if( dashboard.innerHTML.has("Freestyle (no double turns)") )
			m_playOrder = ePlayOrder.NDTFREESTYLE;
		else
			m_playOrder = ePlayOrder.FREESTYLE;
		dashboard.innerHTML = dashboard.innerHTML.replace("double turns","dbl turns");
		rightside = document.getElementById('right_hand_side');//DONT REMOVE THIS LINE! :-(

	}

	/*---- Get Player Names ----*/
	pl["Neutral"] = new Player("Neutral",NID,pl_Colors[NID]);
	tmp = getElementsByClassName(rightside,"span","player");	
	for( i in tmp )
		if( tmp[i].innerHTML )
			pl[tmp[i].innerHTML] = new Player(tmp[i],++num_players,pl_Colors[i]);

	/*---- Calculate Cards & Player Status ----*/

	for( i = 0; i < log.length; i++ ){
		if( log[i].has(" gets a card") ){
			name = log[i].split(/<[^>]*>/)[1];
			pl[name]._cards += 1;
		}
		else if( log[i].has(" fortified ") || log[i].has(" ran out of time") || log[i].has(" missed a turn") ){
		}
		else if( log[i].has(" cashed") ){
			pl[ log[i].split(/<[^>]*>/)[1] ]._cards -= 3;
			num_turnins++;
		}
		else if( log[i].has(" eliminated ") ){
			var tmp = log[i].split(/<[^>]*>/);
			pl[ tmp[1] ]._cards += pl[tmp[3]]._cards;//conquerer gets losers cards
			pl[ tmp[3] ]._cards = 0;
			//pl[ tmp[3] ]._status = eStatus.LOSER;
		}
		else if( log[i].has(" gains ") ){
			//pl[ log[i].split(/<[^>]*>/)[1] ]._status = eStatus.WINNER;
		}
		else if( log[i].has(" was kicked out ") || log[i].has(" was a deadbeat") ){
			//pl[ log[i].split(/<[^>]*>/)[1] ]._status = eStatus.LOSER;
		}
		else if( log[i].has("Incrementing game to round") || log[i].has("Game has been initialized") ){
			/*
			if( m_playOrder != ePlayOrder.SEQUENTIAL )
				for( tmp in pl )
					if( pl[tmp]._status != eStatus.LOSER ) pl[tmp]._status = eStatus.GREEN;
				*/
		}
	}

	/*---- Add redemption value to dashboard and fix wrapping issue ----*/
	tmp = dashboard.innerHTML;

	//Lets user know how many armies they can expect to receive if they turn in cards.
	if( tmp.indexOf("Escalating") > -1 ){
		m_bonusCards = eBonusCards.ESCALATING;
		RedemptionValue = calcRedemption();
		re = new RegExp("</tbody>");
		tmp = tmp.replace(re,"<tr><td colspan=2><b>Next Redemption Value is " + RedemptionValue +".</b></td></tr></tbody>");
		dashboard.innerHTML = tmp;
	}
	else if( tmp.indexOf("Flat Rate") > -1 ){
		m_bonusCards = eBonusCards.FLATRATE;
		RedemptionValue = calcRedemption();
		re = new RegExp("</tbody>");
		tmp = tmp.replace(re,"<tr><td colspan=2><font color=red><b>Red:</b></font> 4&nbsp;<font color=green><b>Green:</b></font> 6&nbsp;<font color=blue><b>Blue:</b></font> 8&nbsp;<b>Mixed:</b> 10</td></tr></tbody>");
		dashboard.innerHTML = tmp;
	}
	else {
		m_bonusCards = eBonusCards.NOCARDS;
		RedemptionValue = calcRedemption();
	}
	
	/*---- Put # of cards next to each player ----*/
	rightside = document.getElementById('right_hand_side');
	if( m_bonusCards != eBonusCards.NOCARDS ){
		tmp = getElementsByClassName(rightside,"span","player");	
			for( i in tmp )
				if( tmp[i].innerHTML )
					tmp[i].innerHTML = tmp[i].innerHTML + " ( " + pl[tmp[i].innerHTML]._cards + " ) ";
	}
	
	/*---- Map Analysis ----*/

	var armiesArr = map.innerHTML.split(/armies=|,|-|" alt="/);
	if( OPTIONS['colorblind'] ) var cbMapStr = armiesArr[0] + " armies=";

	var tmpArmies = new Array(); //temp holding for armies
	var tmpCountries = new Array(); //temp holding for countries
	
	for( i in pl ){ tmpArmies.push(0); tmpCountries.push(0); }

	//Get individual scores
	for( i = 1; i < armiesArr.length-1;i+=2 ){
			pid = parseInt( armiesArr[i] );
			tmpArmies[pid]+= parseInt( armiesArr[i+1] );
			tmpCountries[pid]++;
			if( OPTIONS['colorblind'] )
				cbMapStr+= armiesArr[i] +"-"+ pl_cbIDs[pid] + armiesArr[i+1] + ","
		}

	totalCountries = (armiesArr.length-2)/2;
	i = 0;
	for ( name in pl ){
		totalArmies += tmpArmies[i];
		pl[name]._armies = tmpArmies[i];
		pl[name]._countries = tmpCountries[i++];
	}

	tmp = document.getElementById('inner-map').innerHTML;

	if( OPTIONS['colorblind'] ) {
		cbMapStr = cbMapStr.substring(0,cbMapStr.length-1) + '">';
		tmp = cbMapStr + "";
	}
	//Auto Scroll to Game
	if( OPTIONS['jumptomap'] ){
		document.getElementById('inner-map').innerHTML = '<a name="gmtop">' + tmp + '</a>';
		window.setTimeout(window.location.hash="gmtop",1000);
	}

	/*---- Adds Statistics Table ----*/
	var statsStr = "";
	tmp = "";
	statsStr+= "\n<table align=center style='width:100%;border:1px solid #FFF;background:#eee;' rules=rows><tr style='font-weight:bold;'><td>Name</td><td>Armies</td><td>Countries</td><td>Strength</td><td>Armies/Turn w/o Bonus</td></tr>\n";
	for( name in pl ){
		if( pl[name]._countries != 0 ){
			var nameStr = OPTIONS['colorblind']?pl_cbIDs[ pl[name]._pid ]+":"+name:name;
			var cardStr = m_bonusCards?" ( " + pl[name]._cards + " )":"";
			var pctArmies = Math.round(pl[name]._armies*100/totalArmies);
			var pctCountries = Math.round(pl[name]._countries*100/totalCountries);
			var numArmiesNextTurn = ( pl[name]._pid )?calcArmiesNextTurn(pl[name]._countries):0;

			// strength = Armies + PotentialArmies - 2*Countries/3
			var pl_Strength = Math.round( ( pl[name]._armies + numArmiesNextTurn + (getTurnInP(pl[name]._cards) * RedemptionValue) - (2*pl[name]._countries/3) ) * 100 )/100;
			if( pl[name]._pid ) // if not neutral
				statsStr+=	"<tr><td><span class='player"+ pl[name]._pid +"'>"+ nameStr + cardStr + "</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl[name]._armies +" ( " + pctArmies +"% )</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl[name]._countries + " ( " + pctCountries +"% )</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl_Strength +"</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ numArmiesNextTurn +"</span></td></tr>\n";
			else //neutral
				tmp =		"<tr><td><span class='player"+ pl[name]._pid +"'>"+ nameStr + "</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl[name]._armies +" ( " + pctArmies +"% )</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl[name]._countries + " ( " + pctCountries +"% )</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>"+ pl_Strength +"</span></td>" +
							"<td><span class='player"+ pl[name]._pid +"'>0</span></td></tr>\n";
		}
	}
	statsStr+= tmp; //neutral
	statsStr+="<tr style='font-weight:bold;color:#000;'><td>Totals</td><td>" + totalArmies + " ( 100% )</td><td>" + totalCountries + " ( 100% )</td><td> - </td><td> - </td></tr>\n";
	statsStr+= "</table>"
	stats.innerHTML = statsStr;
}


/*---- Required ----*/
GM_addStyle('body { margin: 0; padding: 0; } div#middleColumn{ padding-top: 5px; } .player0 { font-weight: bold; }');
/*
if( OPTIONS['colorblind'] )
	GM_addStyle('.player1, .player2, .player3, .player4, .player5, .player6 { color: black !important; }' );
*/

/*---- Focus Stuff ----*/
GM_addStyle(
  '*:focus { -moz-outline: 2px solid ' + OPTIONS['focuscolor'] + ' ! important; -moz-outline-offset: 1px ! important; -moz-outline-radius: 5px ! important; }\n' +
  'button:focus::-moz-focus-inner { border-color: transparent ! important; }\n' +
  'button::-moz-focus-inner,\n' +
  'input[type="reset"]::-moz-focus-inner,\n' +
  'input[type="button"]::-moz-focus-inner,\n' +
  'input[type="submit"]::-moz-focus-inner,\n' +
  'input[type="file"] > input[type="button"]::-moz-focus-inner {\n' +
  'border: 1px dotted transparent ! important;\n' +
  '}\n' +
  'textarea:focus, button:focus, select:focus, input:focus { -moz-outline-offset: -1px ! important; }\n' +
  'input[type="radio"]:focus {-moz-outline-radius: 12px; -moz-outline-offset: 0px ! important; }\n' +
  'a:focus { -moz-outline: 0 !important; -moz-outline-offset: 0 !important; -moz-outline-radius: 0 !important; }\n');

var theGame = new gm_ConquerClubGame(OPTIONS);
