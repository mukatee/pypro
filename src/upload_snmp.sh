rm setup.py
cp setup_snmp.py setup.py
python3 setup.py sdist upload -r pypi
