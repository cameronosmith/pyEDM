#!/bin/bash
set -e -x

# Collect the pythons
pys=(/opt/python/*/bin)

# Filter out Python 3.4
pys=(${pys[@]//*27*/})

make -C /io/cppEDM/src

PYBIN="/opt/python/cp37-cp37m/bin"

# Compile wheels
#for PYBIN in "${pys[@]}"; do
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
    "${PYBIN}/python" /io/setup.py bdist_wheel --dist-dir wheelhouse/
    
#done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/pyEDM-*.whl; do
    auditwheel repair --plat $PLAT "$whl" -w /io/wheelhouse/
done

# Install packages and test
#for PYBIN in "${pys[@]}"; do
    "${PYBIN}/python" -m pip install pyEDM --no-index -f /io/wheelhouse
    "${PYBIN}/pytest" /io/tests
#done
