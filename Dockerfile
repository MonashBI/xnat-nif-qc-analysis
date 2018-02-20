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
RUN git clone https://github.com/mbi-image/xnat-nif-qc-analysis.git $HOME/repo
ENV PYTHONPATH $HOME/repo:$PYTHONPATH
WORKDIR $HOME/repo
ENV SERVER 'https://mbi-xnat.erc.monash.edu.au'
ENV T132CH 't1_mprage_trans_p2_iso_0.9_32CH'
ENV T232CH 't2_spc_tra_iso_32CH'
ENV DMRI32CH 'ep2d_diff_mddw_12_p2_32CH'
ENV INSTRUMENTS 'AWP45193'
ENV VISITS '20170724'
RUN python scripts/analyse_qc.py $SERVER \
    -p t1_32ch_saline $T132CH \
    -p t2_32ch_saline $T232CH \
    -p dmri_32ch_saline $DMRI32CH \
    -w $WORK_DIR \
    -i $INSTRUMENTS \
    -v $VISITS
