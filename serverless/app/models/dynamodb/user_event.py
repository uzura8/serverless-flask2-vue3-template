"""This module provides an example import from the `app.models.dynamodb` package."""

from app.models.dynamodb.base import Base
#from app.models.dynamodb.event import Event


class UserEvent(Base):
    """DynamoDB Model class for `user-event` table."""

    table_name = 'user-event'
    public_attrs = [
        'userId',
        'eventId',
        'createdAt',
        'updatedAt',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'userIdEventId',
    ]
    all_attrs = public_attrs + private_attrs
