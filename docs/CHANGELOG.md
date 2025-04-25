## [1.1.1](https://github.com/yujiosaka/CronyxClient.py/compare/v1.1.0...v1.1.1) (2025-04-25)


### Bug Fixes

* use Python 3.11.12 instead of 3.11.13 for compatibility with GitHub Actions ([baf7578](https://github.com/yujiosaka/CronyxClient.py/commit/baf7578cf56e72505f0039a6d9e949d02123bf78))

# [1.1.0](https://github.com/yujiosaka/CronyxClient.py/compare/v1.0.0...v1.1.0) (2025-04-25)


### Bug Fixes

* add --system flag to uv pip install in CI workflow ([2f87967](https://github.com/yujiosaka/CronyxClient.py/commit/2f879676105ebb7405cb62962a611c8b64059050))
* add virtual environment creation for uv in CI workflow ([e8ad2cd](https://github.com/yujiosaka/CronyxClient.py/commit/e8ad2cde795383dc4be2b4c715a02314a23699eb))
* remove --locked flag from uv sync in CI workflow ([a619dd1](https://github.com/yujiosaka/CronyxClient.py/commit/a619dd182582f40e2612ae6e0b8a53515be31f1f))
* remove --locked flag from uv sync in setup script ([46cb5f0](https://github.com/yujiosaka/CronyxClient.py/commit/46cb5f06b4631c6aba9a60e3434efcffd5f34084))
* remove manual venv creation as uv sync creates it automatically ([95a0b95](https://github.com/yujiosaka/CronyxClient.py/commit/95a0b95dc25b04fbb64a8e80eea891fcccd3a8fc))
* update CI workflow to separate build and publish steps, use uv sync in setup script ([dc3c950](https://github.com/yujiosaka/CronyxClient.py/commit/dc3c9501d43e293b59cf19901a37ffe7ae5c522b))
* update CI workflow, Dockerfile, and setup script to follow uv best practices ([25f9c96](https://github.com/yujiosaka/CronyxClient.py/commit/25f9c96e7b181931eeb41c58a7318926b9f57456))
* update Dockerfile to use official uv image following Docker integration guide ([df285fd](https://github.com/yujiosaka/CronyxClient.py/commit/df285fd69393bce71f48c64e9b2076d76146f9ef))
* use uv sync instead of uv pip install in Dockerfile for consistency ([d962921](https://github.com/yujiosaka/CronyxClient.py/commit/d962921472b6adea8847a389c084dfc03af16182))


### Features

* add uv.lock and update Dockerfile to include it ([6a33455](https://github.com/yujiosaka/CronyxClient.py/commit/6a33455fa5a5928b4dc5825fa9ae3ec5768b6c96))
* migrate from poetry to uv ([59fbf81](https://github.com/yujiosaka/CronyxClient.py/commit/59fbf810fcc5d9be0b47a6494e7ede5ef5c84564))

# 1.0.0 (2023-11-05)


### Features

* release cronyx-client ([092c43e](https://github.com/yujiosaka/CronyxClient.py/commit/092c43e2ab862409862b3c3cd11756b3a1351da0))
