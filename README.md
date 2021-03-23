# dropbox

This is the stencil code for Dropbox. You will implement the functions defined in `client.py`. Some notes:

- All the code you write should be in `client.py`; our provided APIs are already imported in `client.py` for you. 
- While you are not permitted to edit the support code files, you may find it helpful to review the comments in the support code files. The crypto library you will use is defined in `support/crypto.py`. The servers for which you are implementing a client are defined in `support/dataserver.py` and `support/keyserver.py`. Finally, `support/util.py` contains several useful functions for working with bytes. There is example usage of all libraries at the end of each support code file. 

## Installation

To install the support code, you will need to install some dependencies; in particular, you will need the Python [cryptography](https://cryptography.io/en/latest/) package. (**Note**: You **should not** use this package directly in any code you write. Instead, use the API provided by the support code documented in the Dropbox Wiki.) There are many ways to install Python packages. If you are confident that you can install this package, you are free to do so however you wish. However, the TAs will only provide direct technical support for the strategy we recommend here.

> *Note:* This strategy applies to only your personal machine! If you are working on a department machine, please see the `Department Machines` section below.

### Recommended Installation: `pip` virtual environments

Follow the instructions in the section below to set up your local environment for working on the project.

#### Virtual Environment

First, create a virtual environment using the following strategy:

1. Ensure you are using `python3.7` or above by running `python3 --version`
2. Clone this repo 
3. Navigate to the local copy of the repo that you just cloned
4. Inside that directory, run `python3 -m venv .env`
	- Note that we have added `.env/` to the `.gitignore` so that it will not be pushed to GitHub 
5. `.env` now contains your virtual environment. In order to activate it, run `source .env/bin/activate`
6. To confirm that the virtual environment has been activated, run `which python`. The resulting path should end `.env/bin/python`
7. Once you are done working on the project, you can run `deactivate` to leave the virtual environment. When you return to the project, you should run `source .env/bin/activate` again. 

#### Installing Necessary Dependencies

Then, while inside of the virtual environment, install the necessary dependencies:

1. Make sure your virtual environment is active
2. Make sure pip is up to date by running `pip install --upgrade pip`
3. Inside the root directory of your repo, run `pip install -r requirements.txt`

#### Testing the Installation

You can then test your local environment setup with the following comamnds. First, make sure your current working directory is the directory containing your Dropbox repo; also, make sure your virtual environment is activated. Then:

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
		ERROR: Keyserver keys must of type AsmPublicKey, not <class 'int'>
		Success!
		```



## Testing

You should write tests in `test_client.py`. There are a few example tests in `test_client.py` as well as a stencil for your tests. To run the tests you can run 

```
python -m unittest
```

(This is how we will run our tests against your implementation.)

The tests will be run in alphabetical order. If you run the tests on the stencil code (with no changes), it will run six tests, five of which should fail. 

## Department Machines

If you are unable to (or don't want to) install the dependencies locally, a properly configured virtual enviroment is available for use on the department machines. To use the virtual enviroment, run `source cs166_dropbox_env`. 
