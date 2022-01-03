# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## [0.0.2] - 2021-12-13

### Added

* `doc/guide.md` more docs for quick start

### Changed

* Update doc
* Works without jammy, [commit](https://github.com/qsh-zh/jam-lht/commit/a2ef2824a2419c88d15af582d9113f438d4a154a)
* `setme` keywords, [commit](0b3212155d26aadf9bbd42c294309ef273db6e7c)
* merge 1.2 from ashleve, [commit](https://github.com/qsh-zh/jam-lht/commit/ee4294fe1dc2a7ef1c98ecef4982684de3cd1209)

### Deprecated

### Removed

* Remove jammy to deps, [commit](https://github.com/qsh-zh/jam-lht/commit/a2ef2824a2419c88d15af582d9113f438d4a154a)

### Fixed

* wandb number of parameters, [commit](https://github.com/qsh-zh/jam-lht/commit/fa29b658a91dc478692f3532d9f8b87ea3c119e8)

## [0.0.1] - 2021-11-17

### Added

* CHANGELOG.log
* `doc/guide.md` for development
* poetry management [pr](https://github.com/qshzh/lightning-hydra-template/pull/1)
* jam wandb log [pr](https://github.com/qshzh/lightning-hydra-template/pull/1)
* demo for multi-run with joblib [commit](https://github.com/qsh-zh/jam-lht/commit/870c040ff61fe9a184d7687c9e1d1bfa1c47775e)
* load env settings [commit](https://github.com/qsh-zh/jam-lht/commit/e3c1114464539124963dbee5c78e09184826ed0a)
* Upgrade jammy 0.0.4
* jammy jyd_link [commit](https://github.com/qsh-zh/jam-lht/commit/30565e042fc6cbb082f860a317823a7ab48677fb)
* auto-fgpu [commit](https://github.com/qsh-zh/jam-lht/commit/5ab06fbb221edd533c13d8e373911bfecc69b4ea)
* `# TODO: setme` for quick setup

### Changed

* Update doc
* Reseed random rng after instantiation
* Reduce training epoch
* Sesolve config after starting, [commit](https://github.com/qsh-zh/jam-lht/commit/64ae765eaa7c9630858878e63b2c1476ea0d3a11)

### Deprecated

### Removed

### Fixed
