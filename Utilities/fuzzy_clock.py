#!/usr/bin/env python

import sys
import time

class FiveMinuteRounder:
    minute_strings = ['', 'five after ', 'ten after ', 'quarter after ', 'twenty after ', 'twenty-five after ',
                      'half past ', 'twenty-five to ', 'twenty to ', 'quarter to ', 'ten to ', 'five to ', '']
    hour_strings = ['twelve', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven']

    def round_minute(self, minute):
        return 5 *((minute + 3) / 5)

    def name_minute(self, minute):
        return self.minute_strings[minute/5]

    def round_time(self, hour, minute):

        minute = self.round_minute(minute)

        if minute > 30:
            hour += 1

        if hour >= 12:
            hour -= 12

        return self.name_minute(minute) + self.hour_strings[hour]

def main(args=None):
    if args == None:
        args = sys.argv

    (hour, minute) = time.localtime()[3:5]
    rounder = FiveMinuteRounder()
    print rounder.round_time(hour, minute)

#     for hour in range(12):
#         for minute in range(60):
#             print hour+1, minute, ':', round_time(hour+1, minute)
#     return 0


if __name__ == '__main__':
    sys.exit(main())

