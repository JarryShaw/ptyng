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
rm -rf dist 2> /dev/null

# fetch platform spec
platform=$( python3 -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))" )

# make distribution
python3.7 setup.py sdist bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp37'
python3.6 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp36'
python3.5 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp35'
python3.4 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp34'
python2.7 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp27'
pypy3 setup.py bdist_wheel --plat-name="${platform}" --python-tag='pp35'
pypy setup.py bdist_wheel --plat-name="${platform}" --python-tag='pp27'

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
