"""
GOAL: Create a CSV file with time dimension.
Columns: DateKey, FullDateKey, DayNumberInWeek, DayName, DayNumber, MonthNumber, YearNumber, WeekNumber, DayWeekType
I.e. for year 2015.
"""

import datetime

from TextWriter import TextWriter

# Define start and end dates.
start_date = datetime.date(2015,1,1)
end_date = datetime.date(2016,1,1)

# Prepare variables
total_data = []
current_date = start_date
pk = 1

# Create a date list - process every date from this interval.
while current_date < end_date:
    # Get all desired information about the date.
    year_n, week_n, week_day_n = current_date.isocalendar()
    day_data = [
        pk,
        current_date.strftime('%d.%m.%Y'),
        week_day_n,
        current_date.strftime('%A'),
        current_date.day,
        current_date.month,
        current_date.year,
        week_n,
    ]
    # Is it a weekend or workday?
    if week_day_n in [6, 7]:
        day_week_type = 'weekend'
    else:
        day_week_type = 'workday'
    # Save data
    day_data.append(day_week_type)
    total_data.append(day_data)
    # Increment current date by one day.
    current_date += datetime.timedelta(days=1)
    pk += 1

# Prepare header
header = [
    'DateKey', 'FullDateKey', 'DayNumberInWeek', 'DayName',
    'DayNumber', 'MonthNumber', 'YearNumber', 'WeekNumber', 'DayWeekType'
]
total_data.insert(0, header)

# Create a CSV file from the list.
tw = TextWriter()
tw.write_date_file('date_dim', total_data)
