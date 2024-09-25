ARG USER_NAME=user

FROM debian:12
ARG USER_NAME

# Install the necessary packages
RUN apt-get -y update
RUN apt-get install -yq --fix-missing  \
    build-essential  \
    emacs-nox  \
    vim  \
    git \
    screen \
    ca-certificates  \
    wget \
    curl  \
    screen \
    python3 \
    python3-pip

# Create a non-root user
RUN useradd -ms /bin/bash $USER_NAME

USER root

# Set up user folders
WORKDIR /home/$USER_NAME
RUN mkdir /home/$USER_NAME/outputs
RUN mkdir /home/$USER_NAME/muse
RUN mkdir -p /home/$USER_NAME/.muse/plugins

# Installing Ollama
ADD https://ollama.com/install.sh /home/$USER_NAME/install.sh
RUN chmod 755 /home/$USER_NAME/install.sh
RUN /home/$USER_NAME/install.sh
RUN rm /home/$USER_NAME/install.sh

# Install MuSE
ENV PIPX_HOME=/opt/pipx
ENV PIPX_BIN_DIR=/usr/local/bin
RUN apt-get install -y pipx
RUN pipx install hatch
COPY ./ /home/$USER_NAME/muse
WORKDIR /home/$USER_NAME/muse
RUN hatch build -t wheel
RUN python3 -m pip install /home/$USER_NAME/muse/dist/*.whl --break-system-packages
RUN rm -rf /home/$USER_NAME/muse/dist
WORKDIR /home/$USER_NAME

# Copy the init script
ADD initScript.bash /home/$USER_NAME/initScript.bash
RUN chmod 755 /home/$USER_NAME/initScript.bash

# Set the user and the working directory
#COPY docs /home/$USER_NAME/docs
WORKDIR /home/$USER_NAME
RUN chown -R user:user *

# Expose the port and set the environment variables
EXPOSE 8888
ENV MUSE_HOME=/home/$USER_NAME/muse
ENV MUSE_OUTPUT=/home/$USER_NAME/outputs
ENV MUSE_PLUGINS=/home/$USER_NAME/.muse/plugins

# Convert the file to Unix format (in case it was created/edited in Windows)
RUN sed -i -e 's/\r$//' /home/user/initScript.bash

# Set the entrypoint and the default command
ENTRYPOINT ["/home/user/initScript.bash"]
CMD ["echo","Default argument for CMD instruction"]
