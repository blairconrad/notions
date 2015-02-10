// ==UserScript==
// @name          Stack Overflow Add Post References
// @namespace   http://userscripts.org/people/4764
// @description   Add easy-to-use reference links for questions and answers
// @include       http://stackoverflow.com/questions/*
// @require	http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js
// ==/UserScript==

(function () {
    function select(elem)
    {
        var range = document.createRange();
        range.setStartBefore(elem);
        range.setEndAfter(elem);

        var selection = window.getSelection();
        selection.addRange(range);
    }

    function clearSelection()
    {
        var selection = window.getSelection();
        selection.removeAllRanges();
    }

    function add_reference($menu, link_id, content_id, content_text)
    {
        $link = $('<span id="' + link_id + '"> reference</span>');
        $content = $('<span id="' + content_id + '">' + content_text + '</span>');


        $content.hide();
        $content.hover(
            function(){
                select($(this).get(0));
            },
            function(){
                clearSelection();
            }
        );

        $link.click(function() { 
            $reference = $('span#' + content_id);
            $reference.toggle();
        });

        $separator = $('<span class="link-separator">|</span>');
                
        $menu.append($separator).append($link).append(' ').append($content);
    }

    function add_reference_to_question()
    {
        var $question_link = $('div#question-header a')
        var $question_title = $question_link.text();
        var $question_url = 'http://stackoverflow.com' + $question_link.attr('href');
        var $question_menu = $('div#question div.post-menu');
        
        add_reference($question_menu, 
                  'question-reference-link',
                  'question-reference-content', 
                  '[' + $question_title + '](' + $question_url + ')');

    }

    function add_reference_to_answers()
    {
        var $answers = $('div.answer');

        $answers.each(add_reference_to_answer);
        GM_log("there are " + $answers.length + " answers");
    }

    function add_reference_to_answer(index, elem)
    {
        var $answer_menu = $('div.post-menu', elem);

        var answer_number = elem.id.split('-')[1];
        var user = $('div.user-details a', elem).text();

        add_reference($answer_menu, 
                  'answer-reference-link-' + answer_number,
                  'answer-reference-content-' + answer_number,
                  '@[' + user + '](#' + answer_number + ')');
    }

    // -----------------------------------------------------------------------

    add_reference_to_question();
    add_reference_to_answers();

}());

