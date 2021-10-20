from setuptools import setup
import pathlib


version_path = pathlib.Path.cwd() / "src" / "haimgard" / "VERSION.txt"
with open(version_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    version = lines[0]

requirements_path = pathlib.Path.cwd() / "requirements.txt"
with open(requirements_path, 'r', encoding='utf-8') as f:
    requirements = []
    for requirement_line in f.readlines():
        requirements.append(requirement_line.strip("\n"))

    
setup(name='haimgard',
version=version,
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
install_requires=requirements,
entry_points = {
    'console_scripts': ['haimgard=haimgard.haimgard:main'],
},
python_requires='>=3.6',
zip_safe=False)