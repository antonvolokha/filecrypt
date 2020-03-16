# Crypt File like a Mr. Robot

This is a simple script allow to combine file and folders with images or audio files

## Compile & Install

Before compile this script please install requirements

```bash
pip3 install -r requirements.txt
pyinstaller --onefile -n filecrypt main.py
```

## Usage
By default script use key from config.py

If you want to create new key use:
```bash
filecrypt --init
```

To crypt file use:
```bash
filecrypt -i inputfile.mp3 -o outputfile.mp3 -f myecretfile0.doc myseretfolder
```
To decrypt file use:
```bash
filecrypt -i crypted.mp3 -d
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)