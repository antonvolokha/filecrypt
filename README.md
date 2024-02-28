# Crypt File like a Mr. Robot

This is a simple cli app allow to combine file and folders with images or audio files

## Compile & Install

Before compile this script please install requirements

```bash
make dependency
make
make install
```

## Usage
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