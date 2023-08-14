from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base


class Repository(Base):
    table_name = 'repository'
    public_attrs = [
        'repoId',
        'serviceDomain',
        'serverDomain',
        'repoUrl',
        'sendMailType',
        'buildType',
        'nodeVersion',
        'deployStatus',
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
    ]
    all_attrs = public_attrs + private_attrs

    services = [
        {'name': 'backlog', 'domain': 'coopnext.backlog.jp/git'},
        {'name': 'github', 'domain': 'github.com'},
    ]

    allowed_vals = {
        'serviceDomain': [i['domain'] for i in services],
        'serverDomain': ['pgit.me', 'pgit.be'],
        'sendMailType': ['completed', 'failed', 'always', 'none'],
        'nodeJSVersion': ['18.X', '16.X', '14.X'],
        'buildType': ['npm', 'yarn'],
        'deployStatus': ['pending', 'inProgress', 'completed', 'failed', 'cancelled',
                         'onHold', 'retryPending', 'retryInProgress'],
    }
