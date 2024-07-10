clear

if (Test-Path -Path "./env") {
    ./env/Scripts/deactivate | Out-Null
    
    echo "Reactivating virtual environment..."
    
    ./env/Scripts/activate | Out-Null
    
    echo "Virtual environment has been reactivated.`n"
    
    echo "Checking for new dependencies..."

    pip install -r requirements.txt | Out-Null
}
else {
echo "Creating a python virtual environment..."

python -m venv env | Out-Null

./env/Scripts/activate | Out-Null

echo "A virtual environment has been created.`n"

echo "Installing dependencies..."

pip install -r requirements.txt | Out-Null
}

echo "Dependencies have been installed.`n"

cd ./OvO_dependencies

if (Test-Path -Path "./dist") {
    echo "Reinitializing the custom OvO dependencies package..."

    python setup.py sdist | Out-Null

    echo "Reinstalling the custom OvO dependencies package..."

    pip install ./dist/OvO_dependencies-1.0.0.tar.gz | Out-Null

    echo "Custom OvO dependencies package successfully reinstalled.`n"
}
else {
    echo "Initializing the custom OvO dependencies package..."

    python setup.py sdist | Out-Null

    echo "Installing the custom OvO dependencies package..."

    pip install ./dist/OvO_dependencies-1.0.0.tar.gz | Out-Null

    echo "Custom OvO dependencies package successfully installed.`n"
}

echo "Compiling algorithms..."

cd ../../java/ant_colony

javac -d bin ./src/antcolony/*.java

echo "Algorithms successfully compiled.`n"

cd ../../backend

echo "Initializing Flask API..."

python ./flask/app.py