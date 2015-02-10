#!/usr/bin/env python

##############################################################################

"""
Generate reminders of upcoming events, either as email or to console.

Usage::
      reminder [options]

Options:
  - --no-mail
  - --send-mail
  - --to-address <address> (default is to local account)
  - --output-format-mail <text|html|>
  - --output-format-console <text|html|>
  - --skip-weekends
  - --increments <increment-list>
  - --event-file <event-file>
  - --use-history
  - --today <today-date>
  - --last-run <last-run-date>
  - --help
  
Use --help to get a more complete help message.
"""

##############################################################################

import string
import time

# == Module Data Members =====================================================

# a list of weekdays
week_length = 7
weekdays = map(lambda number: time.strftime('%A', (0,1,1,0,0,0,number,1,-1)),
               range(week_length));

# a list of month names
months = map(lambda number: time.strftime('%B', (0,number,1,0,0,0,0,1,-1)),
             range(1,13))
months[:0] = ['']


# == Module Functions ========================================================

def get_index(name, list):
    if len(name) < 3:
        return -1
    name = string.lower(name)
    for num in range(len(list)):
        if ( string.find(string.lower(list[num]), name) == 0 ):
            return num
    return -1

# ----------------------------------------------------------------------------

def weekday_from_name(name):
    """given a potential weekday name, return the week day, 0-6, or -1 if
       it's invalid"""
    return get_index(name, weekdays)

# ----------------------------------------------------------------------------
            
def month_number_from_name(name):
    """given a potential month name, see if it indicates a name"""
    return get_index(name, months)

# ----------------------------------------------------------------------------

def get_weekday(year, month_number, day):
    """Return the numeric weekday for the specified date. 0 = Sunday ... 6 = Saturday"""
    return time.localtime(time.mktime((year, month_number, day,
                                       0, 0, 0, 0, 0, 0)))[6]
            
# == Event Specifier =========================================================

class EventSpecifier:

    def __init__(self):

        """
        Construct a new event specifier, from nothing
        """ 
        self.year = None
        self.month = None
        self.day = None
        self.weekday = None

    # ------------------------------------------------------------------------
        
    def next_concrete(self, now = None):
        """
        Return an event, with the same text as this one, that
        is the next one that
          1. has a fully-specified (year, month, day) date, and
          2. matches this one in terms of the date restriction
        """
             
        if now is None:
            now = Event(time.localtime(time.time()))

        (year, month_number, day) \
               = (now.year, now.month, now.day)
        new_event = Event()
        new_event.text = self.text

        if self.day is not None:
            # Has at least day, so not a "weekday" thing.
            if self.year is not None:
                new_event.year = self.year
                new_event.month = self.month
                new_event.day = self.day

            elif self.month is not None:
                # no year
                if month_number > self.month or \
                   (month_number == self.month and day > self.day ):
                    # passed it. add a year
                    new_event.year = year + 1
                else:
                    new_event.year = year
                    
                new_event.month = self.month
                new_event.day = self.day
                    
            else:
                # no year or month
                new_event.day = self.day
                new_event.year = year
                
                if day > self.day:
                    # next month
                    if month_number == 12:
                        new_event.month = 1
                        new_event.year = year + 1
                    else:
                        new_event.month = month_number + 1
                else:
                    # this month
                    new_event.month = month_number

            new_event.weekday = get_weekday(new_event.year,
                                            new_event.month,
                                            new_event.day)
            return new_event

        # If we're here, there was just a weekday number
        weekday = get_weekday(year, month_number, day)
        event_difference = self.weekday - weekday
        if weekday > self.weekday:
            # already passed it this week
            day = day + week_length + event_difference
        else:
            day = day + event_difference

        tuple = time.localtime(time.mktime((year, month_number, day,
                                               0, 0, 0, 0, 0, 0)))
        new_event = Event(tuple)
        new_event.text = self.text
        return new_event
    # end next_concrete
    
    # ------------------------------------------------------------------------
    def parse(self, text):
        """Read a string and set Event attributes. Return the unused
           portion of the string."""
        split_text = string.split(text)
        word_num = 0
        if len(split_text) == 1 and \
           self._get_weekday(split_text[word_num]):
            word_num = word_num + 1
        else:
            if ( len(split_text) > word_num
                 and self._get_day(split_text[word_num]) ):
                word_num = word_num + 1
                if ( len(split_text) > word_num
                     and self._get_month(split_text[word_num]) ):
                    word_num = word_num + 1
                    if ( len(split_text) > word_num 
                         and self._get_year(split_text[word_num]) ):
                        word_num = word_num + 1
            else:
                raise 'Event.ParseError'
        if  self.validate():
            self.text = string.join(split_text[word_num:])
        return 1
    # end parse

    # ------------------------------------------------------------------------
    def validate(self):
        """Make sure a event object is consistent, like the days number matches
           up with the month (and year) and all that.


           NOT YET IMPLEMENTED"""

        if self.weekday is None and \
           self.year is not None and \
           self.month is not None and \
           self.day is not None:
            self.weekday = get_weekday(self.year, self.month, self.day)

        return 1

    # ------------------------------------------------------------------------
    
    def _get_weekday(self, text):
        """Read a string and capture the weekday number
           (0 = Monday, ..., 6 = Sunday)
           Return true or false, depending on success."""
        weekday = weekday_from_name(text)
        if ( 0 <= weekday <= 6 ):
            self.weekday = weekday
            return 1
        else:
            return 0

    # ------------------------------------------------------------------------
    def _get_day(self, text):
        """Read a string and capture the leading day number. 
           Return (true/false, rest)"""
        try: 
            day = int(text)
            if 0 < day < 32:
                self.day = day
            return 1
        except:
            pass
        return 0
    
    def _get_year(self, text):
        """Read a string and capture the year number. 
           Return (true/false, rest)"""
        try: 
            year = int(text)
            if 0 < year:
                self.year = year
            return 1
        except:
            pass
        return 0
    
    # ------------------------------------------------------------------------
    
    def _get_month(self, text):
        """Read a string and capture the month name, and store
           it as a number 1-12"""
        month_number = month_number_from_name(text)
        if 1 <=  month_number <= 12:
            self.month = month_number
            return 1
        else:
            return 0
        
# == Event Class ==============================================================

class Event:
    "An event class... represents weekday, day, month, year, and text"

    def date(self):
        return self.day + 100 * ( self.month  + 100 * self.year )
    
    def __hash__(self):
        return self.date()
    
    def __init__(self, fodder = None):
        """Construct a new event, from a time tuple or from nothing"""
        self.year = None
        self.month = None
        self.day = None
        self.weekday = None
        self.text = None

        if type(fodder) == type(''):
            self.parse(fodder)
        elif type(fodder) == time.struct_time:
            # a tuple
            self.year = fodder[0]
            self.month = fodder[1]
            self.day = fodder[2]
            self.weekday = fodder[6]
        else:
            pass #raise TypeError, type(fodder)
        
    # ------------------------------------------------------------------------
    def parse(self, fodder):
        (day, month, year) = string.split(fodder)
        self.year = int(year)
        self.day  = int(day)
        month_number = month_number_from_name(month)
        self.month = month_number
        self.weekday = get_weekday(self.year, self.month, self.day)
    # end parse
    
    # ------------------------------------------------------------------------
    def __cmp__(self, other):
        """How do the two Events compare?"""
        return cmp(self.year, other.year) or \
               cmp(self.month, other.month) or \
               cmp(self.day, other.day)
    
    # ------------------------------------------------------------------------
    def clone(self):
        """Return a clone of me"""
        doppel = Event()
        for attrib in self.__dict__.keys():
            setattr(doppel, attrib, getattr(self, attrib))
        return doppel

    # ------------------------------------------------------------------------
    def __repr__(self):
        """ Print me"""
        result = '<Event:'
        for attr in ('weekday', 'day', 'month',
                     'year', 'text'):
            if getattr(self, attr) is not None:
                result = result + ' ' + attr + '='
                result = result + `getattr(self, attr)`
        result = result + '>'
        return result

    # ------------------------------------------------------------------------
    def __str__(self):
        """Pretty-print an event object"""
        result = ""
        if self.weekday is not None:
            result = result + weekdays[self.weekday] + ' '
        if self.day is not None:
            result = result + repr(self.day) + ' '
        if self.month is not None:
            result = result + months[self.month] + ' '
        if self.year is not None:
            result = result + repr(self.year) + ' '
        if self.text is not None:
            result = result + self.text
        return result

    # ------------------------------------------------------------------------
    def __radd__(self, increment_string):
        return self.__add__(increment_string)

    def __add__(self, increment_string):
        """Return a copy of self, but incremented into the future by
           a number of days, weeks and/or months.

           increment_string should look like one or more occurrences
           of <digits><code>, where code is a character (d = day, w =
           week, m = month). """
        my_string = string.strip(increment_string)

        year = self.year
        month = self.month
        day = self.day

        while increment_string:
            i = 0
            while i < len(increment_string):
                if increment_string[i] in 'dwm':
                    # found a letter
                    magnitude = int(increment_string[0:i])
                    type = increment_string[i]
                    increment_string = increment_string[i+1:]
                    break
                i = i + 1
            else:
                break

            # process one thingy
            if magnitude:
                if type == 'd':
                    day = day + magnitude
                elif type == 'w':
                    day = day + week_length * magnitude
                elif type == 'm':
                    month = month + magnitude
                else:
                    raise Exception()
                magnitude = 0
            else:
                # do nothing
                pass

        
        new_time = time.localtime(time.mktime((year, month, day,
                                               0, 0, 0, 0, 0, 0)))
        return Event(new_time)

    # ------------------------------------------------------------------------

    def date_string(self):
        return string.join([weekdays[self.weekday] + ',',
                            str(self.day),
                            months[self.month],
                            str(self.year)], ' ')


##############################################################################

#
# A program for reminding people of things.
#

# == Function Definitions ====================================================

def process_event_specifier(event_header, event_body, event_list):
    """Given an event header (the first line) and body (the rest),
       process it."""
    x = EventSpecifier()
    if x.parse(event_header):
        if event_body:
            x.text = x.text + '\n' + event_body
        event_list.append(x)
    else:
        # BLAIR something better than print?
        print "Error - line",  event_header, "doesn't specifiy a date."
    
    #print "Event =", event_header, event_body, "\n\n"
    # BLAIR - put error message if event doesn't parse

# fed process_event_specifier

# ----------------------------------------------------------------------------

class MailSender:
    def __init__(self):
        self.mime_version = '1.0';
        self.set_content_type('plain')
    # end def __init__

    def set_content_type(self, new_content_type):
        self.content_type = new_content_type
    # end def set_content_type
    

    def send(self, from_address, to_addresses, subject, textBody, htmlBody):
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        from email.MIMEImage import MIMEImage
        import smtplib
        
        if ( type(to_addresses) == type("") ):
            to_addresses = [to_addresses];
           
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['To'] = string.join(to_addresses, ', ')
        #msgRoot['From'] = from_address
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        
        msgText = MIMEText(textBody, 'text', 'iso-8859-1')
        msgAlternative.attach(msgText)

        msgHtml = MIMEText(htmlBody, 'html', 'iso-8859-1')
        msgAlternative.attach(msgHtml)
        
        s = smtplib.SMTP()
        s.connect()
        #print msgRoot.as_string()
        s.sendmail(from_address, to_addresses, msgRoot.as_string())
        s.close()

    #end def send
# end class MailSender
        

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------

def read_events(source, event_list):
    line = source.readline()
    mode = 'nothing'
    while line:
        if not string.strip(line):
            if mode == 'event':
                # reached the end of an event
                process_event_specifier(event_header, event_body, event_list)
                mode = 'nothing'
    
        elif string.lstrip(line) == line:
            # left-justified line has to be an event
            if mode == 'event':
                process_event_specifier(event_header, event_body, event_list)
            else:
                mode = 'event'
    
            # start a new event
            (event_header, event_body) = string.split(line, ':', 1)
    
        else:
            # whitespace at front of line
            if mode == 'event':
                event_body = event_body + line
            else:
                # not in event mode... whitespace line is error
                print "Error: line = \n" + line
    
        line = source.readline()
    # elihw line
    if mode == 'event':
        process_event_specifier(event_header, event_body, event_list)
# fed read_events    

# ----------------------------------------------------------------------------

def consolidate_events(event_list):

    def add_event_if_new(event_list, event):
        for existing_event in event_list:
            if (existing_event.date() == event.date() and 
                existing_event.text == event.text):
                return
        event_list.append(event)
    
    new_event_list = []

    for an_event in event_list:
        add_event_if_new(new_event_list, an_event)

    return new_event_list

# fed consolidate_events

# ----------------------------------------------------------------------------

def find_matches(matches, event_list, target_date, increments=[]):

#    matches = {}
    for inc in [''] + increments:
        for an_event in event_list:
            if an_event == target_date + inc:
                if matches.has_key(an_event.date()):
                    matches[an_event.date()].append(an_event)
                else:
                    matches[an_event.date()] = [an_event]

                #    matches[an_event.date()] = divider(an_event) \
                #                           + '\n\n' + an_event.text
    return matches
# fed find_matches

# ----------------------------------------------------------------------------

def update_history(config_dir, today):
    '''Update the 'history' file.'''
    outfile = open(config_dir + 'history', 'w')
    outfile.write('[DEFAULT]\n\nlast-run: '
                  + str(today.day) + ' '
                  + months[today.month] + ' '
                  + str(today.year))
    outfile.close()
    return
# fed update_history


# ============================================================================


class ToolFactory:

    def makeMailSender(self):
        pass

    def makeEventListFormatter(self):
        pass

# end class ToolFactory

# ============================================================================

class PairedFormatter:
    def __init__(self, oneFormatter, twoFormatter):
        self.oneFormatter = oneFormatter
        self.twoFormatter = twoFormatter

    def format(self, events):
        return (self.oneFormatter.format(events), self.twoFormatter.format(events))

# ============================================================================

class TextToolFactory(ToolFactory):
    def makeMailSender(self):
        ms = MailSender()
        ms.set_content_type('plain')
        return ms

    def makeEventListFormatter(self):
        return PairedFormatter(TextFormatter(), HtmlFormatter())

class HtmlToolFactory(ToolFactory):
    def makeMailSender(self):
        ms = MailSender()
        ms.set_content_type('html')
        return ms

    def makeEventListFormatter(self):
        #return PairedFormatter(TextFormatter(), HtmlFormatter())
        return PairedFormatter(TextFormatter(), HtmlFormatter())

# ============================================================================

class Formatter:
    def __init__(self, events):
        pass

    def header(self, events):
        return ""

    def footer(self, events):
        return ""

    def middle(self, events):
        return ""

    def format(self, events):
        return self.header(events) + self.middle(events) + self.footer(events)

    def middle(self, events):
        return ""

    def get_sorted_list(self, events):
        keys = events.keys()
        keys.sort()
        return keys


# ============================================================================

class TextFormatter(Formatter):

    def __init__(self):
        pass

    def middle(self, events):
        def divider(an_event):
            result = weekdays[an_event.weekday] + ' ' \
                     + str(an_event.day) + ' ' \
                     + months[an_event.month] + ' ' \
                     + str(an_event.year)
            result = result + '\n' + '=' * len(result)
            return result
        
        result = ""
#         for key in self.get_sorted_list(events):
#             event_list = events[key]
#             first_event = event_list[0]
#             result = result + divider(first_event) 
#             for an_event in event_list:
#                 result = result + an_event.text + '\n' 
#             result = result + '\n'

        return result
    

    

# end class TextFormatter

# ----------------------------------------------------------------------------

class HtmlFormatter(Formatter):

    def __init__(self):
        pass

    def header(self, events):
        result = """<html>
<head>
    <title>blah</title>
</head>
</html>
<body>
"""
        return result
    # end def header

    def footer(self, events):
        result = "\n</body>\n</html>\n"
        return result
    # end def footer

    def middle(self, events):

        def divider(an_event):
            date = weekdays[an_event.weekday] + ' ' \
                   + str(an_event.day) + ' ' \
                   + months[an_event.month] + ' ' \
                   + str(an_event.year)
            result = """
   <div style="font-size: larger;color: #005A9C;">
      %s
   </div>
""" % (date)
            return result

        result = ""
        for key in self.get_sorted_list(events):
            event_list = events[key]
            first_event = event_list[0]
            result = result + '''
   <div style="margin-left: 2ex;">\n''' + divider(first_event)
            for an_event in event_list:
                body = """
      <div style="margin-left: 2ex;margin-bottom: 1ex;">
         <b>%s</b>
      </div>
""" % (an_event.text)
            
                result = result + body 
            result = result + '''
   </div>\n'''

        return result
    # end def middle
    

# end class HtmlFormatter

# == Main ====================================================================

def do_main():

    global sys
    import sys 
    global os
    import os

    def process_options():
        def usage():
            """Print a usage message."""
            print """Generate reminders of upcoming events, either as email or to console.

  The reminder program generates a list of reminders of upcoming
  events. The user is able to specify the frequencies of the reminders,
  whether or not to skip weekends, and many other parameters.

  Usage:
        reminder [options]

  where the options are myriad, and described below.

Options:

  General Info:

    Each of the options described below must be specified as
    --<optionname>, possibly followed by the value of the option, if
    applicable. For example, so specify the increments, one would use

        --increments '1d 2w'

    or something similar.

    All options can be specified in the configuration files, unless
    explicitly stated otherwise. See the 'Configuration Files'
    section, and each option's documentation, for more details.


  List of Options:

    no-mail

      Don't send mail. Instead, write any output to the console. This
      is the default when run from the console.

    send-mail

      Send mail instead of writing output to the console. This is the
      default when not run from the console. (For example, from a cron
      job.) 
      
    to-address

      Send mail to the indicated account instead of the local account

    output-format-mail

      How to format the reminders if the output is being sent through
      the mail. Valid values are 'text' and 'html'. The default is
      'text'.

    output-format-mail

      How to format the reminders if the output is being printed on
      the console. Valid values are 'text' and 'html'. The default is
      'text'. 


    skip-weekends

      Skip over weekends. This is useful for those people who
      typically get their reminders on weekdays and want to be
      reminded about the weekend events as well. Default is to treat
      weekend days like any others.

      When the skip-weekend option is on, and reminder is run on a
      weekend, it will also remind about events as if it were also
      being run on each day for the rest of the weekend.

      Note that if the 'use-history' option is on in conjunction with
      skip-weekend, reminder will act as if it were last run on the
      Sunday in these situations. Thus, Running reminder on Friday
      would give Friday, Saturday, and Sunday's
      reminders. Subsequently running it on Tuesday would give Monday
      and Tuesday's reminders.

    increments <increment-list>

      A list of increments to apply to the current day to see whether
      or not it's time to warn about each event. The increment-list is
      a whitespace space-separated list of incremenets, each of the form
      "<number><time-code>[<number><time-code>...]" where the
      <time-code> is one of: 

                 d: day
                 w: week
                 m: month

      and the <number> is an integral value that is applied as a
      multiple to the time unit. Thus: an increment of "1d" means warn
      one day in advance, "2w"  means warn two weeks before the event,
      "3m4d" means warn 3 months and 4 days before the event, and so
      forth.

      An increment-list like "1d 1w 2w 1m1w" means to warn of an event
      first one month and one week before it occurs, then 2 weeks
      before it occurs, one week before, the day before the event, and
      finally on the day of the event. The "day of the event"
      notification is built into the reminder program and may not be
      disabled.

      If the "increments" option is not used, the default
      increment-list of "1d 1w 2w 1m 2m 3m" will be used.


    event-file <filename>

      This is the name of the file that contains the list of events.

      See the "Event File" section for more details about the format
      of the event file.

      The default file is named "events" and resides in the reminder
      configuration directory (~/.reminder). 


    use-history

      Use a history file to record the last time the reminder program
      was run.

      If this option is specified, the history file (see the
      "history file" subsection of the "Configuration File" section,
      below, for details) will be scanned to determine the last time
      that reminder was run. If desired, this "last-run" value may be
      overridden using the "--last-run" command-line option.

      Second, after the successful completion of the reminder program,
      today's date (modified by the "--today" and "--skip-weekend"
      options) will be stored in the history file, so the reminder
      program will not generate any more reminders until the next day.


    today <today-date>

      Make reminder pretend that today is "today-date". The
      (mandatory) parameter must be supplied in <day month year>
      format, like "29 Dec 2000", or something like that. See the
      "Date Format" section for more details.

      If this option is not given, the default is to act as if
      reminder were being run today. See 'last-run' for additional
      details. 
      
    last-run <last-run-date>

      Make reminder pretend that it was last run on "last-run-date". The
      (mandatory) parameter must be supplied in <day, month, year>
      format, like "29 Dec 2000", or something like that. See the
      "Date Format" section for more details.

      Reminder will examine upcoming events starting the day after
      'last-run', and looking at every day up until 'today'.

      If this option is not given, the default is to act as if
      reminder were last run yesterday. Thus if neither of the 'today' 
      and 'last-run' options are given, reminder will remind about
      that are the supplied increments from today only.


Configuration Files

  General Information

    In addition to taking command-line parameters, the reminder
    program gets configuration information from a number of
    configuration files. These files must reside in the ".reminder"
    directory under the user's home directory, i.e. "$HOME/.reminder".

    Each of the files must start with a line of the form "[DEFAULT]",
    followed by zero or more lines that define the operation of the
    reminder program. Most of these lines will be of the form
    "<option>: <value". Blank lines are ignored, and the '#' character
    starts a comment that lasts until the end of the line.

  history

    This file contains the "last-run" information used and generated
    when the "use-history" option has been invoked. There should be no
    need for the use to look at or touch this file. It will be
    automatically created when the "use-history" option is used the
    first time, and updated thereafter. The date in the file can be
    changed by invoking reminder with approprite "use-history" and
    "today" options.

    Just in case you're curious, the file looks like this:

        [DEFAULT]

        last-run:  8 November 2000

    When the 'use-history' option is on, the last-run information
    found in this file overrides any such setting that appears in the
    config file (see below), but does not override any last-run
    setting that is given on the command line.

    Note that in general, it is a bad idea to specify "last-run"
    in the config file.

  config

    This file can contain entries corresponding to all of the
    command-line arguments, except for "help". It is also
    recommended that the "last-run" option not be included in this
    file. See the "history" file section and the documentation for the
    "use-history" option for more details.

    When options are specified in this file, they must all have
    arguments, even those command-line options that don not take
    arguments. The way to specify that an option is to be turned on is
    like this:

         <option>: 1

    Similarly, a value of "0" turns the option off. Options that
    require arguments should have an appropriate argument specified
    after the ":".

    Here is a sample config file that tells reminder to skip weekends,
    and use the history file, and changes the default incrments:

        [DEFAULT]

        skip-weekends: 1
        use-history: 1
        increments: 1w
        
    Note that any options specified on the command line override those
    specified in the config file.

Event File

    The event file is a file of events. The file itself is either
    "$HOME/.reminder/events" (the default) or as specified with the
    "event-file" option, either on the command line or in the config
    file. Each event in the file looks like this:

       <date-spec>: <text>

    Where the date-spec is one of the following: - a weekday - a day
    number - a day number followed by a month name - a day number,
    month name, and year

    The separations between parts of a date spec must only contain
    whitespace. The date spec should not have any leading whitespace.

    The text portion of the event specification runs from the ":" in
    the event spec to the end of the line. Furthermore, if the
    following lines have leading whitespace, they will be added to the
    text. This continues until an empty line is found, or a line with
    no leading whitespace. 

    Here is a sample event file:

    Tuesday: volleyball
    8 November: Dan & Teresa's Anniversary
    11 November: Julie's Birthday
        Julie Sun
    13 November: Mei's Birthday
    15: it's the middle of the month
    30 December 2000: Chapters coupon expires

    (Pretend the "Tuesday", "8", and so forth lie at the left-hand margin.

Date Format

    The "Date Format" section hasn't been completed yet.

"""
        # end def usage


        import getopt
        import ConfigParser
    
        options = {}
        options['config_dir'] = os.environ.get('HOME', '') 
        if options['config_dir']:
            options['config_dir'] = options['config_dir'] + '/.reminder/'

        now = time.localtime(time.time())
        yesterday = list(now)
        yesterday[2] = yesterday[2] - 1
        yesterday = time.localtime(time.mktime(tuple(yesterday)))

        options['increments'] = '1d 1w 2w 1m 2m 3m'
        # If we're running in a terminal, default to printing the reminders.
        # Otherwise, default to mailing.
        options['skip-weekends'] = 0
        options['event-file'] = options['config_dir'] + 'events'
        options['use-history'] = 0
        options['today'] = time.strftime('%e %B %Y', now)

        options['last-run'] = time.strftime('%e %B %Y', yesterday)
        options['output-format-mail'] = 'text'
        options['output-format-console'] = 'text'

        # Now, parse the config file.
        config_parser = ConfigParser.ConfigParser(options)
        try:
            config_parser.read(options['config_dir'] + 'config')
        except ConfigParser.MissingSectionHeaderError, error:
            sys.stderr.write('Warning - config file has no sections.\n')

        # use the options from the config file
        for (name, value) in config_parser.items('DEFAULT'):
            options[name] = value

        # Add the send-mail option now, since the ConfigParser can't
        # deal with bools in the input strings
        options.setdefault('send-mail', False)

        # Read the command-line options (none defined yet) and arguments.
        (command_options, arguments) = getopt.getopt(sys.argv[1:],
                                                     '',
                                                     ['no-mail',
                                                      'send-mail',
                                                      'to-address=',
                                                      'output-format-mail=',
                                                      'output-format-console=',
                                                      'skip-weekends',
                                                      'increments=',
                                                      'event-file=',
                                                      'use-history',
                                                      'today=',
                                                      'last-run=',
                                                      'help'])

        # Only read the last-run history if we're 'use-history'ing
        if options['use-history']:
            try:
                config_parser.read(options['config_dir'] + 'history')
            except ConfigParser.MissingSectionHeaderError, error:
                sys.stderr.write('Warning - history file has no sections.\n')

   
        for (option, value) in command_options:
            option = option[2:]
            if option in ('send-mail', 'use-history', 'skip-weekends'):
                options[option] = True
            elif option == 'no-mail':
                options['send-mail'] = False
            elif option in ('increments', 'to-address', 'today', 'event-file',
                            'output-format-mail', 'output-format-console'):
                options[option] = value
            elif option == 'last-run':
                if string.lower(value) == 'yesterday':
                    options[option] = yesterday
                else:
                    options[option] = value
                
            elif option == 'help':
                usage()
                sys.exit(0)

        options['increments'] = string.split(options['increments'])

        if arguments or not options['event-file']:
            print __doc__ #usage()
            sys.exit(1)
            
        return (arguments, options)

    # Main main
    (arguments, options) = process_options()
 
    event_list = []
    infile = open(options['event-file'], 'r')
    read_events(infile, event_list)
   
    def concretize_list(event_list, match_day):
        results = []
        for e in event_list:
            results.append(e.next_concrete(match_day))
        return results

    match_day = Event(options['last-run'])
    match_day = match_day + '1d'
    first_day = match_day
    
    # Now, make an event for today
    today = Event(options['today'])
    if options['skip-weekends'] and 4 <= today.weekday:
        while today.weekday < 6:
            today += '1d'
         
    matches = {}

                               #consolidate_events(concretize_list(event_list,
                               #                                   match_day)),

    
    while ( match_day <= today ):
        this_list = event_list[:]
        matches = find_matches(matches,
                               concretize_list(this_list, match_day),
                               match_day,
                               options['increments'])
        match_day = match_day + '1d'

    # consolidate the matches
    for key in matches.keys():
        matches[key] = consolidate_events(matches[key])
    
    #message = ''
    #keys = matches.keys()
    #keys.sort()
    #message = string.join(map(matches.get, keys), '\n\n\n')
    #    message = format_matches_html(matches)

    if options['send-mail']:
        output_format = options['output-format-mail']
    else:
        output_format = options['output-format-console']
        
    if 'text' == output_format:
        toolBox = TextToolFactory()
    elif 'html' == output_format:
        toolBox = HtmlToolFactory()
    else:
        # have to have some default
        sys.stderr.write("Unknown output-format '" + output_format +
                         "'. Using 'text'.")
        toolBox = TextToolFactory()

    if len(matches):
        formatter = toolBox.makeEventListFormatter()
        (textMessage, htmlMessage) = formatter.format(matches)
    else:
        textMessage = ''
        htmlMessage = ''

    if first_day == today:
        date_range = first_day.date_string()
    elif first_day > today:
        date_range = 'Empty range: ' + first_day.date_string() + ' -- ' \
                     + today.date_string()
    else:
        date_range = first_day.date_string() + ' -- ' + today.date_string()

    if textMessage or htmlMessage:
        if options['send-mail']:
            def username():
                return os.environ.get('USER', os.environ['LOGNAME'])
            from_address = username() + '@localhost'
            to_address = options.get('to-address', from_address)
            subject = 'Reminders for ' + date_range
            
            sender = toolBox.makeMailSender()
            sender.send(from_address, to_address, subject, textMessage, htmlMessage)

        else:
            print textMessage
    else:
        if not options['send-mail']:
            print "no reminders for", date_range

    if options['use-history']:
        update_history(options['config_dir'], today)

# end do_main

# Do the main thing, unless we're imported as a module
if __name__ == "__main__": do_main()    

# ============================================================================
