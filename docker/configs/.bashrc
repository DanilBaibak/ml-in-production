# Colorful prompt string
PS1='\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ '

export LS_OPTIONS='--color=auto --group-directories-first'
alias ll='ls -lha $LS_OPTIONS'

export HISTFILE=${WORK_DIR}/.bash_history/history
touch $HISTFILE
