from setuptools import setup, find_packages

setup(
    name="weekly",
    use_scm_version=True,
    setup_requires=[
        'setuptools_scm'
    ],
    description='A basic microblog for weekly reports',
    license='BSD',
    package=find_packages(),
    entry_points={
        'console_scripts': [
            'weekly=weekly.weekly:main'
        ],
    },
)
