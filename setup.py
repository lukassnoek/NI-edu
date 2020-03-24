import os
import shutil
from setuptools import setup, find_packages
PACKAGES = find_packages()

shutil.copyfile('course_settings.yml', os.path.join('niedu', 'data', 'course_settings.yml'))

# Get version and release info, which is all stored in shablona/version.py
ver_file = os.path.join('niedu', 'version.py')
with open(ver_file) as f:
    exec(f.read())

opts = dict(
    name=NAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    platforms=PLATFORMS,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=["neurodesign@git+https://github.com/Neuroimaging-UvA/neurodesign.git"],
    requires=REQUIRES,
    zip_safe=True,
    entry_points = {
        'console_scripts': [
            'niedu_download_data=niedu.cmd_interfaces:niedu_download_data',
            'niedu_enable_nbgrader=niedu.cmd_interfaces:niedu_enable_nbgrader',
            'niedu_create_users=niedu.cmd_interfaces:niedu_create_users',
            'niedu_delete_users=niedu.cmd_interfaces:niedu_delete_users',
            'niedu_create_single_user=niedu.cmd_interfaces:niedu_create_single_user',
            'niedu_add_fsl_path_to_bashrc=niedu.cmd_interfaces:niedu_add_fsl_path_to_bashrc'
        ]
    }
)


if __name__ == '__main__':
    setup(**opts)
