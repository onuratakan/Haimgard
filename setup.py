from setuptools import setup
import pathlib

    
setup(name='haimgard',
version="0.9.0",
description="""Haimgard is an environment for writing, testing and using exploit code.""",
long_description="""
# Haimgard | [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/onuratakan/Haimgard)
Haimgard is an environment for writing, testing and using exploit code.

# Reminder
Important Information and Reminder Information and programs in all repositories are created for testing purposes. Any legal responsibility belongs to the person or organization that uses it.
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/Haimgard',
author='Onur Atakan ULUSOY - PwnWiki',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["haimgard"],
package_dir={'':'src'},
package_data={
    "haimgard": ["modules/*/*.py", "modules/*/*.txt"],
},
install_requires="""
commonmark==0.9.1
cowsay==4.0
loguru==0.5.3
rich==10.12.0
scapy==2.4.5
beautifulsoup4==4.10.0
bs4==0.0.1
soupsieve==2.3.1
python-nmap==0.7.1
pyreadline==2.1
scapy==2.4.5
mac-vendor-lookup==0.1.11
python_whois==0.7.3
""",
entry_points = {
    'console_scripts': ['haimgard=haimgard.haimgard:main'],
},
python_requires='>=3.6',
zip_safe=False)