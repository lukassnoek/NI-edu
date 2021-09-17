import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


# This will enable the nbextensions utility
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        os.system('jupyter contrib nbextension install')
        os.system('jupyter nbextension enable toc2/main')

PACKAGES = find_packages()

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
    install_requires=["neurodesign@git+https://github.com/lukassnoek/neurodesign.git", REQUIRES],
    zip_safe=True,
    cmdclass={'install': PostInstallCommand},
    ignore_package_data={'': [".git"]}
)


if __name__ == '__main__':
    setup(**opts)
