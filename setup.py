import io
from os import path
from setuptools import setup, find_packages

pwd = path.abspath(path.dirname(__file__))
with io.open(path.join(pwd, 'README.md'), encoding='utf-8') as readme:
    desc = readme.read()

setup(
    name='subgpt',
    version=__import__('subgpt').__version__,
    description='Find subdomains with GPT, for free',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='s0md3v',
    license='GNU Affero General Public License v3.0',
    url='https://github.com/s0md3v/SubGPT',
    download_url='https://github.com/s0md3v/SubGPT/archive/v%s.zip' % __import__(
        'subgpt').__version__,
    packages=find_packages(),
    install_requires=['dnspython', 'EdgeGPT', 'tldextract'],
    classifiers=[
        'Topic :: Security',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'subgpt = subgpt.subgpt:main'
        ]
    },
    keywords=['recon', 'subdomain', 'pentesting', 'gpt', 'hacking']
)
