# Daily Battle

Daily Battle is a Python application that makes it easy to open daily battles on [Key-Drop](https://key-drop.com).

## Features

-   Easy to use
-   Joining battles quickly and easily
-   Automate joining battles [guide](#guide-to-automatic-battle-joining)

## Installation

```sh
pip install -r requirements.txt
python src/main.py
```

## Options

| Short option | Long option       | Description                |
| ------------ | ----------------- | -------------------------- |
| `-h`         | `--help`          | Show help                  |
| `-c COOKIE`  | `--cookie COOKIE` | Generate token from cookie |

## Guide to Automatic Battle Joining

Introducing how to automatically join battles every day. I will use a VPS with the Linux Alpine operating system. We will perform the basic steps and additionally install some packages.

Install the required packages using the following command:

```bash
sudo apk add git py3-pip py3-virtualenv chromium chromium-chromedriver
```

Open crontab by typing the following command in the terminal:

```bash
  crontab -e
```

Go to the [Key-Drop](https://key-drop.com/) website where you must be logged in. In your browser, open devtools with `CTRL+SHIFT+I`, then go to `Application > Cookies > session_id`, and copy the value.

Edit the crontab file:

```bash
  0 0 * * * python ~/path/to/daily-battle/src/main.py -cookie <session_id value>
```

## Disclaimer

Please note that the Daily Battle is a third-party application and is not affiliated with Key-Drop. Use it responsibly and in accordance with Key-Drop's terms and conditions. The application is provided as-is, and the developers are not responsible for any misuse or consequences arising from its usage.
