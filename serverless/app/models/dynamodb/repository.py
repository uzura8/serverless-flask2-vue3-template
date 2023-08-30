from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base
from app.config_loader import config


class Repository(Base):
    table_name = 'repository'
    public_attrs = [
        'repoId',  # unique
        'repoCode',  # not unique
        'serverDomain',
        'serviceDomain',
        'serviceSegment',
        'repoName',
        # 'repoUrl',
        'sendMailType',
        'isBuildRequired',
        'buildType',
        'buildTargetDirPath'
        'nodeJSVersion',
        'deployStatus',
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'deployStatusUpdatedAt'
        'createdBy',
        'updatedBy',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_vals = {
        'serviceDomain': [i['domain'] for i in config['services']],
        'serverDomain': [i['domain'] for i in config['pgitClients']],
        'sendMailType': ['completed', 'failed', 'always', 'none'],
        'nodeJSVersion': ['18.X', '16.X', '14.X'],
        'buildType': ['npm', 'yarn'],
        'deployStatus': ['pending', 'inProgress', 'completed', 'failed'],
        # 'deployStatus': ['pending', 'inProgress', 'completed', 'failed', 'canceled',
        #                  'onHold', 'retryPending', 'retryInProgress'],
    }
