# Dropbox-Stencil

This is the stencil code for Dropbox. You will implement the functions defined in `stencil.py`. All the code you write should be in `stencil.py` . You should use the libraries provided in `support/`. The support code is imported in `stencil.py`. It will be helpful to review the function definitions and comments in the support code files. The crypto library you will use is defined in `support/crypto.py` and relies on the [cryptography](https://cryptography.io/en/latest/) package. The servers for which you are implementing a client are defined in `support/dataserver.py` and `support/keyserver.py`. Finally, `support/util.py` contains several useful functions for working with bytes. There is example usage of all libraries at the end of each file. The example usage for the `util` library is included at the bottom of `stencil.py`, where it is shown in conjunction with the `dataserver` library. 



## Installation

To use this code you need the [cryptography](https://cryptography.io/en/latest/) package. There are many ways to install python packages. If you are confident that you can install this package, you are free to do so however you wish. Note, however, that we will only provide direct technical support for the strategy we recommend here.

### Installation with `pip` virtual environments

> This is the recommended installation strategy

#### Virtual Environment

1. Ensure you are using `python3.7` or above by running `python3 --version`
2. Clone this repo 
3. Navigate to the local copy of the repo that you just cloned
4. Inside that directory, run `python3 -m venv .env`
	- Note that we have added `.env/` to the `.gitignore` so that it will not be pushed to GitHub 
5. `.env` now contains your virtual environment. In order to activate it, run `source .env/bin/activate`
6. To confirm that the virtual environment has been activated, run `which python`. The resulting path should end `.env/bin/python`
7. Once you are done working on the project, you can run `deactivate` to leave the virtual environment. When you return to the project, you should run `source .env/bin/activate` again. 

#### Installing the library

1. Make sure your virtual environment is active
2. Make sure pip is up to date by running `pip install --upgrade pip`
3. Inside the root directory of your repo, run `python3 -m pip install -r requirements.txt`
4. 

You should install it using pip with `python3 -m pip install -r requirements.txt`. 

You should also use `python3`.

To run the stencil, run `python3 stencil.py`. This will not do anything but should not throw errors.

To test the crypto library, run `python3 -m support.crypto` which also should not throw errors. 
