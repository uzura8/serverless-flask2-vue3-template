"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base


class Game(Base):
    """DynamoDB Model class for `game` table."""

    table_name = 'game'
    public_attrs = [
        'gameId',
        'eventId',
        'gameNumber',
        'name',
        'body',
        'createdAt',
        'updatedAt',
        'images',
        'gameType',
        'gameTypeText',
        'duration',
        'durationUnit',
        'joinedCount',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'createdBy',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_event_types = []
