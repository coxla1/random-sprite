# random-sprite
Using [PyZ3R library](https://github.com/tcprescott/pyz3r), select a random sprite from a restricted list, apply a MSU pack (if available) and then launch the seed.

# Install instructions
* Clone or download this repository.
* Install [Python 3.6+](https://www.python.org/), _don't forget to add to PATH variable when installing_.
* In a command line, install the requirements using : `python -m pip install -r requirements.txt`
* Rename `default.yaml` to `config.yaml`
* Copy the JAP 1.0 ROM of ALTTP in the current directory (google for it) with the following name (this can also be edited in `config.yaml`) : `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`
* If you want to automatically start the seed when generated : associate `.sfc` file extension with your emulator.

# Usage
* Configure your settings by editing `config.yaml` file (options are the ones available on the website)
* Either execute `run.bat` (Windows only) or do the following from command line : `python main.py`
* Paste seed URL, wait for it to create a patched file in `output/`
* Note : if you automatically start the seed, the command line will not close, you can do it when emulator has started.