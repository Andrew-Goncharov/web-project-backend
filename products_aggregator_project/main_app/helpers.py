import datetime as dt


def is_valid_datetime(value: str) -> bool:
    try:
        dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z')
        return True
    except Exception as e:
        return False