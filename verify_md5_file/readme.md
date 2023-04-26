## Verify MD5 file

This tools will check that the files in a folder match the MD5 stored in an .md5 file in that same folder. 

Install requirements, with `venv`:

```python
# :
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r requirements.txt
```

Then, run giving the directory to check as an argument:

```python
python3 verify_md5_file.py [folder]
```
