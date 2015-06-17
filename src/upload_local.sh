rm setup.py
cp setup_local.py setup.py
python3 setup.py sdist upload -r pypi
