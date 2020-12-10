# Change Log

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
