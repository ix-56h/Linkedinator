# Linkedinator

Linkedin bot to connect with people who's corresponding to your search configuration.

![Linkedinator](https://www.zupimages.net/up/20/10/sq8g.png)

## Installation

```bash
sh setup.sh
```
Download the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) corresponding to your chrome version and your system and unzip into `drivers` directory.

## Usage

```
usage: linkedinator.py [-h] [-g {1,2}] [-r {1,2,3,4}] [-m MAX] [-l LOCATION]
                       [-L] [--auto]

optional arguments:
  -h, --help            show this help message and exit
  -g {1,2}, --gender {1,2}
                        Get profile by gender. 1 = Woman, 2 = Man
  -r {1,2,3,4}, --range {1,2,3,4}
                        Set "mutual connection" search argument. 4 = All,
                        Default = Don't care
  -m MAX, --max MAX     Set maximum connections requests. Default = 50
  -l LOCATION, --location LOCATION
                        Set the chrome binary location
  -L, --live            Run the bot in live mod
  --auto                Connect automatically with everyone.
```

## License
[WTFPL](http://www.wtfpl.net/)
