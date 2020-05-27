import os
import sys
import inspect
import json
import textwrap
from utils.log import log, log_colors


missing_env_vars = []


class to:
    STR = 'str'
    INT = 'int'
    BOOL = 'bool'
    ABS_PATH = 'abs_path'
    LIST_OF_INTS = 'list_of_ints'

    def parse(value, to_type):
        if to_type == to.STR:
            return value

        if to_type == to.BOOL:
            return value == '1'

        if to_type == to.INT:
            return int(value)

        if to_type == to.LIST_OF_INTS:
            return [int(item) for item in value.split(',')]

        if to_type == to.ABS_PATH:
            if os.path.isabs(value):
                return value
            else:
                value = os.path.join(os.getcwd(), value)
                return os.path.normpath(value)

        return value


def env(key, to_type=to.STR):
    value = os.environ.get(key)

    if value is None or value == '':
        missing_env_vars.append(key)
        return None

    try:
        return to.parse(value, to_type)
    except Exception:
        message = (
            f'Count not parse {key} to {to_type}. ' +
            'Please check your environment.')
        log(message, color=log_colors.FAIL)
        sys.exit(1)


def as_dict(module):
    sections = [
        (name, obj)
        for name, obj in inspect.getmembers(module)
        if inspect.isclass(obj) and name not in ['to', 'partial']
    ]

    return {
        section: {
            key: value
            for key, value in dict(vars(obj)).items()
            if not key.startswith('_')
        }
        for section, obj in sections
    }


def warn_missing():
    for var in missing_env_vars:
        warning = f'WARNING: {var} is missing in your environment.'
        log(warning, color=log_colors.WARNING)


def show(module):
    settings = as_dict(module)
    for section, pairs in settings.items():
        log(section)
        for key, value in pairs.items():
            if isinstance(value, dict):
                disp = textwrap \
                    .indent(json.dumps(value, indent=2), '\t') \
                    .replace('\t{', '{')
                log(f'\t{key} = {disp}')
            else:
                log(f'\t{key} = {value}')
        log()

    warn_missing()
