from setuptools import setup, find_packages

import imp

version = imp.load_source('pyrubberband.version', 'pyrubberband/version.py')

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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords='audio music sound',
    license='ISC',
    install_requires=[
        'librosa>=0.4',
        'six',
    ],
    extras_require={
        'docs': ['numpydoc']
    }
)
