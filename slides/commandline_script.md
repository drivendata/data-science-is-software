## Command-line Script
=============

    cookiecutter https://github.com/drivendata/cookiecutter-data-science


    conda create -n water_pumps python=3.6


    make create_environment


    source activate water_pumps


### BACK TO SLIDES

-------

# Edit `requirements.txt` to add

    jupyter
    ipython
    numpy
    pandas
    matplotlib
    watermark
    scikit-learn
    scipy
    pytest
    nbdime




    pip install -r requirements.txt


    cp ~/dd-dsis/notebooks/1-hr-lecture.ipynb water_pumps/notebooks/

### To Jupyter!


## Testing
    touch src/features/test_features.py
    touch src/features/__init__.py

    pytest src

## Coverage

    coverage run --source src -m py.test
    coverage html
    open htmlcov/index.html


## Collaboration

    git init
    flake8 src

    git-nbdiffdriver config --enable
    git add notebooks/
    git commit -m 'Initial notebook commit'

#### Edit the notebook

    git diff notebooks/

### Create .py on notebook save

    atom ~/.jupyter/jupyter_notebook_config.py


### Pre-commit hooks

    echo "flake8 src && pytest src" > .git/hooks/pre-commit
