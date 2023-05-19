"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base
from app.models.dynamodb.event import Event


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

    @classmethod
    def create(self, vals, uuid_name=None):
        """Create a new game."""
        # TODO: implement transaction
        game_num = Event.increament_game_num(vals['eventId'])
        vals['gameNum'] = game_num

        return super().create(vals, uuid_name)
