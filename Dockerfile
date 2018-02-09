FROM nianalysis

# Add docker user
RUN useradd -ms /bin/bash docker
USER docker
ENV HOME=/home/docker

# Create symlink to credentials directory which should be mounted at runtime
RUN ln -s $HOME/credentials/netrc $HOME/.netrc

# Set up bashrc and vimrc for debugging
RUN sed 's/#force_color_prompt/force_color_prompt/' $HOME/.bashrc > $HOME/tmp; mv $HOME/tmp $HOME/.bashrc;
RUN echo "set background=dark" >> $HOME/.vimrc
RUN echo "syntax on" >> $HOME/.vimrc
RUN echo "set number" >> $HOME/.vimrc
RUN echo "set autoindent" >> $HOME/.vimrc

# Download QA script to run
RUN git clone https://github.com/mbi-image/xnat-nif-qc-analysis.git $HOME/repo
WORKDIR $HOME/repo
RUN python scripts/analyse_qc.py
