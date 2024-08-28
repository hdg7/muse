FROM debian:12

RUN apt-get -y update
RUN apt-get install -yq --fix-missing build-essential emacs-nox vim-tiny git inkscape jed libsm6 libxext-dev libxrender1 lmodern netcat-openbsd python3-dev tzdata unzip nano emacs ca-certificates wget gcc-12 gcc-12-plugin-dev curl screen  nginx clang llvm lld gdb python3 python3-pip

RUN useradd -ms /bin/bash user 

USER user
WORKDIR /home/user

#Installing the jupyter interface
USER root
RUN pip3 install --upgrade pip --break-system-packages

#Installing Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN pip3 install ipyflex plotly

WORKDIR /home/user/
RUN mkdir /home/user/outputs
COPY muse /home/user/muse
RUN mkdir /root/models

#Installing the python mlighter-utils
RUN muse/install.bash

ADD initScript.bash /home/user/initScript.bash 
WORKDIR /home/user/muse
EXPOSE 8888
ENV MUSE_HOME=/home/user/muse
ENV MUSE_OUTPUT=/home/user/outputs
RUN chmod 755 /home/user/initScript.bash
RUN chown -R user:user *
#For Windows users
RUN sed -i -e 's/\r$//' /home/user/initScript.bash
ENTRYPOINT ["/home/user/initScript.bash"]
CMD ["echo","Default argument for CMD instruction"]
#USER root

