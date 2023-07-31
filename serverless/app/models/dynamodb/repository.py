from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base


class Repository(Base):
    table_name = 'repository'
    public_attrs = [
        'repoId',
        'serverDomain',
        'repoUrl',
        'sendMailType',
        'buildType',
        'nodeVersion',
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
    ]
    all_attrs = public_attrs + private_attrs

    allowed_vals = {
        'sendMailType': ['completed', 'failed', 'always', 'none'],
        'buildType': ['npm', 'yarn', 'none'],
    }
