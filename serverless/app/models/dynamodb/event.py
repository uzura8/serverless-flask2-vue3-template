"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base

class Event(Base):
    """DynamoDB Model class for `event` table."""

    table_name = 'event'
    public_attrs = [
        'eventId',
        'fieldId',
        'date',
        'name',
        'body',
        'createdAt',
        'updatedAt',
        'images',
        'eventType',
        'weatherType',
        'weatherText',
        'joinedCount',
        'windType',
        'temperature',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'fieldIdDate',
        'createdBy',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_event_types = []
