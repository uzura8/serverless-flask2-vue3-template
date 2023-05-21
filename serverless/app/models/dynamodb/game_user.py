"""This module provides an example import from the `app.models.dynamodb` package."""

from app.models.dynamodb.base import Base
#from app.models.dynamodb.game import Game


class GameUser(Base):
    """DynamoDB Model class for `game_user` table."""

    table_name = 'game-user'
    public_attrs = [
        'gameUserId',
        'gameId',
        'userId',
        'killCount',
        'deathCount',
        'isFlugGet',
        'gameMemo',
        'createdAt',
        'updatedAt',
        'images',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
    ]
    all_attrs = public_attrs + private_attrs

    #@classmethod
    #def create(self, vals, uuid_name=None):
    #    """Create a new game."""
    #    # TODO: implement transaction
    #    game_num = Event.increament_game_num(vals['eventId'])
    #    vals['gameNumber'] = game_num

    #    return super().create(vals, uuid_name)
