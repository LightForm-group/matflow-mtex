# Change Log

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
