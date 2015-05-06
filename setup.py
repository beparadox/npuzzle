from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='npuzzle',
        version='0.1',
        description='Improving heuristics for sliding block puzzles',
        long_description=readme(),
        classifiers=[
            'Sliding block puzzle',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Heuristics, Machine Learning'
            ],
        keywords='npuzzle sliding block puzzle heuritistics',
        url='https://github.com/beparadox/npuzzle',
        author='Bambridge E. Peterson',
        author_email='bambridge.peterson@gmail.com',
        license='MIT',
        packages=['npuzzle'],
        install_requires=[
        'numpy',
        'matplotlib',
        'pymongo'],
        test_suite='nose.collector',
        tests_require=['nose'],
        include_package_data=True,
        zip_safe=False)
