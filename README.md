# Linkedinator - Elevate Your LinkedIn Networking

![Linkedinator](https://www.zupimages.net/up/20/10/sq8g.png)

Enhance your LinkedIn networking game with Linkedinator, your intelligent LinkedIn bot. Connect effortlessly with professionals who match your search criteria and build meaningful connections in just a few clicks.

## Installation

Getting started with Linkedinator is a breeze. Simply run the following command:

```bash
sh setup.sh
```

Additionally, download the appropriate [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) or [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0) based on your browser version and system architecture. Place the downloaded driver into the `drivers` directory.

## Usage

Linkedinator offers versatile functionality to tailor your networking approach. Here's how you can use it:

```shell
usage: linkedinator.py [-h] -d {firefox,chrome} [-g {1,2}] [-r {1,2,3,4}] [-m MAX] [-l LOCATION] [-L] [-P] [--debug] [--auto]
```

**Options**:

- `-h, --help`: Display this help message and exit.
- `-d {firefox,chrome}, --driver {firefox,chrome}`: Select the browser driver to use.
- `-g {1,2}, --gender {1,2}`: Filter profiles by gender. (1 = Woman, 2 = Man)
- `-r {1,2,3,4}, --range {1,2,3,4}`: Define the "mutual connection" search parameter. (4 = All, Default = Don't care)
- `-m MAX, --max MAX`: Set the maximum number of connection requests. (Default = 50)
- `-l LOCATION, --location LOCATION`: Specify the browser binary location.
- `-L, --live`: Activate the bot's live mode.
- `-P, --premium`: Connect exclusively with Premium members.
- `--debug`: Enable debugging mode.
- `--auto`: Automatically connect with everyone.

## Compatibility

- **OS X**: Enjoy image display functionality when using iTerm2.
- **Windows & Linux**: Image display is not supported on these platforms.

## License

Linkedinator is distributed under the [WTFPL](http://www.wtfpl.net/) license, offering you maximum freedom in its usage and modification.