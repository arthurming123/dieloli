import datetime
import random
import math
import ephem
from types import FunctionType
from dateutil import relativedelta
from Script.Core import (
    cache_control,
    game_type,
    get_text,
)
from Script.Config import normal_config, game_config

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """


def init_time():
    """
    初始化游戏时间
    """
    game_time = datetime.datetime(
        normal_config.config_normal.year,
        normal_config.config_normal.month,
        normal_config.config_normal.day,
        normal_config.config_normal.hour,
        normal_config.config_normal.minute,
    )
    cache.game_time = game_time


def get_date_text(game_time_data: datetime.datetime = None) -> str:
    """
    获取时间信息描述文本
    Keyword arguments:
    game_timeData -- 时间数据，若为None，则获取当前游戏时间
    """
    if game_time_data is None:
        game_time_data = cache.game_time
    return _("时间:{year}年{month}月{day}日{hour}点{minute}分").format(
        year=game_time_data.year,
        month=game_time_data.month,
        day=game_time_data.day,
        hour=game_time_data.hour,
        minute=game_time_data.minute,
    )


def get_week_day_text() -> str:
    """
    获取星期描述文本
    """
    week_day = cache.game_time.weekday()
    week_date_data = game_config.config_week_day[week_day]
    return week_date_data.name


def sub_time_now(minute=0, hour=0, day=0, month=0, year=0) -> datetime.datetime:
    """
    增加当前游戏时间
    Keyword arguments:
    minute -- 增加的分钟
    hour -- 增加的小时
    day -- 增加的天数
    month -- 增加的月数
    year -- 增加的年数
    """
    new_date = get_sub_date(minute, hour, day, month, year)
    cache.game_time = new_date


def get_sub_date(
    minute=0,
    hour=0,
    day=0,
    month=0,
    year=0,
    old_date: datetime.datetime = None,
) -> datetime.datetime:
    """
    获取旧日期增加指定时间后得到的新日期
    Keyword arguments:
    minute -- 增加分钟
    hour -- 增加小时
    day -- 增加天数
    month -- 增加月数
    year -- 增加年数
    old_date -- 旧日期，若为None，则获取当前游戏时间
    """
    if old_date is None:
        old_date = cache.game_time
    new_date = old_date + relativedelta.relativedelta(
        years=year, months=month, days=day, hours=hour, minutes=minute
    )
    return new_date


def get_rand_day_for_year(year: int) -> datetime.datetime:
    """
    随机获取指定年份中一天的日期
    Keyword arguments:
    year -- 年份
    Return arguments:
    time.time -- 随机日期
    """
    start = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
    end = datetime.datetime(year, 12, 31, 23, 59, 59)
    return get_rand_day_for_date(start, end)


def timetuple_to_datetime(t: datetime.datetime.timetuple) -> datetime.datetime:
    """
    将timetulp类型数据转换为datetime类型
    Keyword arguments:
    t -- timetulp类型数据
    Return arguments:
    d -- datetime类型数据
    """
    return datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)


def get_rand_day_for_date(start_date: datetime.datetime, end_date: datetime.datetime) -> datetime.datetime:
    """
    随机获取两个日期中的日期
    Keyword arguments:
    start_date -- 开始日期
    end_date -- 结束日期
    Return arguments:
    time.localtime -- 随机日期
    """
    sub_day = (end_date - start_date).days
    sub_day = random.randint(0, sub_day)
    return get_sub_date(day=sub_day, old_date=start_date)


def count_day_for_datetime(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> int:
    """
    计算两个时间之间经过的天数
    Keyword arguments:
    start_date -- 开始时间
    end_date -- 结束时间
    Return arguments:
    int -- 经过天数
    """
    return (start_date - end_date).days


def judge_date_big_or_small(time_a: datetime.datetime, time_b: datetime.datetime) -> int:
    """
    比较当前时间是否大于或等于旧时间
    Keyword arguments:
    time_a -- 当前时间
    time_b -- 旧时间
    Return arguments:
    0 -- 小于
    1 -- 大于
    2 -- 等于
    """
    if time_a == time_b:
        return 2
    else:
        return time_b < time_a


def ecliptic_lon(now_time: datetime.datetime) -> float:
    """
    根据日期计算黄经
    now_time -- 日期
    Return arguments:
    float -- 黄经
    """
    s = ephem.Sun(now_time)
    equ = ephem.Equatorial(s.ra, s.dec, epoch=now_time)
    e = ephem.Ecliptic(equ)
    return e.lon


def get_solar_period(now_time: datetime.datetime) -> int:
    """
    根据日期计算对应节气id
    Keyword arguments:
    now_time -- 日期
    Return arguments:
    int -- 节气id
    """
    e = ecliptic_lon(now_time)
    n = int(e * 180.0 / math.pi / 15)
    return n


def get_old_solar_period_time(now_time: datetime.datetime) -> (datetime.datetime, int):
    """
    根据日期计算上个节气的开始日期
    Keyword arguments:
    now_time -- 日期
    Return arguments:
    new_time -- 节气日期
    """
    s1 = get_solar_period(now_time)
    s0 = s1
    dt = 1
    new_time = now_time
    while True:
        new_time = get_sub_date(day=-dt, old_date=new_time)
        s = get_solar_period(new_time)
        if s0 != s:
            s0 = s
            dt = -dt / 2
        if s != s1 and abs(dt) < 1:
            break
    return new_time, s0


def get_next_solar_period_time(now_time: datetime.datetime) -> (datetime.datetime, int):
    """
    根据日期计算下个节气的开始日期
    Keyword arguments:
    now_time -- 日期
    Return arguments:
    new_time -- 节气日期
    """
    s1 = get_solar_period(now_time)
    s0 = s1
    dt = 1
    new_time = now_time
    while True:
        new_time = get_sub_date(day=dt, old_date=new_time)
        s = get_solar_period(new_time)
        if s0 != s:
            s0 = s
            dt = -dt / 2
        if s != s1 and abs(dt) < 1:
            break
    return new_time, s0


def judge_datetime_solar_period(now_time: datetime.datetime) -> (bool, int):
    """
    校验日期是否是节气以及获取节气id
    Keyword arguments:
    now_time -- 日期
    Return arguments:
    bool -- 校验结果
    int -- 节气id
    """
    new_time, solar_period = get_old_solar_period_time(now_time)
    if new_time.year == now_time.year and new_time.month == now_time.month and new_time.day == now_time.day:
        return 1, solar_period
    new_time, solar_period = get_next_solar_period_time(now_time)
    if new_time.year == now_time.year and new_time.month == now_time.month and new_time.day == now_time.day:
        return 1, solar_period
    return 0, 0


def get_sun_time(now_time: datetime.datetime) -> int:
    """
    根据时间获取太阳位置id
    Keyword arguments:
    now_time -- 时间
    Return arguments:
    int -- 太阳位置id
    """
    gatech = ephem.Observer()
    gatech.long, gatech.lat = str(cache.school_longitude), str(cache.school_latitude)
    now_add_time = round(cache.school_longitude / 15)
    gatech.date = get_sub_date(hour=-now_add_time, old_date=now_time)
    sun = ephem.Sun()
    sun.compute(gatech)
    now_az = sun.az * 57.2957795
    if now_az >= 225 and now_az < 255:
        return 8
    elif now_az >= 255 and now_az < 285:
        return 9
    elif now_az >= 285 and now_az < 315:
        return 10
    elif now_az >= 315 and now_az < 345:
        return 11
    elif now_az >= 345 or now_az < 15:
        return 0
    elif now_az >= 15 and now_az < 45:
        return 1
    elif now_az >= 45 and now_az < 75:
        return 2
    elif now_az >= 75 and now_az < 105:
        return 3
    elif now_az >= 105 and now_az < 135:
        return 4
    elif now_az >= 135 and now_az < 165:
        return 5
    elif now_az >= 165 and now_az < 195:
        return 6
    return 7


def get_moon_phase(now_time: datetime.datetime) -> int:
    """
    根据时间获取月相配置id
    Keyword arguments:
    now_time -- 时间
    Return arguments:
    int -- 月相配置id
    """
    gatech = ephem.Observer()
    gatech.long, gatech.lat = str(cache.school_longitude), str(cache.school_latitude)
    now_add_time = round(cache.school_longitude / 15)
    new_time = get_sub_date(hour=-now_add_time, old_date=now_time)
    gatech.date = new_time
    moon = ephem.Moon()
    moon.compute(gatech)
    now_phase = moon.phase
    new_time = get_sub_date(day=1, old_date=new_time)
    gatech.date = new_time
    next_moon = ephem.Moon()
    next_moon.compute(gatech)
    next_phase = next_moon.phase
    now_type = next_phase > now_phase
    for phase in game_config.config_moon_data[now_type]:
        phase_config = game_config.config_moon[phase]
        if now_phase > phase_config.min_phase and now_phase <= phase_config.max_phase:
            return phase_config.cid


def judge_attend_class_today(character_id: int) -> bool:
    """
    校验角色今日是否需要上课
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time is None:
        now_time = cache.game_time
    now_week = now_time.weekday()
    now_month = now_time.month
    if now_month not in {3, 4, 5, 6, 8, 9, 10, 11, 12}:
        return 0
    if character_data.age <= 18:
        if character_data.age <= 12 and now_week < 5:
            return 1
        elif character_data.age <= 15 and now_week < 6:
            return 1
        elif character_data.age <= 18 and character_data.age > 15:
            return 1
    elif (
        character_id in cache.teacher_phase_table
        and now_week in cache.teacher_class_week_day_data[character_id]
    ):
        return 1
    return 0
