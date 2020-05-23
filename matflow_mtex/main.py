'`matflow_mtex.main.py`'

from collections import OrderedDict
from subprocess import run, PIPE

from matflow_mtex import software_versions, sources_mapper, cli_format_mapper
from matflow_mtex.scripting import get_wrapper_script


@sources_mapper(task='get_model_texture', method='unimodal', script='write_unimodal_ODF')
def write_unimodal_ODF():

    script_name = 'write_unimodal_ODF.m'
    snippets = [
        {
            'name': 'get_unimodal_ODF.m',
            'req_args': ['crystalSym', 'specimenSym', 'modalOrientation', 'halfwidth'],
        },
        {
            'name': 'export_ODF.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='modal_orientation', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='halfwidth', task='get_model_texture', method='unimodal')
def default_CLI_formatter(input_val):

    if isinstance(input_val, list):
        input_val = '[' + ' '.join([f'{i}' for i in input_val]) + ']'

    return f'"{input_val}"'


@software_versions()
def get_versions(matlab_executable='matlab'):
    'Get MTEX and MATLAB versions.'

    cmd = [
        matlab_executable,
        '-wait',
        '-log',
        '-nosplash',
        '-nodesktop',
        '-r',
        r'''"fprintf('MATLAB version: %s\n', version); exit"''',
    ]
    proc = run(cmd, stdout=PIPE, stderr=PIPE)
    _, stderr = proc.stdout.decode(), proc.stderr.decode()

    # For some reason MATLAB sends stdout to stderr:
    matlab_version_str = re.search('MATLAB version: (.*)', stderr).group(1).strip()

    out = {
        'MATLAB': matlab_version_str,
        'MTEX': None,
    }
    return out
