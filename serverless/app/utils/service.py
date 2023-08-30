from app.utils.string import sanitize_domain_str
from app.config_loader import config


def generate_repo_id(service_domain, service_segment, repo_name):
    services = config['services']
    name = next((service['name']
                for service in services if service['domain'] == service_domain), None)
    if not name:
        return

    suffix = '-'.join([sanitize_domain_str(service_segment),
                       sanitize_domain_str(repo_name)])
    return f'{name}.{suffix}'
