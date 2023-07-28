"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base


class Gun(Base):
    """DynamoDB Model class for `field` table."""

    table_name = 'gun'
    # makerId	gunGenre	poweredType   asin
    public_attrs = [
        'gunId',
        'labels',
        'makerId',
        'gunType',
        'poweredType',
        'asin',
        'createdAt',
        'updatedAt',
        'profileImage',
        'images',
        'description',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'createdBy',
    ]
    all_attrs = public_attrs + private_attrs
