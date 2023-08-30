from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base
from app.config_loader import config


class Job(Base):
    table_name = 'job'
    public_attrs = [
        'jobId',
        'serverDomain',
        'serviceDomain',
        'serviceSegment',
        'repoName',
        'repoId',
        'repoCode',
        'branchName',
        'deployStatus',
        'deployType',
        'isBuildRequired',
        'buildType',
        'nodeJSVersion',
        'lastCommitInfo',
        # 'lastCommitTime'
        # 'lastCommitBy'
        'createdAt',
        'updatedAt',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        'deployStatusCreatedAt',
        'reqRawData',
        'resultLog',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_vals = {
        'serviceDomain': [i['domain'] for i in config['services']],
        'serverDomain': [i['domain'] for i in config['pgitClients']],
        'deployType': ['add', 'update', 'delete'],
        'deployStatus': ['pending', 'inProgress', 'completed', 'failed'],
        # 'deployStatus': ['pending', 'inProgress', 'completed', 'failed', 'canceled',
        #                  'onHold', 'retryPending', 'retryInProgress'],
    }
