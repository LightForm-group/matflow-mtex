# Change Log

## [0.1.9] - 2021.xx.xx

### Added

- Add task `sample_orientations` with methods `from_CTF_file` and `from_CRC_file`. This is for randomly sampling `N` orientations directly from the EBSD data. Similar to the `sample_texture` task, but an ODF is not constructed.
## [0.1.8] - 2021.09.24

### Changed

- Validate orientations in `visualise_orientations/pole_figure`.
- Respect `quat_component_ordering` in `plot_pole_figure`

## [0.1.7] - 2021.03.21

### Changed

- Add option to rotate EBSD data in snippets `get_ODF_from_CRC_file` and `get_ODF_from_CTF_file`.

## [0.1.6] - 2021.01.19

### Added

- Support "fibre" ODF components in snippet `get_model_ODF.m`
- Add input mapper for task `visualise_volume_element_response` with method `texture_pole_figure`.

### Changed

- Account for `euler_degree` boolean specification in orientations JSON file.
- Scale vector part of quaternions in `plot_pole_figure` snippet by -1 if P-constant is +1.
- Change visualise orientations snippet to plot contours

## [0.1.5] - 2021.01.10

### Added

- Add new tasks for generating orientations that bypass exporting/importing ODFs due to issues with how [MTEX currently handles this](https://github.com/mtex-toolbox/mtex/issues/659). These tasks are: `sample_texture` with methods: `from_model_ODF`, `from_CTF_file` and `from_CRC_file`. Previously, this would have been achieved with two tasks `get_model_texture`/`estimate_ODF` and then `sample_texture`.
- Add ability to generate an ODF in `sample_texture/from_model_ODF` task using multiple ODF components.
- Add `visualise_orientations/pole_figure` task to plot sampled orientations on a pole figure in MTEX.

## [0.1.4] - 2020.12.10

### Fixed

- Fix output mapper functions `parse_orientations` and `parse_MTEX_ODF_file` for cases where the files have only one row of data. Now we use the `ndmin=2` argument of `numpy.loadtxt` to ensure arrays of consistent dimensions are returned.

## [0.1.3] - 2020.08.18

### Added

- Support specifying orientation coordinate system, which can be used to correctly align, within the model, the textures with respect to e.g. RD/TD/ND.

## [0.1.2] - 2020.07.18

### Added

- Support generating an ODF from CRC (and CPR) EBSD files (in addition to existing CTF file support).

## [0.1.1] - 2020.07.01

### Added

- Add `fibre` method to `get_model_texture` task.
- Add `random` method to `get_model_texture` task.

### Changed

- Use `orientation.byMiller` in `get_unimodal_ODF.m`

## [0.1.0] - 2020.06.09

- Initial release.
