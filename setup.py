import os
import shutil
from setuptools import setup, find_packages
PACKAGES = find_packages()

# Add to pacakge upon installing
shutil.copyfile('course_settings.yml', os.path.join('niedu', 'data', 'course_settings.yml'))

# Get version and release info, which is all stored in shablona/version.py
ver_file = os.path.join('niedu', 'version.py')
with open(ver_file) as f:
    exec(f.read())

print(REQUIRES)
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
    install_requires=["neurodesign@git+https://github.com/Neuroimaging-UvA/neurodesign.git", REQUIRES],
    zip_safe=True
)


if __name__ == '__main__':
    setup(**opts)
