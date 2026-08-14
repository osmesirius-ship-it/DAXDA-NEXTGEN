"""Setup script for PyPI release of daxda-guard.
"""

from setuptools import setup, find_packages

setup(
    name="daxda-guard",
    version="1.0.0",
    description="Air-Gapped Synchronous AI Authority & Governance Audit SDK (Cl(7,0) Multivector Algebra)",
    author="DAXDA Systems Engineering Team",
    packages=find_packages(),
    package_data={"daxda_guard": ["../libdaxda_core.so"]},
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)
