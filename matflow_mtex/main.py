'`matflow_mtex.main.py`'

import json
import copy
from pathlib import Path
from textwrap import dedent
import warnings

import numpy as np
from damask_parse.utils import validate_orientations, parse_inc_specs

from matflow_mtex import sources_mapper, cli_format_mapper, input_mapper, output_mapper
from matflow_mtex.scripting import get_wrapper_script
from matflow_mtex.utils import to_camel_case


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


@sources_mapper(task='estimate_ODF', method='from_CRC_file', script='estimate_ODF')
def estimate_ODF_from_CRC_file():

    script_name = 'estimate_ODF.m'
    snippets = [
        {
            'name': 'get_ODF_from_CRC_file.m',
            'req_args': ['CRC_file_path', 'specimenSym', 'phase'],
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


@sources_mapper(task='sample_texture', method='from_model_ODF', script='sample_texture')
def sample_texture_from_model_ODF():

    script_name = 'sample_texture.m'
    snippets = [
        {
            'name': 'get_model_ODF.m',
            'req_args': [
                'ODFComponentDefnsJSONPath',
                'crystalSym',
                'specimenSym',
            ],
        },
        {
            'name': 'sample_ODF_orientations.m',
            'req_args': ['numOrientations'],
        },
        {
            'name': 'export_orientations_JSON.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@sources_mapper(task='sample_texture', method='from_CTF_file', script='sample_texture')
def sample_texture_from_CTF_file():

    script_name = 'sample_texture.m'
    snippets = [
        {
            'name': 'get_EBSD_orientations_from_CTF_file.m',
            'req_args': [
                'CTF_file_path',
                'referenceFrameTransformation',
                'specimenSym',
                'phase',
                'rotationJSONPath',
            ],
        },
        {
            'name': 'get_ODF_from_EBSD_orientations.m',
        },
        {
            'name': 'sample_ODF_orientations.m',
            'req_args': ['numOrientations'],
        },
        {
            'name': 'export_orientations_JSON.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@sources_mapper(task='sample_texture', method='from_CRC_file', script='sample_texture')
def sample_texture_from_CRC_file():

    script_name = 'sample_texture.m'
    snippets = [
        {
            'name': 'get_EBSD_orientations_from_CRC_file.m',
            'req_args': [
                'CRC_file_path',
                'referenceFrameTransformation',
                'specimenSym',
                'phase',
                'rotationJSONPath',
            ],
        },
        {
            'name': 'get_ODF_from_EBSD_orientations.m',
        },
        {
            'name': 'sample_ODF_orientations.m',
            'req_args': ['numOrientations'],
        },
        {
            'name': 'export_orientations_JSON.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@sources_mapper(task='sample_orientations', method='from_CTF_file', script='sample_orientations')
def sample_orientations_from_CTF_file():

    script_name = 'sample_orientations.m'
    snippets = [
        {
            'name': 'get_EBSD_orientations_from_CTF_file.m',
            'req_args': [
                'CTF_file_path',
                'referenceFrameTransformation',
                'specimenSym',
                'phase',
                'rotationJSONPath',
            ],
        },
        {
            'name': 'randomly_sample_EBSD_orientations.m',
            'req_args': ['numOrientations'],
        },
        {
            'name': 'export_orientations_JSON.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@sources_mapper(task='sample_orientations', method='from_CRC_file', script='sample_orientations')
def sample_orientations_from_CRC_file():

    script_name = 'sample_orientations.m'
    snippets = [
        {
            'name': 'get_EBSD_orientations_from_CRC_file.m',
            'req_args': [
                'CRC_file_path',
                'referenceFrameTransformation',
                'specimenSym',
                'phase',
                'rotationJSONPath',
            ],
        },
        {
            'name': 'randomly_sample_EBSD_orientations.m',
            'req_args': ['numOrientations'],
        },
        {
            'name': 'export_orientations_JSON.m',
        },
    ]
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets),
            'filename': script_name,
        }
    }
    return out


@sources_mapper(task='visualise_orientations', method='pole_figure', script='visualise_orientations')
@sources_mapper(task='visualise_volume_element_response', method='texture_pole_figure', script='visualise_orientations')
def plot_pole_figure():

    script_name = 'visualise_orientations.m'
    snippets = [
        {
            'name': 'plot_pole_figure.m',
            'req_args': [
                'orientationsPath',
                'poleFigureDirections',
                'use_contours',  # todo change to camel case?
                'IPF_reference_direction', # todo change to camel case?
            ],
        },
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


@input_mapper(
    input_file='orientation_coordinate_system.json',
    task='sample_texture',
    method='from_ODF',
)
def write_ori_coord_sys_from_ODF(path, ODF):
    with Path(path).open('w') as handle:
        json.dump(ODF['orientation_coordinate_system'], handle)


@input_mapper(
    input_file='orientations.json',
    task='visualise_orientations',
    method='pole_figure',
)
def write_orientations(path, orientations, crystal_symmetry):

    orientations = validate_orientations(orientations)

    with Path(path).open('w') as handle:

        if 'euler_angles' in orientations:
            orientations['euler_angles'] = np.array(orientations['euler_angles']).tolist()
        if 'quaternions' in orientations:
            orientations['quaternions'] = np.array(orientations['quaternions']).tolist()
        orientations['crystal_symmetry'] = crystal_symmetry

        json.dump([orientations], handle, indent=4)


@input_mapper(
    input_file='orientations.json',
    task='visualise_volume_element_response',
    method='texture_pole_figure',
)
def write_orientations_from_VE_response(path, volume_element_response, increments,
                                        crystal_symmetries, phases,
                                        orientation_coordinate_system):

    if increments is None:
        increments = [{'values': [-1]}]  # final increment only by default

    oris_out = volume_element_response['field_data']['O']

    phases_out = volume_element_response['field_data']['phase']
    phases_out_dat = phases_out['data'].flatten()
    phase_names_out = phases_out['meta']['phase_names']

    if phases is None:
        phases = [phase_names_out[0]]  # first phase only by default

    phase_names_idx = [phase_names_out.index(i) for i in phases]

    # 1D bool array to get which voxel orientations to include:
    use_voxels = np.logical_or.reduce(
        tuple([phases_out_dat == i for i in phase_names_idx])
    )

    available_incs = oris_out['meta']['increments']

    ori_JSON_data = []
    for inc in parse_inc_specs(increments, available_incs):
        # Want to generate pole figure image for each increment

        ori_dat_inc_i_index = available_incs.index(inc)

        quats_inc_i = oris_out['data']['quaternions'][ori_dat_inc_i_index]
        quats_inc_i_flat = quats_inc_i.reshape((-1, 4))
        quats_inc_i_flat_sub = quats_inc_i_flat[use_voxels]

        ori_dict_i = copy.deepcopy(oris_out['data'])
        ori_dict_i['quaternions'] = quats_inc_i_flat_sub.tolist()

        crystal_syms = set(crystal_symmetries[i] for i in phases)
        if len(crystal_syms) > 1:
            raise ValueError('Cannot generate a pole figure using multiple crystal '
                             f'symmetries.')
        else:
            crystal_sym = list(crystal_syms)[0]

        ori_dict_i['crystal_symmetry'] = crystal_sym
        ori_dict_i['increment'] = inc

        if orientation_coordinate_system:
            ori_dict_i['orientation_coordinate_system'] = orientation_coordinate_system

        ori_JSON_data.append(ori_dict_i)

    with Path(path).open('w') as handle:
        json.dump(ori_JSON_data, handle, indent=4)


@input_mapper(
    input_file='ODF_components.json',
    task='sample_texture',
    method='from_model_ODF',
)
def write_model_ODF_components(path, ODF_components):
    ODF_components = copy.deepcopy(ODF_components)
    for idx, ODF_comp in enumerate(ODF_components):
        for key in list(ODF_comp.keys()):
            ODF_components[idx][to_camel_case(key)] = ODF_comp.pop(key)
        # This hack adds a unique key to each ODF component definition, thus helping
        # to ensure that MATLAB's `jsondecode` loads into a cell array of structures
        # instead of a structure array:
        ODF_components[idx][f'index_{idx}'] = True
    with Path(path).open('w') as handle:
        json.dump(ODF_components, handle, indent=4)


@input_mapper(input_file='rotation.json', task='sample_texture', method='from_CTF_file')
@input_mapper(input_file='rotation.json', task='sample_texture', method='from_CRC_file')
@input_mapper(input_file='rotation.json', task='sample_orientations', method='from_CTF_file')
@input_mapper(input_file='rotation.json', task='sample_orientations', method='from_CRC_file')
def write_sample_texture_rotation(path, rotation):
    rotation = copy.deepcopy(rotation)
    with Path(path).open('w') as handle:
        json.dump(rotation, handle, indent=4)


@output_mapper(output_name='ODF', task='get_model_texture', method='unimodal')
@output_mapper(output_name='ODF', task='get_model_texture', method='fibre')
@output_mapper(output_name='ODF', task='get_model_texture', method='random')
@output_mapper(output_name='ODF', task='estimate_ODF', method='from_CTF_file')
@output_mapper(output_name='ODF', task='estimate_ODF', method='from_CRC_file')
def parse_MTEX_ODF_file(path, orientation_coordinate_system):

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

    data = np.loadtxt(str(path), skiprows=num_header, ndmin=2)
    euler_angles = data[:, 0:3]
    weights = data[:, 3]

    ODF = {
        'crystal_symmetry': crystal_sym,
        'specimen_symmetry': specimen_sym,
        'euler_angle_labels': euler_angle_labels,
        'euler_angles': euler_angles,
        'weights': weights,
        'orientation_coordinate_system': orientation_coordinate_system,
    }

    return ODF


@output_mapper(output_name='orientations', task='sample_texture', method='from_ODF')
def parse_orientations(path, ori_coord_sys_path):

    with Path(path).open() as handle:
        ln = handle.readline()
        euler_angle_labels = ln.split()

    euler_angles = np.loadtxt(str(path), skiprows=1, ndmin=2)

    with Path(ori_coord_sys_path).open() as handle:
        ori_coord_sys = json.load(handle)

    orientations = {
        'euler_angle_labels': euler_angle_labels,
        'euler_angles': euler_angles,
        'orientation_coordinate_system': ori_coord_sys,
    }
    return orientations


@output_mapper(output_name='orientations', task='sample_texture', method='from_model_ODF')
@output_mapper(output_name='orientations', task='sample_texture', method='from_CTF_file')
@output_mapper(output_name='orientations', task='sample_texture', method='from_CRC_file')
@output_mapper(output_name='orientations', task='sample_orientations', method='from_CTF_file')
@output_mapper(output_name='orientations', task='sample_orientations', method='from_CRC_file')
def parse_orientations_JSON(path, orientation_coordinate_system):

    with Path(path).open() as handle:
        orientations = json.load(handle)

    if 'euler_angles' in orientations:
        orientations['euler_angles'] = np.array(orientations['euler_angles'])
    if 'quaternions' in orientations:
        orientations['quaternions'] = np.array(orientations['quaternions'])

    if orientation_coordinate_system:
        orientations.update({
            'orientation_coordinate_system': orientation_coordinate_system,
        })

    return orientations


@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='crystal_symmetry', task='get_model_texture', method='random')
@cli_format_mapper(input_name='crystal_symmetry', task='sample_texture', method='from_model_ODF')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='specimen_symmetry', task='get_model_texture', method='random')
@cli_format_mapper(input_name='specimen_symmetry', task='estimate_ODF', method='from_CTF_file')
@cli_format_mapper(input_name='specimen_symmetry', task='estimate_ODF', method='from_CRC_file')
@cli_format_mapper(input_name='specimen_symmetry', task='sample_texture', method='from_model_ODF')
@cli_format_mapper(input_name='specimen_symmetry', task='sample_texture', method='from_CTF_file')
@cli_format_mapper(input_name='specimen_symmetry', task='sample_texture', method='from_CRC_file')
@cli_format_mapper(input_name='specimen_symmetry', task='sample_orientations', method='from_CTF_file')
@cli_format_mapper(input_name='specimen_symmetry', task='sample_orientations', method='from_CRC_file')
@cli_format_mapper(input_name='modal_orientation_hkl', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='modal_orientation_uvw', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='halfwidth', task='get_model_texture', method='unimodal')
@cli_format_mapper(input_name='halfwidth', task='get_model_texture', method='fibre')
@cli_format_mapper(input_name='CTF_file_path', task='estimate_ODF', method='from_CTF_file')
@cli_format_mapper(input_name='CRC_file_path', task='estimate_ODF', method='from_CRC_file')
@cli_format_mapper(input_name='CTF_file_path', task='sample_texture', method='from_CTF_file')
@cli_format_mapper(input_name='CRC_file_path', task='sample_texture', method='from_CRC_file')
@cli_format_mapper(input_name='CTF_file_path', task='sample_orientations', method='from_CTF_file')
@cli_format_mapper(input_name='CRC_file_path', task='sample_orientations', method='from_CRC_file')
@cli_format_mapper(input_name='phase', task='estimate_ODF', method='from_CTF_file')
@cli_format_mapper(input_name='phase', task='estimate_ODF', method='from_CRC_file')
@cli_format_mapper(input_name='phase', task='sample_texture', method='from_CTF_file')
@cli_format_mapper(input_name='phase', task='sample_texture', method='from_CRC_file')
@cli_format_mapper(input_name='phase', task='sample_orientations', method='from_CTF_file')
@cli_format_mapper(input_name='phase', task='sample_orientations', method='from_CRC_file')
def default_CLI_formatter(input_val):

    if isinstance(input_val, list):
        input_val = '[' + ' '.join([f'{i}' for i in input_val]) + ']'

    return f'"{input_val}"'


@cli_format_mapper(input_name='reference_frame_transformation', task='sample_texture', method='from_CTF_file')
@cli_format_mapper(input_name='reference_frame_transformation', task='sample_texture', method='from_CRC_file')
@cli_format_mapper(input_name='reference_frame_transformation', task='sample_orientations', method='from_CTF_file')
@cli_format_mapper(input_name='reference_frame_transformation', task='sample_orientations', method='from_CRC_file')
def reference_frame_formatter(ref_frame):
    if ref_frame == 'euler_to_spatial':
        return '"convertEuler2SpatialReferenceFrame"'
    elif ref_frame == 'spatial_to_euler':
        return '"convertSpatial2EulerReferenceFrame"'
    else:
        return '""'


@cli_format_mapper(input_name='pole_figure_directions', task='visualise_orientations', method='pole_figure')
@cli_format_mapper(input_name='pole_figure_directions', task='visualise_volume_element_response', method='texture_pole_figure')
def multiple_miller_indices_formatter(miller_directions):

    out = (
        '"{' +
        ' '.join(['{' + ' '.join([str(i) for i in miller_dir]) + '}'
                  for miller_dir in miller_directions]) +
        '}"'
    )

    return out


@cli_format_mapper(input_name='use_contours', task='visualise_orientations', method='pole_figure')
@cli_format_mapper(input_name='use_contours', task='visualise_volume_element_response', method='texture_pole_figure')
def bool_cli_formatter(arg):
    # Note we should use the `ensure_double` snippet in the matlab script as well.
    return f'{1 if arg else 0}'
