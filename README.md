
# Daily Battle

Daily Battle is a Python application that makes it easy to open daily battles on [Key-Drop](https://key-drop.com).


## Features

- Easy to use
- Joining battles quickly and easily
- Automate joining battles [guide](#guide-to-automatic-battle-joining)


## Run Locally

Clone the project

```bash
  git clone https://github.com/Montazu/daily-battle.git
```

Go to the project directory

```bash
  cd daily-battle
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the script

```bash
  python battle.py
```


## Options

Short option|Long option|Description
---|---|---
`-h`|`--help`|Show help
`-c COOKIE`|`--cookie COOKIE`| Generate token from cookie

## Guide to Automatic Battle Joining

Go to the [Key-Drop](https://key-drop.com/) website where you must be logged in. In your browser, open devtools with `CTRL+SHIFT+I`, then go to `Application > Cookies > session_id`, and copy the value.

Open crontab by typing the following command in the terminal
```bash
  crontab -e
```

Edit the crontab file

```bash
  0 0 * * * python ~/path/to/daily-battle/battle.py -cookie <session_id value>
```

Now the script will run daily at midnight and join the free battle if you have any coupons available.
## Disclaimer

Please note that the Daily Battle is a third-party application and is not affiliated with Key-Drop. Use it responsibly and in accordance with Key-Drop's terms and conditions. The application is provided as-is, and the developers are not responsible for any misuse or consequences arising from its usage.