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
        'gameNum'
    ]

    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'fieldIdDate',
        'createdBy',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_event_types = []

    @classmethod
    def increament_game_num(self, event_id, is_check_exist=False):
        """Increament game number."""

        if is_check_exist:
            item = self.get_one_by_pkey('eventId', event_id)
            if not item:
                raise Exception('Event not found')

        table = self.get_table()
        table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='ADD gameNum :incr',
            ExpressionAttributeValues={':incr': 1}
        )
        item = self.get_one_by_pkey('eventId', event_id)
        return item['gameNum']
