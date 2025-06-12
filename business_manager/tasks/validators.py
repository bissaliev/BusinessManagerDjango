from datetime import datetime, timezone
from django.core.exceptions import ValidationError


def validate_datetime(value: datetime):
    now = datetime.now(timezone.utc)
    if value < now:
        raise ValidationError("Время и дата задачи не должна быть меньше текущей")
