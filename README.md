# ForNax
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage example
```bash
# SYNC stage
python fornax/main.py \
    --stage=sync \
    --source_path=https://github.com/lwencel-priv/fornax.git \
    --source_path_type=repository_address \
    --manifest_type=none \
    --branch=master \
    --repository_storage_path="./tmp/repositories" \
    --workspace="./tmp/logs"

# CHECKOUT stage
python fornax/main.py \
    --workspace="./tmp/logs" \
    --stage=checkout \
    --project=fornax \
    --branch=develop

# PREPARE_ENVIRONMENT stage
python fornax/main.py \
    --workspace="./tmp/logs" \
    --stage=prepare_environment
```

# License
ForNax is licensed under the MIT license.
