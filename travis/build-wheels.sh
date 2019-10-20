#!/bin/bash
set -e -x

# Install a system package required by our library
#yum install -y atlas-devel

git clone https://github.com/eigenteam/eigen-git-mirror eigen_git
mv eigen_git/Eigen io

make -C io/cppEDM/src clean
make -C io/cppEDM/src 

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    echo ${PYBIN}
    if [[ ${PYBIN} == *"cp27-cp27m"* ]]
    then
        continue  ### resumes iteration of an enclosing for loop ###
    fi
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done
