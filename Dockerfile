FROM nianalysis

# Add docker user
RUN useradd -ms /bin/bash docker
USER docker
ENV HOME=/home/docker
WORKDIR $HOME

# Create symlink to credentials directory which should be mounted at runtime
RUN ln -s $HOME/credentials/netrc $HOME/.netrc

# Download QA script to run
RUN mkdir $HOME/scripts
RUN wget https://raw.githubusercontent.com/mbi-image/NiAnalysis/phantom_qc/scripts/analyse_qc.py $HOME/scripts

# Set up bashrc and vimrc
RUN sed 's/#force_color_prompt/force_color_prompt/' $HOME/.bashrc > $HOME/tmp; mv $HOME/tmp $HOME/.bashrc;
RUN echo "set background=dark" >> $HOME/.vimrc
RUN echo "syntax on" >> $HOME/.vimrc
RUN echo "set number" >> $HOME/.vimrc
RUN echo "set autoindent" >> $HOME/.vimrc