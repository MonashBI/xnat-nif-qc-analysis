FROM nianalysis

# Add docker user
RUN useradd -ms /bin/bash docker
USER docker
ENV HOME=/home/docker
ENV WORK_DIR $HOME/work-dir 

RUN mkdir -p $WORK_DIR 

# Create symlink to credentials directory which should be mounted at runtime
RUN ln -s $HOME/credentials/netrc $HOME/.netrc

# Set up bashrc and vimrc for debugging
RUN sed 's/#force_color_prompt/force_color_prompt/' $HOME/.bashrc > $HOME/tmp; mv $HOME/tmp $HOME/.bashrc;
RUN echo "set background=dark" >> $HOME/.vimrc
RUN echo "syntax on" >> $HOME/.vimrc
RUN echo "set number" >> $HOME/.vimrc
RUN echo "set autoindent" >> $HOME/.vimrc

# Download QA script to run
RUN echo "BUILD 2"
RUN git clone https://github.com/mbi-image/xnat-nif-qc-analysis.git $HOME/repo
ENV PYTHONPATH $HOME/repo:$PYTHONPATH
WORKDIR $HOME

# Echo the analysis script to run
# python $HOME/repo/scripts/analyse_qc.py https://mbi-xnat.erc.monash.edu.au \
#     -p t1_32ch t1_mprage_trans_p2_iso_0.9_32CH -p t2_32ch t2_spc_tra_iso_32CH -p dmri_32ch ep2d_diff_mddw_12_p2_32CH \
#     -w $WORK_DIR -i AWP45193 -d 20170724"
