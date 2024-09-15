from setuptools import setup, find_packages

import importlib.util

spec = importlib.util.spec_from_file_location('pyrubberband.version', 'pyrubberband/version.py')
version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version)

setup(
    name='pyrubberband',
    version=version.version,
    description='Python module to wrap rubberband',
    author='Brian McFee',
    author_email='brian.mcfee@nyu.edu',
    url='http://github.com/bmcfee/pyrubberband',
    download_url='http://github.com/bmcfee/pyrubberband/releases',
    packages=find_packages(),
    long_description="""A python module to wrap rubberband.""",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='audio music sound',
    license='ISC',
    install_requires=[
        'numpy',
        'six',
        'soundfile>=0.12.1',
    ],
    extras_require={
        'docs': ['numpydoc'],
        'tests': [
            'pytest',
            'pytest-cov',
            'contextlib2',
        ]
    },
)
