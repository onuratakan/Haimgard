from setuptools import setup
import pathlib

    
setup(name='haimgard',
version="0.2.1",
description="""Haimgard is an environment for writing, testing and using exploit code.""",
long_description="""
# Haimgard-Framework
Haimgard is an environment for writing, testing and using exploit code.

# 🔑 License
MIT

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
    "haimgard": ["modules/*/*.py", "*.txt"],
},
install_requires="""
commonmark==0.9.1
cowsay==4.0
loguru==0.5.3
rich==10.12.0
scapy==2.4.5
""",
entry_points = {
    'console_scripts': ['haimgard=haimgard.haimgard:main'],
},
python_requires='>=3.6',
zip_safe=False)