#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import shutil
import os
import subprocess
import urllib2

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    question_number = int(args[0])


    base_url = 'http://projecteuler.net/index.php?section=problems&id='
    url = base_url + str(question_number)

    div_count = 1
    question = []
    for line in urllib2.urlopen(url):

        if question and line.startswith('<div'):
            div_count += 1
            continue

        if question and line.startswith('</div>'):
            div_count -= 1
            if div_count == 0:
                break
            continue

        if question or line.startswith('<div class="problem_content"'):
            question.append('# ' + line.strip())

    question_text = '\n'.join(question[1:])
    question_text = question_text.replace('&quot;', '"')
    question_text = question_text.replace('<li>', '* ')
    question_text = question_text.replace('</li>', '')
    question_text = question_text.replace('<ol>', '')
    question_text = question_text.replace('</ol>', '')
    question_text = question_text.replace('<sup>', '**')
    question_text = question_text.replace('**2', '²')
    question_text = question_text.replace('**3', '³')
    question_text = question_text.replace('<sub>', '_')
    question_text = question_text.replace('<br />', '\n')

    question_text = question_text.replace("<img src='images/symbol_times.gif' width='9' height='9' alt='&times;' border='0' style='vertical-align:middle;' />", '×')
    question_text = question_text.replace("<img src='images/symbol_lt.gif' width='10' height='10' alt='&lt;' border='0' style='vertical-align:middle;' />", '<')
    question_text = question_text.replace("<img src='images/symbol_le.gif' width='10' height='12' alt='&le;' border='0' style='vertical-align:middle;' />", '≤')
    question_text = question_text.replace("<img src='images/symbol_ne.gif' width='11' height='10' alt='&ne;' border='0' style='vertical-align:middle;' />", '≠')
    question_text = question_text.replace("<img src='images/symbol_gt.gif' width='10' height='10' alt='&gt;' border='0' style='vertical-align:middle;' />", '>')
    question_text = question_text.replace("<img src='images/symbol_sum.gif' width='11' height='14' alt='&sum;' border='0' style='vertical-align:middle;' />", '∑')
    
    for tag in ['i', 'p', 'sup', 'sub', 'var']:
        question_text = question_text.replace('<' + tag + '>', '')
        question_text = question_text.replace('</' + tag + '>', '')
    
    question_label = 'q%(question_number)05d' % vars()

    template = file('template.py').read()
    new_file = template % vars()
    
    os.mkdir(question_label)
    file(os.path.join(question_label, question_label + '.py'), 'wb').write(new_file)

    subprocess.call(['svn.exe', 'add', question_label])
    subprocess.call(['svn.exe', 'propset', 'svn:ignore', '*.pyc', question_label])
    return 0


if __name__ == '__main__':
    sys.exit(main())

