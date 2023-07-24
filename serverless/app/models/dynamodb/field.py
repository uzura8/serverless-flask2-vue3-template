"""This module provides an example import from the `app.models.dynamodb.base` module."""

from app.models.dynamodb.base import Base


class Field(Base):
    """DynamoDB Model class for `field` table."""

    table_name = 'field'
    public_attrs = [
        'fieldId',
        'slug',
        'name',
        'body',
        'createdAt',
        'updatedAt',
        'profileImage',
        'images',
        # 'zipCode',
        'address',
        'tel',
        'website',
        'fieldType',
        'categoryRegionSlug',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'createdBy',
        'categoryContentDiv',
        'categoryRegionPathSlug',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_field_types = ['outdoor', 'indoor', 'paintball']
