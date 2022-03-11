# How to contribute to flaskcwg.github.io

## Setup Instructions

* [Fork](https://github.com/flaskcwg/flaskcwg.github.io/fork) the repo
* Clone your forked repo

    ```bash
    git https://github.com/{username}/flaskcwg.github.io.git
    cd flaskcwg.github.io
    ```

* Setup the upstream to original repo

    ```bash
    git remote add upstream https://github.com/flaskcwg/flaskcwg.github.io.git
    ```

* Create a virtual env and activate it

    For Linux/Mac:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

    For Windows:

    ```bash
    py -m venv env
    source env\Scripts\activate
    ```

* install dependencies

    ```bash
    pip install -r requirements.txt
    ```

* run `static.py`. This will build html content in `docs/`

    ```bash
    python static.py
    ```

* run `serve.py`. Go to the IP address shown in the printout to view the generated site

    ```bash
    cd docs
    python serve.py
    ```

* Add your fork as a remote to push your work to. Replace {username} with your username. This names the remote "fork", the default Pallets remote is "origin".
