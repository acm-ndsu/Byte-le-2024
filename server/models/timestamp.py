from datetime import datetime, timezone
import sqlalchemy as sa


class TimeStamp(sa.types.TypeDecorator):
    """
    This class is used to create time stamps for things like when clients submit code during the competiton.
    """
    impl = sa.types.DateTime

# if datetime is none, returns datetime. if timezone is none, returns local timezone.
    def process_bind_param(self, value: datetime, dialect):
        if value is None:
            return datetime.utcnow()

        return value

# changes timezone to utc timezone
    def process_result_value(self, value: datetime, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value
