// ==UserScript==
// @name           PBeM Backgammon Fixer
// @namespace      http://mywebsite.com/myscripts
// @description    A template for creating new user scripts from
// @include        http://www.gamerz.net/pbmserv/Backgammon/*
// ==/UserScript==

// <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
//    "http://www.w3.org/TR/html4/loose.dtd">
// <HTML>
// <HEAD>
// 
// <!--[if gte IE 5.5000]>
// <script type="text/javascript" src="../pngfix_map.js"></script>
// <![endif]-->
// 
// <SCRIPT LANGUAGE="JavaScript" type="text/javascript">
// <!--
// 
// function BoardClick(pos,type){
//   if(type == 1){
//     document.GetMoveForm.nm.value += ':'+pos;
//   } else {
//     if(document.GetMoveForm.nm.value.length > 0){
//       if(document.GetMoveForm.nm.value.search(/([-:]\d+|-H|-B)$/) > -1){
//         document.GetMoveForm.nm.value += ','+pos;
//       } else {
//         document.GetMoveForm.nm.value += '-'+pos;
//       }
//     } else {
//       document.GetMoveForm.nm.value = pos;
//     }
//   }
// }
// // -->
// </SCRIPT>
// 
// <link rel="StyleSheet" href="../main4.css" type="text/css">
// <script src="../main8.js"></script>
// <title>Backgammon game 31641</title>
// <link rel="shortcut icon" href="/favicon.ico" >
// </head>
// <body bgcolor="#FFFFFF">
// 
// <table class="badlayout" cellpadding=0><tr><td valign="top" align="center">
// <div class="rounded">
//  <ul class="menu">
//   <li>make&nbsp;display
//   <ul>
//     <li> <a href="Backgammon.php?w=0.1&ds=0">small</a>
//    </ul>
//     <li> <a href="Backgammon.php?w=0.1&fl=1">rotate&nbsp;board</a>
// 
//   <li> <a href="../List.php?Backgammon">backgammon&nbsp;games</a>
//   <li> <a href="../gamerz.php">all&nbsp;games</a>
//   <li> <a href="../Ratings.php?Backgammon">backgammon&nbsp;ratings</a>
//   <li> <a href="../Challenge.php?Backgammon">backgammon&nbsp;challenge</a>
// 
//   <li> <a href="http://www.gamerz.net/pbmserv/backgammon.html" target="_blank">backgammon help</a>
//   <li> <a href="mailto:wamelen@math.lsu.edu">report&nbsp;bugs</a>
//   <li> <a href="../login.html">log in</a>
//  </ul>
// </div>
// </td>
// 
// <td class="boardtd" valign="top" align="center">
// <MAP NAME="boardmap">
// <AREA HREF="JavaScript:BoardClick(12,0)" shape=rectangle coords="20,20,59,220">
// <AREA HREF="JavaScript:BoardClick(13,0)" shape=rectangle coords="20,340,59,540">
// <AREA HREF="JavaScript:BoardClick(11,0)" shape=rectangle coords="60,20,99,220">
// <AREA HREF="JavaScript:BoardClick(14,0)" shape=rectangle coords="60,340,99,540">
// <AREA HREF="JavaScript:BoardClick(10,0)" shape=rectangle coords="100,20,139,220">
// <AREA HREF="JavaScript:BoardClick(15,0)" shape=rectangle coords="100,340,139,540">
// <AREA HREF="JavaScript:BoardClick(9,0)" shape=rectangle coords="140,20,179,220">
// <AREA HREF="JavaScript:BoardClick(16,0)" shape=rectangle coords="140,340,179,540">
// <AREA HREF="JavaScript:BoardClick(8,0)" shape=rectangle coords="180,20,219,220">
// <AREA HREF="JavaScript:BoardClick(17,0)" shape=rectangle coords="180,340,219,540">
// <AREA HREF="JavaScript:BoardClick(7,0)" shape=rectangle coords="220,20,259,220">
// <AREA HREF="JavaScript:BoardClick(18,0)" shape=rectangle coords="220,340,259,540">
// <AREA HREF="JavaScript:BoardClick(6,0)" shape=rectangle coords="302,20,341,220">
// <AREA HREF="JavaScript:BoardClick(19,0)" shape=rectangle coords="302,340,341,540">
// <AREA HREF="JavaScript:BoardClick(5,0)" shape=rectangle coords="342,20,381,220">
// 
// <AREA HREF="JavaScript:BoardClick(20,0)" shape=rectangle coords="342,340,381,540">
// <AREA HREF="JavaScript:BoardClick(4,0)" shape=rectangle coords="382,20,421,220">
// <AREA HREF="JavaScript:BoardClick(21,0)" shape=rectangle coords="382,340,421,540">
// <AREA HREF="JavaScript:BoardClick(3,0)" shape=rectangle coords="422,20,461,220">
// <AREA HREF="JavaScript:BoardClick(22,0)" shape=rectangle coords="422,340,461,540">
// <AREA HREF="JavaScript:BoardClick(2,0)" shape=rectangle coords="462,20,501,220">
// <AREA HREF="JavaScript:BoardClick(23,0)" shape=rectangle coords="462,340,501,540">
// <AREA HREF="JavaScript:BoardClick(1,0)" shape=rectangle coords="502,20,541,220">
// <AREA HREF="JavaScript:BoardClick(24,0)" shape=rectangle coords="502,340,541,540">
// <AREA HREF="JavaScript:BoardClick('B',0)" shape=rectangle coords="260,20,301,540">
// <AREA HREF="JavaScript:BoardClick('H',0)" shape=rectangle coords="542,20,583,540">
// <AREA HREF="JavaScript:BoardClick(2,1)" shape=rectangle coords="88,260,128,300">
// <AREA HREF="JavaScript:BoardClick(1,1)" shape=rectangle coords="152,260,192,300">
// </map>
// <table><tr><td width=604>
// <div style="display:block;position:relative;top=0px;left:0px;
// width:604px;height:560px">
// <img name=brd src="BackBack11.jpg" border=0 height=560 width=604
//   style="position:absolute;top=0px;left:0px">
// 
// <img src="dice21.png" border=0 STYLE="position:absolute;top:260px;left:88px">
// <img src="dice11.png" border=0 STYLE="position:absolute;top:260px;left:152px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:100px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:56px;left:100px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:180px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:56px;left:180px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:92px;left:180px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:20px;left:220px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:56px;left:220px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:302px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:56px;left:302px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:92px;left:302px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:342px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:56px;left:342px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:382px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:20px;left:502px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:56px;left:502px">
// 
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:500px;left:302px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:464px;left:302px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:428px;left:302px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:392px;left:302px">
// <img src="bpiece61.png" border=0 STYLE="position:absolute;top:356px;left:302px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:500px;left:382px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:464px;left:382px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:500px;left:462px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:500px;left:20px">
// <img src="wpiece1.png" border=0 STYLE="position:absolute;top:464px;left:20px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:500px;left:60px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:464px;left:60px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:500px;left:220px">
// <img src="bpiece1.png" border=0 STYLE="position:absolute;top:464px;left:220px">
// <img NAME="brd" src="BackBackT1.gif" border=0
//   USEMAP="#boardmap"
//   STYLE="position:absolute;top=0px;left:0px">
// </div>
// </td></tr></table>
// 
// <h3>White (maz) pip count: 104/15</h3><h3>Black (blair) pip count: 118/15</h3></td>
// <td valign="top" align="center">
// <div class="rounded">
// <h2 class="gameheading">Backgammon game 31641</h2>
// <h3 class="names">maz plays White, blair plays Black</h3>
// </div>
// <div class="rounded">
// <h4 class="tomove">
// The last move was Roll: 4,1  Move: 13-9,9-8, Black (blair) to move</h4>
// <form name=GetMoveForm method=GET action=Backgammon.php>
// <input name=w type=hidden value=0.1>
// Click or enter move <input name=nm type=text size=10 maxlength=60>
// 
// <input name=m type=hidden value=18>
// <input type=submit value="View move">
// </form>
// <form name=SpecialMove method=GET action=Backgammon.php>
// <input name=w type=hidden value=0.1>
// <select name="sm">;<option value="">--special move--
// <option value="manualformvrmaz">maz toggle manual
// <option value="greedyformvrmaz">maz toggle greedy
// <option value="undoformvrmaz">maz request undo
// <option value="manualformvrblair">blair toggle manual
// <option value="greedyformvrblair">blair toggle greedy
// <option value="undoformvrblair">blair request undo
// <option value="proposeformvrblair">blair propose a draw
// <option value="resignformvrblair">blair resign
// </select>
// <input type=submit value="Submit">
// 
// </form>
// </div>
// <div class="rounded">
// <div class="movenav">
// <a href="Backgammon.php?w=0.1&m=0">&lt;&lt;</A> <a href="Backgammon.php?w=0.1&m=16">&lt;</A>
// </div>
//   <table class="moves">
//     <tr><th colspan=2>White</th><th colspan=2>Black</th>
//   <script>
//   PrintMoves(["Roll: 3,1  Move: 8-5,6-5","Roll: 2,1  Move: 12-14,1-2","Roll: 3,1  Move: 13-10,24-23","Roll: 5,2  Move: 2-7,12-14","Roll: 5,2  Move: 10-5,23-21","Roll: 6,1  Move: 12-18,17-18","Roll: 5,4  Move: 6-1,5-1","Roll: 4,3  Move: B-4,4-7","Roll: 6,4  Move: 24-20,21-15","Roll: 4,3  Move: 12-15,15-19","Roll: 3,2  Move: B-22,22-20","Roll: 6,1  Move: 12-18,18-19","Roll: 5,4  Move: 13-8,8-4","Roll: 6,1  Move: 17-23,17-18","Roll: 5,5  Move: 20-15,20-15,15-10,15-10","Roll: 3,2  Move: 18-21,19-21","Roll: 4,1  Move: 13-9,9-8"],
//     [],'Backgammon.php?w=0.1',-1);
//   </script>
//   </table>
// 
//   </div>
// 





function removeMenu()
{
   var menuTd = document.evaluate(
      "//td",
      document,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null).singleNodeValue;

   if ( menuTd )
   {
      menuTd.parentNode.removeChild(menuTd);
   }
}

removeMenu();
