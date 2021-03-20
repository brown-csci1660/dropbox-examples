# Dropbox-Stencil

This is the stencil code for Dropbox. You will implement the functions defined in `client.py`. All the code you write should be in `client.py` . You should use the libraries provided in `support/`. The support code is imported in `client.py`. It will be helpful to review the function definitions and comments in the support code files. The crypto library you will use is defined in `support/crypto.py` and relies on the [cryptography](https://cryptography.io/en/latest/) package (**Note**: you **should not** use this package directly in any code you write. Instead, use the API provided by the support code). The servers for which you are implementing a client are defined in `support/dataserver.py` and `support/keyserver.py`. Finally, `support/util.py` contains several useful functions for working with bytes. There is example usage of all libraries at the end of each file. The example usage for the `util` library is included at the bottom of `client.py`, where it is shown in conjunction with the `dataserver` library. 



## Installation

To use this code you need the [cryptography](https://cryptography.io/en/latest/) package. There are many ways to install python packages. If you are confident that you can install this package, you are free to do so however you wish. Note, however, that we will only provide direct technical support for the strategy we recommend here.

> Note: This strategy applies to only your personal machine! If you are working on a department machine, please see the `Department Machines` section

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

#### Testing the Installation

Inside the repo with your virtual environment active: 

1. Run `python client.py`

	- It should produce no output. If it exits cleanly, you are good to go.

2. Run `python -m support.crypto`

	- It should produce no output. If it exits cleanly, you are good to go.

3. Run `python -m support.dataserver`

	- It should produce the following output:

		```
		random memloc: b'<RANDOM STRING OF BYTES GOES HERE>'
		Specific memloc in hex: b'0000000000000000'
		-------------------
		error testing:
		ERROR: Memloc must be 16 bytes
		exception raised correctly!
		
		ERROR: Datasever can only store raw bytes! You gave val of type <class 'str'>. Please serialize to bytes.
		exception raised correctly!
		```

4. Run `python -m support.keyserver`

	- It should produce the following output:

		```
		Expecting two error messages...
		ERROR: Keyserver tags must be strings, not <class 'int'>
		ERROR: Keyserver keys must of type asmPublicKey, not <class 'int'>
		Success!
		```

		

## Department Machines

A properly configured virtual enviroment is available for use on the department machines. To use the virtual enviroment, run `source cs166_dropbox_env`. 

