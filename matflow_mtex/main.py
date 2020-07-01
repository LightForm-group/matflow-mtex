'`matflow_mtex.main.py`'

from pathlib import Path
from textwrap import dedent

import numpy as np

from matflow_mtex import sources_mapper, cli_format_mapper, input_mapper, output_mapper
from matflow_mtex.scripting import get_wrapper_script


@sources_mapper(task='get_model_texture', method='unimodal', script='write_unimodal_ODF')
def write_unimodal_ODF():

    script_name = 'write_unimodal_ODF.m'
    snippets = [
        {
            'name': 'get_unimodal_ODF.m',
            'req_args': [
                'crystalSym',
                'specimenSym',
                'modalOrientationHKL',
                'modalOrientationUVW',
                'halfwidth',
            ],
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


@sources_mapper(task='get_model_texture', method='fibre', script='write_fibre_ODF')
def write_fibre_ODF():

    script_name = 'write_fibre_ODF.m'
    snippets = [
        {
            'name': 'get_fibre_ODF.m',
            'req_args': ['crystalSym', 'specimenSym', 'halfwidth'],
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


@sources_mapper(task='get_model_texture', method='random', script='write_random_ODF')
def write_random_ODF():

    script_name = 'write_random_ODF.m'
    snippets = [
        {
            'name': 'get_random_ODF.m',
            'req_args': ['crystalSym', 'specimenSym', 'numOrientations'],
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


@sources_mapper(task='estimate_ODF', method='from_CTF_file', script='estimate_ODF')
def estimate_ODF_from_CTF_file():

    script_name = 'estimate_ODF.m'
    snippets = [
        {
            'name': 'get_ODF_from_CTF_file.m',
            'req_args': ['CTF_file_path', 'specimenSym', 'phase'],
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


@sources_mapper(task='sample_texture', method='from_ODF', script='sample_texture')
def sample_texture_from_ODF():

    script_name = 'sample_texture.m'
    snippets = [
        {
            'name': 'load_ODF.m',
            'req_args': ['crystalSym', 'specimenSym'],
        },
        {
            'name': 'sample_ODF_orientations.m',
            'req_args': ['numOrientations'],
        },
        {'name': 'export_orientations.m'},
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@input_mapper(input_file='ODF.txt', task='sample_texture', method='from_ODF')
def write_ODF_file(path, ODF):
    'Write out ODF into an "MTEX" text file'

    ang_labs = ODF['euler_angle_labels']

    odf_header = dedent(f"""
        % MTEX ODF
        % crystal symmetry: "{ODF['crystal_symmetry']}"
        % specimen symmetry: "{ODF['specimen_symmetry']}"
        % {ang_labs[0]} {ang_labs[1]} {ang_labs[2]} value
    """).strip()

    data = np.hstack([ODF['euler_angles'], ODF['weights'][:, None]])
    np.savetxt(path, data, header=odf_header, fmt='%8.5f', comments='')


@output_mapper(output_name='ODF', task='get_model_texture', method='unimodal')
@output_mapper(output_name='ODF', task='get_model_texture', method='fibre')
@output_mapper(output_name='ODF', task='get_model_texture', method='random')
@output_mapper(output_name='ODF', task='estimate_ODF', method='from_CTF_file')
def parse_MTEX_ODF_file(path):

    crystal_sym = None
    specimen_sym = None
    euler_angle_labels = None

    with Path(path).open() as handle:
        contents = handle.readlines()

    num_header = 0
    for ln in contents:
        ln_s = ln.strip()
        if ln_s.startswith('%'):
            num_header += 1
            if 'crystal symmetry' in ln_s:
                crystal_sym = ln_s.split('"')[1]
            if 'specimen symmetry' in ln_s:
                specimen_sym = ln_s.split('"')[1]
        if ln_s.endswith('value'):
            euler_angle_labels = ln_s.split()[1:4]
        if crystal_sym and specimen_sym and euler_angle_labels:
            break

    data = np.loadtxt(str(path), skiprows=num_header)
    euler_angles = data[:, 0:3]
    weights = data[:, 3]

    ODF = {
        'crystal_symmetry': crystal_sym,
        'specimen_symmetry': specimen_sym,
        'euler_angle_labels': euler_angle_labels,
        'euler_angles': euler_angles,
        'weights': weights,
    }
    return ODF


@output_mapper(output_name='orientations', task='sample_texture', method='from_ODF')
def parse_orientations(path):

    with Path(path).open() as handle:
        ln = handle.readline()
        euler_angle_labels = ln.split()

    euler_angles = np.loadtxt(str(path), skiprows=1)

    orientations = {
        'euler_angle_labels': euler_angle_labels,
        'euler_angles': euler_angles,
    }
    return orientations


@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='random')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='random')
@cli_format_mapper(input_name='specimen_symmetry', task='estimate_ODF', method='from_CTF_file')
@cli_format_mapper(input_name='modal_orientation_hkl', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='modal_orientation_uvw', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='halfwidth', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='halfwidth', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='CTF_file_path', task='estimate_ODF', method='from_CTF_file')
@cli_format_mapper(input_name='phase', task='estimate_ODF', method='from_CTF_file')
def default_CLI_formatter(input_val):

    if isinstance(input_val, list):
        input_val = '[' + ' '.join([f'{i}' for i in input_val]) + ']'

    return f'"{input_val}"'
