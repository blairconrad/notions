// ==UserScript==
// @name           Stack Overflow Restrict Tags
// @description	restricts questions shown to those listed in your favourite tags. See favourite_tags variable in script body.
// @namespace      http://userscripts.org/people/4764
// @include        http://stackoverflow.com/*
// @require	http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js
// ==/UserScript==

(function () {
   // For now, edit this to include your favourite tags. Case matters.
   var favourite_tags = ['java', 'c#', 'python'];

    function makeMenuToggle(key, defaultValue, toggleOn, toggleOff, prefix)
    {
        // Load current value into variable
        window[key] = GM_getValue(key, defaultValue);
        // Add menu toggle
        GM_registerMenuCommand((prefix ? prefix+": " : "") + (window[key] ? toggleOff : toggleOn), function() {
            GM_setValue(key, !window[key]);
            location.reload();
        });
    }

    function hideUnfavouriteQuestions()
    {

        if ( shouldHideUnfavouriteQuestions )
        {
            var question_tags = $('div>div.question-summary');
            question_tags.filter(function () 
                                 { 
                                     var match = false;
                                     $('a.post-tag', this).each(function () { (match |= favourite_tags.indexOf(this.text) >= 0 ); } );
                                     return !match;
                                 }
                                ).hide(1000);
        }
    }

    function hideAnswersWhenSearching()
    {
        if ( shouldHideAnswersWhenSearching )
        {
            GM_log("hidiing answers");
            $('div.question-summary:has(a.answer-title)').hide(1000);
        }
    }

    function addMenuCommands()
    {
        makeMenuToggle("shouldHideUnfavouriteQuestions", false, "Show only questions from favourite categories", "Show all questions", "SO");
        makeMenuToggle("shouldHideAnswersWhenSearching", false, "Show only questions in search results", "Show questions and answers when searching", "SO");
    }
    // -----------------------------------------------------------------------


    addMenuCommands();
    hideUnfavouriteQuestions();
    hideAnswersWhenSearching();

}());

