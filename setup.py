import os

from setuptools import find_packages, setup

description = 'OpenVisus tilesource for large_image.'
long_description = description + '\n\nSee the large-image package for more details.'

project_version="1.0.2"

setup(
    name='large-image-source-openvisus',
    version = project_version,
    description=description,
    long_description=long_description,
    license='Apache Software License 2.0',
    author='OpenVisus',
    author_email='scrgiorgio@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
      'large-image',
      'OpenVisusNoGui',
    ],
    extras_require={
        'girder': f'girder-large-image',
        'all': ['large-image-converter',],
    },
    keywords='large_image, tile source',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/large_image',
    python_requires='>=3.9',
    entry_points={
        'large_image.source': [
            'openvisus = large_image_source_openvisus:OpenVisusTileSource',
        ],
        'girder_large_image.source': [
            'openvisus = large_image_source_openvisus.girder_source:OpenVisusGirderTileSource',
        ],
    },
)