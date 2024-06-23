
# OpenVisus for Large Image

For Windows:

```bash
set PATH=%PATH%;c:\python310
python.exe -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip

python -m pip install pooch wheel twine large-image[common] girder-large-image OpenVisusNoGui

cd sources\openvisus

# this is the develop mode, if you need to debug (i.e. it will store in site packages links to the current source files)
python -m pip install -e .

python test.py

# create and upload wheel
# CHANGE the setup.py to contain the right version
del dist\*.whl
python setup.py bdist_wheel
twine upload dist/*.whl
rm -Rf ./build ./dist ./*egg-info
# python -m pip install --no-cache-dir --force-reinstall large-image-source-openvisus


```

