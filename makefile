TARGET=filecrypt
SOURCE=main.py
PYINSTALLER_CMD=pyinstaller --onefile -n $(TARGET) $(SOURCE)

all: build

build:
	@echo "Creating binary..."
	pyinstaller --onefile -n $(TARGET) $(SOURCE)

# Clean the build directories
clean:
	rm -rf build dist $(TARGET).spec

.PHONY: all clean
