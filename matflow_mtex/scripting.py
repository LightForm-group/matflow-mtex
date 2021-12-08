import re
from textwrap import indent, dedent

from pkg_resources import resource_string

SNIPPETS_ARG_TYPES = {
    'get_unimodal_ODF.m': {
        'ensure_types': {
            'modalOrientationUVW': '1D_matrix',
            'modalOrientationHKL': '1D_matrix',
            'halfwidth': 'double',
        },
    },
    'get_model_ODF.m': {},
    'get_fibre_ODF.m': {
        'ensure_types': {
            'halfwidth': 'double',
        },
    },
    'get_random_ODF.m': {'ensure_types': {'numOrientations': 'double'}},
    'export_ODF.m': {'defaults': {'fileName': 'ODF.txt'}},
    'get_EBSD_orientations_from_CTF_file.m': {},
    'get_EBSD_orientations_from_CRC_file.m': {},
    'get_ODF_from_EBSD_orientations.m': {},
    'randomly_sample_EBSD_orientations.m': {'ensure_types': {'numOrientations': 'double'}},
    'sample_ODF_orientations.m': {'ensure_types': {'numOrientations': 'double'}},
    'load_ODF.m': {'defaults': {'ODF_path': 'ODF.txt'}},
    'export_orientations.m': {'defaults': {'fileName': 'orientations.txt'}},
    'export_orientations_JSON.m': {'defaults': {'fileName': 'orientations.json'}},
    'plot_pole_figure.m': {
        'ensure_types': {
            'poleFigureDirections': '2D_cell_array',
            'use_contours': 'double',
        }
    },
}


def get_snippet(name):
    'Get a MATLAB snippet function (as a string) from the snippets directory.'
    return resource_string('matflow_mtex', f'snippets/{name}').decode()


def get_snippet_signature(name):
    'Return a list of function arguments and the return label of a given snippet file.'
    snippet_str = get_snippet(name)
    pattern = r'function (\w+) = (\w+)\((.*)\)'
    output, func_name, inputs = re.match(pattern, snippet_str).groups()
    if f'{func_name}.m' != name:
        raise ValueError('The function name should be the same as the snippet file name.')
    inputs = [i.strip() for i in inputs.split(',')]
    out = {
        'name': func_name,
        'inputs': inputs,
        'output': output,
    }
    return out


def get_wrapper_script(script_name, snippet_args):
    'Return a string representing a MATLAB script comprised of multiple snippets.'

    all_req_args = [j for i in snippet_args for j in i.get('req_args', [])]
    wrap_inputs = ', '.join(all_req_args + ['varargin'])
    parse_inputs = ', '.join(all_req_args + [r'varargin{:}'])
    parser_name = 'parser'

    ind = '    '

    snippet_sigs = [get_snippet_signature(i['name']) for i in snippet_args]
    all_inputs = [j for i in snippet_sigs for j in i['inputs']]
    all_outputs = [i['output'] for i in snippet_sigs]
    all_specified_args = [i for i in all_inputs if i not in all_outputs]

    parser_add_req = f'\n{ind}'.join([f'addRequired({parser_name}, {i!r});'
                                      for i in all_req_args])

    optional_ins = set(all_specified_args) - set(all_req_args)

    includes = [i['name'] for i in snippet_args]
    parser_add_opt = []
    for i in optional_ins:
        opt_default = None
        for k, v in SNIPPETS_ARG_TYPES.items():
            if k in includes and i in v.get('defaults', {}):
                opt_default = v['defaults'][i]
        if not opt_default:
            raise ValueError(f'No default found for argument: {i}')
        parser_add_opt.append(f'addOptional({parser_name}, {i!r}, {opt_default!r});')

    parser_add_opt = f'\n{ind}'.join(parser_add_opt)

    all_args_list = f'\n{ind}'.join([f'{i} = {parser_name}.Results.{i};'
                                     for i in all_specified_args])

    ensure_types = []
    for i in snippet_args:
        snip_arg_types = SNIPPETS_ARG_TYPES[i['name']].get('ensure_types')
        if not snip_arg_types:
            continue
        for snip_arg, val_type in snip_arg_types.items():
            ensure_snippet = f'ensure_{val_type}'
            ensure_types.append(f'{snip_arg} = {ensure_snippet}({snip_arg});')
            includes.append(f'{ensure_snippet}.m')
    ensure_types_fmt = f'\n{ind}'.join(ensure_types)
    includes = list(set(includes))

    func_invokes = []
    for i in snippet_sigs:
        ins_fmt = ', '.join(i['inputs'])
        func_invokes.append(f'{i["output"]} = {i["name"]}({ins_fmt});')
    func_invokes_fmt = f'\n{ind}'.join(func_invokes)

    wrapper_lns = [
        f'function exitcode = {script_name.rstrip(".m")}({wrap_inputs})',
        f'',
        f'{ind}{parser_name} = inputParser;',
        f'',
        f'{ind}{parser_add_req}',
        f'{ind}{parser_add_opt}',
        f'',
        f'{ind}parse({parser_name}, {parse_inputs})',
        f'',
        f'{ind}{all_args_list}',
        f'',
        f'{ind}{ensure_types_fmt}',
        f'',
        f'{ind}{func_invokes_fmt}',
        f'',
        f'{ind}exitcode = 1;',
        f'end',
    ]
    wrapper = '\n'.join(wrapper_lns)

    # Add includes:
    wrapper += '\n\n' + '\n'.join([get_snippet(i) for i in includes])

    return wrapper
