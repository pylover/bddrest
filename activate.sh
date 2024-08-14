# Usage:
# source activate.sh
# source path/to/activate.sh
# . activate.sh
VENV=$(basename `dirname "$(readlink -f "$BASH_SOURCE")"`)
VENVPATH=${HOME}/.virtualenvs/${VENV}
source ${VENVPATH}/bin/activate
