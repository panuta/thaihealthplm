# -*- encoding: utf-8 -*-
from django.conf import settings

import calendar
from datetime import date

from constants import *

def format_full_datetime(datetime):
    return unicode('%d %s %d เวลา %02d:%02d น.', 'utf-8') % (datetime.day, unicode(THAI_MONTH_NAME[datetime.month], 'utf-8'), datetime.year + 543, datetime.hour, datetime.minute)

def format_abbr_datetime(datetime):
    return unicode('%d %s %d เวลา %02d:%02d น.', 'utf-8') % (datetime.day, unicode(THAI_MONTH_ABBR_NAME[datetime.month], 'utf-8'), datetime.year + 543, datetime.hour, datetime.minute)

def format_full_date(datetime):
    return unicode('%d %s %d', 'utf-8') % (datetime.day, unicode(THAI_MONTH_NAME[datetime.month], 'utf-8'), datetime.year + 543)

def format_abbr_date(datetime):
    return unicode('%d %s %d', 'utf-8') % (datetime.day, unicode(THAI_MONTH_ABBR_NAME[datetime.month], 'utf-8'), datetime.year + 543)

def format_full_month_year(datetime):
    return "%s %d" % (unicode(THAI_MONTH_NAME[datetime.month], "utf-8"), datetime.year + 543)

def format_abbr_month_year(datetime):
    return "%s %d" % (unicode(THAI_MONTH_ABBR_NAME[datetime.month], "utf-8"), datetime.year + 543)



