#!/usr/bin/env bash

if [[ ! "${BASH_SOURCE[0]}" != "${0}" ]]; then 
    echo "*** ERROR: this script must be sourced ..."
    exit -1
fi

SCRIPT=$(readlink -f "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(dirname "$SCRIPT")
BASEDIR=$(realpath "${SCRIPT_DIR}/..")

NEW_PYTHONPATH="${BASEDIR}/src:${BASEDIR}/src/generated"
if [[ ! -z ${PYTHONPATH} ]]; then
    NEW_PYTHONPATH="${PYTHONPATH}:${NEW_PYTHONPATH}"
fi
export PYTHONPATH=${NEW_PYTHONPATH}

export PYTHONDONTWRITEBYTECODE="YES"
export DREPIN_DEBUG="YES"
