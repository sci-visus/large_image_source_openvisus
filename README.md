# Instructions

Add OpenVisus as a backend for large image

Links:
- https://github.com/girder/large_image

Instructions for windows

```bash

# create a virtual environment with all development packages
c:\python310\python.exe -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install pooch wheel twine large-image[common] girder-large-image 
python -m pip install --upgrade OpenVisusNoGui
```

Test it:
- it's **broken** right now
  - there is some *confusion* between LargeImage plugin and Girder large image plugin
  - should it be fixed? 

```bash

# enable dev mode
python -m pip install -e .

python test.py D:/visus-datasets/david_subsampled/visus.idx ~test.png
```

Change `setup.py` to contain the project version and upload the wheel:

```bash
rm -f dist/*
python3 setup.py bdist_wheel
twine upload dist/*.whl
```

Then goto [nsdf-services/histomicsui](https://github.com/nsdf-fabric/nsdf-services/blob/main/histomicsui/ReadMe.md) and follow instructions