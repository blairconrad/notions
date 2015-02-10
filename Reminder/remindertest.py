#!/usr/env/bin python

import unittest
import reminder

class WeekdayFromName(unittest.TestCase):
    def testNonMatchingEntries(self):
        for name in [ '', 'Blah', 'Mondays' ]:
            self.assertEqual(-1, reminder.weekday_from_name(name))

    def test3LetterMatches(self):
        mixed = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
        lower = [ 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' ]
        for index  in range(len(mixed)):
            self.assertEqual(index, reminder.weekday_from_name(mixed[index]))
            self.assertEqual(index, reminder.weekday_from_name(lower[index]))


    def testWholeWordMatches(self):
        mixed = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
        lower = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]
        for index  in range(len(mixed)):
            self.assertEqual(index, reminder.weekday_from_name(mixed[index]))
            self.assertEqual(index, reminder.weekday_from_name(lower[index]))

class MonthFromName(unittest.TestCase):
    def testNonMatchingEntries(self):
        for name in [ '', 'Octember', 'Junes' ]:
            self.assertEqual(-1, reminder.month_number_from_name(name))

    def test3LetterMatches(self):
        mixed = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                  'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
        lower = [ 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
                  'aug', 'sep', 'oct', 'nov', 'dec' ]
        for index  in range(len(mixed)):
            self.assertEqual(index + 1, reminder.month_number_from_name(mixed[index]))
            self.assertEqual(index + 1, reminder.month_number_from_name(lower[index]))


    def testWholeWordMatches(self):
        mixed = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December' ]
        lower = [ 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december' ]
        for index  in range(len(mixed)):
            self.assertEqual(index + 1, reminder.month_number_from_name(mixed[index]))
            self.assertEqual(index + 1, reminder.month_number_from_name(lower[index]))


