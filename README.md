# vms
Vaccine management system

This system manages all stages of the vaccination process, from registration to recording doses.

## Environment setup instructions

__Note__ These instructions assume you have `python3` and `pip` installed on your development environment.

1. Create a virtual environment outside of the project directory
    - `python3 -m venv myvenv`

The above command will create a `myvenv` directory

2. Activate the virtual environment
    - For mac/linux: `source myvenv/bin/activate`
    - For windows: `myvenv/Scripts/activate.bat`

If the virutal environment has been successfully started, you should see your shell
prompt change to begin with: `(myvenv)`. You should always remember to activate this virtual environment when you're working on this project.

To deactivate the virtual environment, you can simply run `deactivate`. Your shell prompt should return to normal once virtual environment has been deactivated.

3. `cd` into the base directory of the project and run the following command to install all the dependencies.
    - `pip install -r requirements.txt`

4. Execute the `run.sh` script. This should start the django server, which by default listens on port 8000. You can then go to `http://localhost:8000/` to access your django application.

To use precommit hooks to enforce style and PEP8, run `pre-commit install` - you'll only need to do this once and your code will be automatically tidied after you attempt to `git commit`.
