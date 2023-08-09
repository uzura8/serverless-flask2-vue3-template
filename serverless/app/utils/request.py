from app.utils.error import InvalidUsage
from app.validators import ValidatorExtended


def validate_req_params(schema, params=None, accept_keys=None):
    target_schema = {}
    target_vals = {}
    if params:
        for key, val in params.items():
            if accept_keys and key not in accept_keys:
                raise InvalidUsage('Field {} is not accepted'.format(key), 400)

            if key in schema:
                target_schema[key] = schema[key]
                target_vals[key] = val

    v = ValidatorExtended(target_schema)
    if not v.validate(target_vals):
        msg = 'Validation Failed'
        field_errs = []
        err_dict = v.errors
        for key, errs in err_dict.items():
            for err in errs:
                field_errs.append({
                    'field': key,
                    'message': err,
                })

        raise InvalidUsage(msg, 400, {'errors': field_errs})

    return v.document


def validate_params(schema, req_params, add_params=None):
    # req_params = req_params.to_dict()
    params = {**req_params, **add_params} if add_params else req_params
    vals = validate_req_params(schema, params)
    return vals
