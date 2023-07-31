from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base


class Server(Base):
    table_name = 'server'
    public_attrs = [
        'domain',
        'isExecuting',
        'availableNodeVersions',
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
    ]
    all_attrs = public_attrs + private_attrs
