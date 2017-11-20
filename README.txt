testrunner
==========

LIVE DEMO
---------

http://165.227.165.48:6543


Getting Started
---------------

- Change directory into your newly created project.

    cd testrunner

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode.

    env/bin/pip install -e .

- Configure the database.

    env/bin/initialize_testrunner_db development.ini

- Run task queue.

    env/bin/huey_consumer.py testrunner.consumer.huey &

- Run your project.

    env/bin/gunicorn -k eventlet --paste development.ini


Debian Wheezy Notes
===================

There is an ancient version of pip in Wheezy. But recent pip is
not compatible with Wheezy's Python 3.2. So we have to install
more recent Python. Application is tested under Wheezy
with Python 3.5.2 installed through pyenv (https://github.com/pyenv/pyenv).

- Isnstall required system packages.

    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev

- Check out pyenv where you want it installed.
  A good place to choose is $HOME/.pyenv (but you can install
  it somewhere else).

    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

- Define environment variable PYENV_ROOT to point to the path where
  pyenv repo is cloned and add $PYENV_ROOT/bin to your $PATH for
  access to the pyenv command-line utility.

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

- Add pyenv init to your shell to enable shims and autocompletion.

    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc

- Restart your shell so the path changes take effect.

    exec bash

- Install Python versions into $(pyenv root)/versions

    pyenv install 3.5.2

- Set the global Python version.

    pyenv global 3.5.2
