import jdatetime
from datetime import datetime, timedelta

def j_start(date_type='day', date_value=datetime.now() ):
    quarter_list = [1, 4, 7, 10]
    if type(date_value) == str:
        date_value_d = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
    else:
        date_value_d = date_value
    jdate_value = jdatetime.datetime.fromgregorian(datetime=date_value_d)
    jdate_value_d = jdate_value
    j_year = jdate_value.year
    j_month = jdate_value.month
    j_day = jdate_value.day
    j_hour = jdate_value.hour
    j_minute = jdate_value.minute
    j_second = jdate_value.second
    if date_type == 'year':
        jdate_value_d = jdatetime.datetime(j_year, 1, 1, 0, 0)
    elif date_type == 'quarter':
        jdate_value_d = jdatetime.datetime(j_year, quarter_list[(j_month - 1) // 3], 1, 0, 0, 0)
    elif date_type == 'month':
        jdate_value_d = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
    elif date_type == 'week':
        if jdate_value.weeknumber() != 1:
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0) - timedelta(days=jdate_value.weekday())
        else:
            jdate_value_d = jdatetime.datetime(j_year, 1, 1, 0, 0)

    elif date_type == 'day':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0)
    elif date_type == 'hour':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, 0, 0)
    elif date_type == 'minute':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, 0)
    elif date_type == 'second':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second)
    elif date_type == '_':
        jdate_value_d = jdate_value

    return jdate_value_d.togregorian()


def j_end(date_type='day', date_value=datetime.now() ):
    '''
    It gets a datetime group type and datetime, then calculate the last datetime of that period.

    example:
        group_by -> 'year'
        value    -> '2024-03-20 00:00:00' (1403/01/01 00:00:00)
        return   -> '2025-03-21 00:00:00' (1404/01/01 00:00:00)

    :param self:
    :param group_by:
    :param value:
    :return:
    '''
    quarter_list = [1, 4, 7, 10]
    jdate_value = jdatetime.datetime.fromgregorian(date=date_value)
    jdate_value_d = jdate_value
    j_year = jdate_value.year
    j_month = jdate_value.month
    j_day = jdate_value.day
    j_hour = jdate_value.hour
    j_minute = jdate_value.minute
    j_second = jdate_value.second
    match date_type:
        case 'year':
            jdate_value_d = jdatetime.datetime(j_year + 1, 1, 1, 0, 0)
        case 'quarter':
            j_month = quarter_list[(j_month - 1) // 3]
            if j_month < 9:
                j_month += 3
            else:
                j_month = 1
                j_year += 1
            jdate_value_d = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
        case 'month':
            first_day = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            jdate_value_d = next_month.replace(day=1)
        case 'week':
            if jdate_value_d.weeknumber() < 52:
                # TODO: The last week of a year can be share between two years. last day of the week is the last day of
                #   that year.
                #   if last day of this week has the same year record, its ok
                #   if not, find the last day of the year, then set the last day of the year as end of the week
                jdate_value_d = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
            else:
                # TODO:
                #   find the last day of current week by finding the next week first day minus one.
                next_week_start = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
                if next_week_start.year == j_year:
                    jdate_value_d = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
                else:
                    jdate_value_d = jdatetime.datetime(j_year + 1, 1, 1, 0, 0)

        case 'day':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0) + timedelta(days=1)
        case 'hour':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, 0, 0) + timedelta(hours=1)
        case 'minute':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, 0) + timedelta(
                minutes=1)
        case 'second':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second) + timedelta(
                seconds=1)
        case '_':
            jdate_value_d = jdate_value

    return jdate_value_d.togregorian()
