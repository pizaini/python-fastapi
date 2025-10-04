import datetime
from typing import Union

import pendulum
from pendulum import DateTime

APP_TIMEZONE = 'Asia/Jakarta'
pendulum.set_local_timezone(pendulum.timezone(APP_TIMEZONE))
pendulum.set_locale('id')

def datetime_to_diff_for_humans(dt_object: Union[pendulum.DateTime, datetime]) -> str:
    pendulum_dt = pendulum.instance(dt_object, tz=pendulum.timezone(APP_TIMEZONE))
    return pendulum_dt.diff_for_humans()

def datetime_local(dt_object: Union[pendulum.DateTime, datetime]) -> str:
    pendulum_dt = pendulum.instance(dt_object, tz=pendulum.timezone(APP_TIMEZONE))
    return pendulum_dt.format('DD MMMM YYYY HH:mm')

def date_local(dt_object: Union[pendulum.DateTime, datetime]) -> str:
    pendulum_dt = pendulum.instance(dt_object, tz=pendulum.timezone(APP_TIMEZONE))
    return pendulum_dt.format('DD MMMM YYYY')

def get_app_datetime() -> DateTime:
    return pendulum.now(tz=pendulum.timezone(APP_TIMEZONE))