# Linkedinator

Linkedin bot to connect with people who's corresponding to your search configuration.

![Linkedinator](https://www.zupimages.net/up/20/10/sq8g.png)

## Installation

```bash
sh setup.sh
```
Download the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) or [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0) corresponding to your browser version and your system into `drivers` directory.

## Usage

```
usage: linkedinator.py [-h] -d {firefox,chrome} [-g {1,2}] [-r {1,2,3,4}] [-m MAX] [-l LOCATION] [-L] [-P] [--debug]
                       [--auto]

optional arguments:
  -h, --help            show this help message and exit
  -d {firefox,chrome}, --driver {firefox,chrome}
                        Set the driver to use.
  -g {1,2}, --gender {1,2}
                        Get profile by gender. 1 = Woman, 2 = Man
  -r {1,2,3,4}, --range {1,2,3,4}
                        Set "mutual connection" search argument. 4 = All, Default = Don't care
  -m MAX, --max MAX     Set maximum connections requests. Default = 50
  -l LOCATION, --location LOCATION
                        Set the browser binary location
  -L, --live            Run the bot in live mod
  -P, --premium         Connect only with Premium
  --debug               Set debug flag
  --auto                Connect automatically with everyone.
```

## OS X
Use iterm2 if you want to see images in your terminal.

## WINDOWS & LINUX
Can't display images, sorry.

## License
[WTFPL](http://www.wtfpl.net/)
