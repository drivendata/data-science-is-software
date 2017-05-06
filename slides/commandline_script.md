## Command-line Script
=============

Create the default project structure.

    cookiecutter https://github.com/drivendata/cookiecutter-data-science

Create an environment to work in that has the same name as the project.

    conda create -n pumps python=3.6

Cookiecutter Data Science provides a shortcut for the `conda create` command:

    make create_environment

Activate the conda environment:

    source activate pumps

-------

Edit `requirements.txt` to add relevant dependencies to your project. Pin these to specific versions as appropriate. These are the dependencies that we need for all our demo steps.

    jupyter
    ipython
    numpy
    pandas
    matplotlib
    scikit-learn
    scipy
    pytest
    nbdime
    runipy
    seaborn

Install the requirements.

    pip install -r requirements.txt

Copy the notebook from the `data-science-is-software` project to our new project. Obvi, this step is only for the demo--if you're using these steps for your own project, don't bother!

    cp ~/dd-dsis/notebooks/1-hr-lecture.ipynb notebooks/


## Testing

Create a file called `test_features.py` to put our tests in. The file needs to start with `test_` so py.test can find it.

    touch src/features/test_features.py

Make Python recognize `features` as  a module:

    touch src/features/__init__.py

Edit `test_features.py` to include a function called `test_remove_invalid_data`. Have this call the `remove_invalid_data` method. Then you can run the tests simply by typing.

    pytest src

## Code Coverage

Code coverage tells us how much of our code our tests actually exercised. The `run` command executes the tests. The `html` command creates the report. Then we can open it in a browser.

    coverage run --source src -m py.test
    coverage html
    open htmlcov/index.html


## Collaboration

Run a notebook as a standalone script rather than using the Jupyter web server:

    runipy notebooks/1-hr-lecture.ipynb

Coding standards are important. Pick norms and stick to them across your code base. `flake8` is HIGHLY recommended.

   flake8 src

Using version control with notebooks is challenging. Here are some ways that it can be made easier with `git`.

Initialize a repository

    git init

Add your notebooks and make an initial commit.

    git add notebooks/
    git commit -m 'Initial notebook commit'

Now, you should edit the notebook so that it is different from your commit. Running the vanilla diff tool gives results that are impossible to read.

    git diff notebooks/

The `nbdime` package provides a tool for configuring git to use it's notebook-aware diffing.

    git-nbdiffdriver config --enable

Now when we run the diff, we get beautiful output.

    git diff notebooks/


### Create .py on notebook save

Additionally, it can be helpful if you use a service like github to make viewing the code diffs in notebooks even easier. Because the Github web ui does not provide notebook-aware diffing, we can have jupyter automatically create a `.py` version of the notebook code every time we save the notebook. Keeping this `.py` file up to date automatically means that it's easier to track when code in notebooks changed with a web UI like GitHub. First, use your text editor to open the jupyter config:

    atom ~/.jupyter/jupyter_notebook_config.py

Then, we can paste in the auto-saving functions from this gist:

    http://bit.ly/py-html-config

Now we can tell the script that we want to save .py and .html versions of the notebooks automatically to a folder with the same name as the notebook. We do that simply by adding an indicator file to the folder:

    touch notebooks/.ipynb_saveprogress


### Pre-commit hooks

Finally, we don't want to be the person who breaks the build (or violates our code norms). We can have `git` automatically run our code standards tool and our tests before it let's us commit. This way, we never commit failing code.

    echo "flake8 src && pytest src" > .git/hooks/pre-commit

Now try a commit and `flake8` and `pytest` will run.

    git commit -m 'Test hook'
