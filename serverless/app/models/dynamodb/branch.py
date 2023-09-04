from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base
from app.config_loader import config


class Branch(Base):
    table_name = 'branch'
    public_attrs = [
        'branchId',  # unique
        'repoId',
        'branchName',
        'repoCode',  # not unique
        'serverDomain',
        'serviceDomain',
        'serviceSegment',
        'repoName',
        'createdAt',
        'updatedAt',
        'lastCommitInfo',
    ]
    response_attrs = public_attrs + [
    ]
    private_attrs = [
        # 'createdBy',
        # 'updatedBy',
    ]
    all_attrs = public_attrs + private_attrs

    allowed_vals = {
        'serviceDomain': [i['domain'] for i in config['services']],
        'serverDomain': [i['domain'] for i in config['pgitClients']],
    }
