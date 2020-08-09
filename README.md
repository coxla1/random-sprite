# select-random-sprite
Using Selenium and Chrome, select a random sprite from a restricted list. 

# Install instructions
* Clone or download this repository.
* Install [Python 3.x](https://www.python.org/), _don't forget to add to PATH variable when installing_.
* Install [Google Chrome](https://www.google.com/intl/en/chrome/).
* Finally download the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) corresponding to your version (most liley the latest) and unzip it in the current directory.
* In a command line, install the requirements using :
`python -m pip install -r requirements.txt`
	
* Rename `default.yaml` to `config.yaml`
* Copy the JAP 1.0 ROM of ALTTP in the current directory (no link here, google for it) with the following name (this can also be edited in config.yaml) : 
`Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

# Usage
* Configure your settings by editing config.yaml file (options are the same available on the website)
* Either execute `run.bat` (Windows only) or do the following from command line :
`python main.py`
* Paste seed URL, wait for it to download (Do not try to interfere with the page)
