#!/usr/bin/env bash

# print a trace of simple commands
set -x

# prepare for PyPI distribution
rm -rf build 2> /dev/null
mkdir eggs \
      sdist \
      wheels 2> /dev/null
mv -f dist/*.egg eggs/ 2> /dev/null
mv -f dist/*.whl wheels/ 2> /dev/null
mv -f dist/*.tar.gz sdist/ 2> /dev/null

# fetch platform spec
python3 setup.py sdist bdist_wheel
platform=$( python3 -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))" )
file=$( ls dist/*.tar.gz )
name=${file%*.tar.gz*}

# make distribution
python3.7 setup.py bdist_egg bdist_wheel
mv "${name}-py3-none-any.whl" "${name}-cp37-none-${platform}.whl"
python3.6 setup.py bdist_egg bdist_wheel
mv "${name}-py3-none-any.whl" "${name}-cp36-none-${platform}.whl"
pypy3 setup.py bdist_wheel
mv "${name}-py3-none-any.whl" "${name}-pp35-none-${platform}.whl"
python2.7 setup.py bdist_egg bdist_wheel
mv "${name}-py2-none-any.whl" "${name}-cp27-none-${platform}.whl"
pypy setup.py bdist_egg bdist_wheel
mv "${name}-py2-none-any.whl" "${name}-pp27-none-${platform}.whl"
python3.5 setup.py bdist_egg
python3.4 setup.py bdist_egg
python3 setup.py sdist

# distribute to PyPI and TestPyPI
twine upload dist/* -r pypi --skip-existing
twine upload dist/* -r pypitest --skip-existing

git pull
ret="$?"
if [[ $ret -ne "0" ]] ; then
    exit $ret
fi
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push
