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
        'gameTypeNote',
        'duration',
        'durationUnit',
        'isUnlimitedRespawn',
        'respawnCount',
        'firepowerLimitType',
        'firepowerLimitNote',
        'joinedCount',
        'matchResultType',
        'matchResultNote',
        'respawnCount',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'createdBy',
        'createdUserType',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_event_types = []

    @classmethod
    def create(self, vals, uuid_name=None):
        """Create a new game."""
        # TODO: implement transaction
        if vals.get('gameNumber'):
            game_num = vals['gameNumber']
            event = Event.get_one_by_pkey('eventId', vals['eventId'])
            current_game_num = event.get('gameNumber')
            if game_num > current_game_num:
                keys = {'p': {'key': 'eventId', 'val': vals['eventId']}}
                Event.update(keys, {'gameNumber': game_num})
        else:
            game_num = Event.increament_game_num(vals['eventId'])
            vals['gameNumber'] = game_num

        return super().create(vals, uuid_name)
