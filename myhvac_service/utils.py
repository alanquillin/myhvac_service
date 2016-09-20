from myhvac_service import const

from datetime import datetime, timedelta


def get_active_schedule(program, now=None):
    if not program or not program.schedules:
        return None

    if not now:
        now = datetime.now()

    ordered_schedules = extract_ordered_schedules(program, now)

    if not ordered_schedules:
        return None

    active_schedule = ordered_schedules[-1]['schedule']

    for s in ordered_schedules:
        if now < s.get('datetime'):
            break

        active_schedule = s.get('schedule')

    return active_schedule


def extract_ordered_schedules(program, now=None):
    schedules_by_day = group_schedules_by_day(program)
    schedules_data = []

    if not now:
        now = datetime.now()

    for day, schedules in schedules_by_day.iteritems():
        d = get_reletive_date_for_day(day, now)

        for schedule in schedules:
            dt = datetime.combine(d, schedule.time_of_day)
            schedules_data.append({'datetime': dt, 'schedule': schedule})

    return sorted(schedules_data, key=lambda k: k['datetime'])


def get_reletive_date_for_day(day, now=None):
    if not now:
        now = datetime.now()

    for day_mod in range(-3, 4):
        dt = now + timedelta(days=day_mod)
        if day.lower() == dt.strftime("%A").lower():
            return dt.date()


def group_schedules_by_day(program):
    schedules_by_day = {}
    for schedule in program.schedules:
        dow = days_of_week_from_bin_aggr(schedule.days_of_week_bin_aggr)
        if not dow:
            continue
        for day in dow:
            d = schedules_by_day.get(day, [])
            d.append(schedule)
            schedules_by_day[day] = d

    return schedules_by_day


def days_of_week_from_bin_aggr(dow_bin_aggr):
    dow_bin = reverse('{0:b}'.format(dow_bin_aggr))
    dow = []
    for idx, day in const.BIN_AGGR_DAYS_OF_WEEK_IDX.iteritems():
        found = False
        if len(dow_bin) >= idx:
            found = True if dow_bin[idx-1] == '1' else False

        if found:
            dow.append(day)

    return dow


def reverse(_str):
    return _str[::-1]


class _Schedule(object):
    def __init__(self, id, days_of_week_bin_aggr=None, time_of_day=None, cool_temp=None, heat_temp=None):
        self.days_of_week_bin_aggr = days_of_week_bin_aggr
        self.time_of_day = time_of_day
        self.cool_temp = cool_temp
        self.heat_temp = heat_temp
        self.id = id
        self.name = "schedule_%s" % id

    def __repr__(self):
        return '%s <id=%s, name=%s, time_of_day=%s, days_of_week_bin_aggr=%s, dow=%s, cool_temp=%s, heat_temp=%s' % \
               (self.__class__.__name__, self.id, self.name,
                self.time_of_day.strftime('%I:%M %p'), self.days_of_week_bin_aggr,
                days_of_week_from_bin_aggr(self.days_of_week_bin_aggr),
                self.cool_temp, self.heat_temp)


class _Program(object):
    def __init__(self, schedules=[]):
        self.schedules = schedules

    def __repr__(self):
        return '%s <schedules=%s>' % (self.__class__.__name__, self.schedules)


def build_test_program():
    return _Program([_Schedule(1, 42, datetime(2016, 9, 20, 8).time(), 72, 68),
                    _Schedule(2, 42, datetime(2016, 9, 20, 17, 30).time(), 70, 68),
                    _Schedule(3, 65, datetime(2016, 9, 20, 7, 15).time(), 72, 66),
                    _Schedule(4, 65, datetime(2016, 9, 20, 12, 00).time(), 72, 68)])

