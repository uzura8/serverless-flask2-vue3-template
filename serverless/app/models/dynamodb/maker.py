"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base


class Maker(Base):
    """DynamoDB Model class for `field` table."""

    table_name = 'maker'
    public_attrs = [
        'makerId',
        'slug',
        'labels',
        'categoryRegionSlug',
        'createdAt',
        'updatedAt',
        'profileImage',
        'images',
        'description',
        'website',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'createdBy',
    ]
    all_attrs = public_attrs + private_attrs
