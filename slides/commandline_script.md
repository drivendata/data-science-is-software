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

    pip install -r requirements.txt


cp ~/dd-dsis/notebooks/1-hr-lecture.ipynb water_pumps/notebooks/






coverage run --source src -m py.test
coverage html
open htmlcov/index.html
