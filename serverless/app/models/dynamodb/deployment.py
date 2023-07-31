from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base


class Deployment(Base):
    table_name = 'server'
    public_attrs = [
        'deployId',
        'serverDomain',
        'repoId',
        'branch',
        'deployType',
        'deployStatus',
        'lastCommitId',
        'lastCommitTime'
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'reqRawData',
        'resultLog',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_vals = {
        'deployType': ['add', 'update', 'delete'],
        'deployStatus': ['pending', 'running', 'completed', 'failed'],
    }
