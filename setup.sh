
setup_data_help() {

echo Step 1: download https://www.kaggle.com/fernandol/countries-of-the-world/downloads/countries-of-the-world.zip/1
echo Step 2: pip install csvkit
echo Step 3: Clean up the csv file, remove unwanted columns using csvkit
echo Step 4: Load the csv file into mysql '(optional)'
echo Note: See README file for more information.

}

install_pkgs(){

python3 -m venv thisenv

# If the above does not work, run this:
# virtualenv  --python=python3  thisenv ; . ./thisenv/bin/activate

./thisenv/bin/pip install -r requirements.txt

}



