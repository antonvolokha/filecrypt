TARGET=filecrypt
SOURCE=main.py
PYINSTALLER_CMD=pyinstaller --onefile -n $(TARGET) $(SOURCE)

all: testing build clean

dependency:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment..."
	. venv/bin/activate
	@echo "Installing dependencies..."
	pip install -r requirements.txt

testing:
	@echo "Testing code..."
	pytest

build:
	@echo "Creating binary..."
	pyinstaller --onefile -n $(TARGET) $(SOURCE)

clean:
	rm -rf build $(TARGET).spec

clean_all:
	make clean
	rm -rf dist

install-binary: build
	@echo "Installing binary to /usr/local/bin..."
	sudo cp dist/$(TARGET) /usr/local/bin/$(TARGET)
	@echo "Installation complete. You can now run '$(TARGET)' from anywhere."

.PHONY: all clean_all
