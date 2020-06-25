# Timestamp: 2020/06/25 17:39:46 UTC
# 
# Thank you for using Neurodocker. If you discover any issues
# or ways to improve this software, please submit an issue or
# pull request on our GitHub repository:
# 
#     https://github.com/ReproNim/neurodocker

FROM neurodebian:stretch-non-free

USER root

ARG DEBIAN_FRONTEND="noninteractive"

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    ND_ENTRYPOINT="/neurodocker/startup.sh"
RUN export ND_ENTRYPOINT="/neurodocker/startup.sh" \
    && apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           apt-utils \
           bzip2 \
           ca-certificates \
           curl \
           locales \
           unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG="en_US.UTF-8" \
    && chmod 777 /opt && chmod a+s /opt \
    && mkdir -p /neurodocker \
    && if [ ! -f "$ND_ENTRYPOINT" ]; then \
         echo '#!/usr/bin/env bash' >> "$ND_ENTRYPOINT" \
    &&   echo 'set -e' >> "$ND_ENTRYPOINT" \
    &&   echo 'export USER="${USER:=`whoami`}"' >> "$ND_ENTRYPOINT" \
    &&   echo 'if [ -n "$1" ]; then "$@"; else /usr/bin/env bash; fi' >> "$ND_ENTRYPOINT"; \
    fi \
    && chmod -R 777 /neurodocker && chmod a+s /neurodocker

ENTRYPOINT ["/neurodocker/startup.sh"]

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           vim \
           git \
           firefox-esr \
           openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-key adv --recv-keys --keyserver keys.gnupg.net E1F958385BFE2B6E

RUN echo "deb http://packages.x2go.org/debian stretch extras main" >> /etc/apt/sources.list.d/x2go.list

RUN apt-get update -qq && apt-get install x2go-keyring && apt-get update && apt-get install -y x2gomatebindings x2goserver x2goserver-xsession

RUN sed -i "s/#PasswordAuthentication/PasswordAuthentication/g" /etc/ssh/sshd_config

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

RUN mkdir /var/run/sshd

RUN echo 'root:ubuntu' | chpasswd

RUN sed -i '$i/usr/sbin/sshd -D &' $ND_ENTRYPOINT

ENV CONDA_DIR="/opt/miniconda-latest" \
    PATH="/opt/miniconda-latest/bin:$PATH"
RUN export PATH="/opt/miniconda-latest/bin:$PATH" \
    && echo "Downloading Miniconda installer ..." \
    && conda_installer="/tmp/miniconda.sh" \
    && curl -fsSL --retry 5 -o "$conda_installer" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash "$conda_installer" -b -p /opt/miniconda-latest \
    && rm -f "$conda_installer" \
    && conda update -yq -nbase conda \
    && conda config --system --prepend channels conda-forge \
    && conda config --system --set auto_update_conda false \
    && conda config --system --set show_channel_urls true \
    && sync && conda clean -y --all && sync \
    && conda create -y -q --name neuro_py37 \
    && conda install -y -q --name neuro_py37 \
           "python=3.7" \
           "jupyter" \
           "nbgrader" \
           "jupyter_contrib_nbextensions" \
           "matplotlib" \
           "scikit-learn" \
           "seaborn" \
    && sync && conda clean -y --all && sync \
    && bash -c "source activate neuro_py37 \
    &&   pip install --no-cache-dir  \
             "nilearn" \
             "nibabel"" \
    && rm -rf ~/.cache/pip/* \
    && sync \
    && sed -i '$isource activate neuro_py37' $ND_ENTRYPOINT

RUN curl -L https://github.com/krallin/tini/releases/download/v0.6.0/tini > /usr/bin/tini && chmod +x /usr/bin/tini

RUN sed -i '$i/usr/bin/tini -s -- jupyter notebook --ip=0.0.0.0 --port 9999 --allow-root &' $ND_ENTRYPOINT

RUN test  || useradd --no-user-group --create-home --shell /bin/bash -p $(openssl passwd -1 ubuntu)  neuro

WORKDIR /home/neuro

COPY [".", "/home/neuro/"]

RUN mv course_settings_container.yml course_settings.yml

RUN mkdir -p /home/neuro/.jupyter && echo c.NotebookApp.ip = \"0.0.0.0\" > /home/neuro/.jupyter/jupyter_notebook_config.py

RUN bash -c 'source activate neuro_py37 && pip install . && jupyter nbextension install --sys-prefix --py nbgrader --overwrite && jupyter nbextension enable --sys-prefix --py nbgrader && jupyter serverextension enable --sys-prefix --py nbgrader'

EXPOSE 9999

EXPOSE 22

RUN echo '{ \
    \n  "pkg_manager": "apt", \
    \n  "instructions": [ \
    \n    [ \
    \n      "base", \
    \n      "neurodebian:stretch-non-free" \
    \n    ], \
    \n    [ \
    \n      "install", \
    \n      [ \
    \n        "vim", \
    \n        "git", \
    \n        "firefox-esr", \
    \n        "openssh-server" \
    \n      ] \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "apt-key adv --recv-keys --keyserver keys.gnupg.net E1F958385BFE2B6E" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "echo \"deb http://packages.x2go.org/debian stretch extras main\" >> /etc/apt/sources.list.d/x2go.list" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "apt-get update -qq && apt-get install x2go-keyring && apt-get update && apt-get install -y x2gomatebindings x2goserver x2goserver-xsession" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "sed -i \"s/#PasswordAuthentication/PasswordAuthentication/g\" /etc/ssh/sshd_config" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "sed -i '"'"'s/#PermitRootLogin prohibit-password/PermitRootLogin yes/g'"'"' /etc/ssh/sshd_config" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "mkdir /var/run/sshd" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "echo '"'"'root:ubuntu'"'"' | chpasswd" \
    \n    ], \
    \n    [ \
    \n      "add_to_entrypoint", \
    \n      "/usr/sbin/sshd -D &" \
    \n    ], \
    \n    [ \
    \n      "miniconda", \
    \n      { \
    \n        "conda_install": [ \
    \n          "python=3.7", \
    \n          "jupyter", \
    \n          "nbgrader", \
    \n          "jupyter_contrib_nbextensions", \
    \n          "matplotlib", \
    \n          "scikit-learn", \
    \n          "seaborn" \
    \n        ], \
    \n        "pip_install": [ \
    \n          "nilearn", \
    \n          "nibabel" \
    \n        ], \
    \n        "create_env": "neuro_py37", \
    \n        "activate": true \
    \n      } \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "curl -L https://github.com/krallin/tini/releases/download/v0.6.0/tini > /usr/bin/tini && chmod +x /usr/bin/tini" \
    \n    ], \
    \n    [ \
    \n      "add_to_entrypoint", \
    \n      "/usr/bin/tini -s -- jupyter notebook --ip=0.0.0.0 --port 9999 --allow-root &" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "test  || useradd --no-user-group --create-home --shell /bin/bash -p \"$1$0/bGc/rG$rj320wFrxFYQrG0jXFU25.\" neuro" \
    \n    ], \
    \n    [ \
    \n      "workdir", \
    \n      "/home/neuro" \
    \n    ], \
    \n    [ \
    \n      "copy", \
    \n      [ \
    \n        ".", \
    \n        "/home/neuro/" \
    \n      ] \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "mv course_settings_container.yml course_settings.yml" \
    \n    ], \
    \n    [ \
    \n      "run", \
    \n      "mkdir -p /home/neuro/.jupyter && echo c.NotebookApp.ip = \\\"0.0.0.0\\\" > /home/neuro/.jupyter/jupyter_notebook_config.py" \
    \n    ], \
    \n    [ \
    \n      "run_bash", \
    \n      "source activate neuro_py37 && pip install . && jupyter nbextension install --sys-prefix --py nbgrader --overwrite && jupyter nbextension enable --sys-prefix --py nbgrader && jupyter serverextension enable --sys-prefix --py nbgrader" \
    \n    ], \
    \n    [ \
    \n      "expose", \
    \n      [ \
    \n        "9999" \
    \n      ] \
    \n    ], \
    \n    [ \
    \n      "expose", \
    \n      { \
    \n        "2": "2" \
    \n      } \
    \n    ] \
    \n  ] \
    \n}' > /neurodocker/neurodocker_specs.json
