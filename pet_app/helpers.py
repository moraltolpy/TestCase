import datetime
from copy import deepcopy

import arrow

from pet_app.models import Visit


def available_range(visit_date, vet):
    booked_time = Visit.objects.\
        filter(vet=vet, visit_date__date=arrow.get(visit_date.year, visit_date.month, visit_date.day).datetime).\
        values_list('visit_date__time', flat=True)
    available_time, available_ranges = [], []

    for hour in range(8, 18):
        for minute in range(0, 60, 10):
            if not datetime.time(hour, minute) in booked_time:
                available_time.append(datetime.time(hour, minute))

    current_range = {'start': available_time[0]}
    for i, visit_time in enumerate(available_time):
        if visit_time == current_range['start']:
            continue
        elif i == len(available_time) - 1:
            current_range['end'] = visit_time
            available_ranges.append(deepcopy(current_range))
        elif _is_last_available(visit_time, available_time[i + 1]):
            current_range['end'] = visit_time
            available_ranges.append(deepcopy(current_range))
            current_range = {'start': available_time[i + 1]}

    result_string = 'Available spots are: '
    for r in available_ranges:
        result_string += "%s.%02.f - %s.%02.f, " % (r["start"].hour, r["start"].minute, r["end"].hour, r["end"].minute)
    return result_string[:-2] + '.', available_ranges


def _is_last_available(first, second):
    shifted = arrow.now().replace(hour=first.hour, minute=first.minute).shift(minutes=+10)
    if datetime.time(shifted.hour, shifted.minute) < second:
        return True
    return False
