"""This module provides an example import from the `app.models.dynamodb` package."""

from app.models.dynamodb.base import Base
# from app.models.dynamodb.game import Game


class UserGame(Base):
    """DynamoDB Model class for `user-game` table."""

    table_name = 'user-game'
    public_attrs = [
        'gameUserId',
        'gameId',
        'userId',
        'eventId',
        'killCount',
        'deathCount',
        'isFlagGet',
        'gameMemo',
        'createdAt',
        'updatedAt',
        'images',
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'userIdEventId',
    ]
    all_attrs = public_attrs + private_attrs

    # @classmethod
    # def create(self, vals, uuid_name=None):
    #    """Create a new game."""
    #    # TODO: implement transaction
    #    game_num = Event.increament_game_num(vals['eventId'])
    #    vals['gameNumber'] = game_num

    #    return super().create(vals, uuid_name)
