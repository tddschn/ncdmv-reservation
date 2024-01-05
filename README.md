# NC DMV Reservation Tools

> Dealing with DMV is often a frustrating experience. But it doesn't have to be!

Automated availability checking and monitoring for DMV offices across the state of North Carolina, tested to work on Jan 2024.

No feature will be added unless I need it myself. If you need additional features, you're welcome to contribute a PR. :)

https://teddysc.me/blog/ncdmv-reservation

- [NC DMV Reservation Tools](#nc-dmv-reservation-tools)
  - [Background](#background)
  - [Quick Start](#quick-start)
    - [Installation](#installation)
    - [Running](#running)
  - [How it works](#how-it-works)
  - [Continuous Monitoring](#continuous-monitoring)
    - [On your local machine](#on-your-local-machine)
    - [GitHub Actions](#github-actions)
  - [Thoughts](#thoughts)
  - [Develop](#develop)
  - [Links](#links)

## Background

DMVs within reasonable distance of where I live are always completely booked, so I made this tool to help me spot when someone cancelled their appointment so I could snag it.

Since the tool was made for self-use only, currently it's hard-coded to only checks for the appointment type of `1st time Driver License Test (over 18)`. If you need additional features, you're welcome to contribute a PR. :)

I've used it to spot availability slot twice after running it for a few hours, and secured my reservation. :)

## Quick Start

### Installation

```bash
# install google-chrome / google-chrome-stable, and
# install chromedriver with your favorite package manager and put it in your $PATH
brew install chromedriver
# or sudo pacman -S chromedriver

# python3.12+ required
pipx install ncdmv-reservation
```

### Running

```
$ ncdmv-driver-license-office-availability | jq | tee ncdmv.json
[
  {
    "is_reservable": true,
    "office_name": "Aberdeen",
    "street_address": "521 S. Sandhills Blvd., Aberdeen, NC",
    "zip_code": "28315"
  },
  {
    "is_reservable": true,
    "office_name": "Ahoskie",
    "street_address": "242 N.C. 42 W., Ahoskie, NC",
    "zip_code": "27910"
  },
  {
    "is_reservable": true,
    "office_name": "Albemarle",
    "street_address": "611 Concord Road, Albemarle, NC",
    "zip_code": "28001"
  },
  {
    "is_reservable": true,
    "office_name": "Andrews",
    "street_address": "1440 Main St., Andrews, NC",
    "zip_code": "28901"
  },
  {
    "is_reservable": true,
    "office_name": "Asheboro",
    "street_address": "2754 U.S. 220 Business South, Asheboro, NC",
    "zip_code": "27205"
  },
  ...
]
```

Filtering for the DMV office you're interested in with `jq`:

```
$ <ncdmv.json jq '.[] | select(.office_name == "Raleigh West") | .is_reservable' -r
false
# so it's completely booked (the `Raleigh West` office)
```



## How it works

`ncdmv-driver-license-office-availability` spins up a chrome instance to click through the very user friendly DMV site, scrap the page, and convert it to structured JSON.

Use the `-H, --no-headless` option to see the chrome instance in action.


## Continuous Monitoring

### On your local machine

I found this approach more convenient for me.

```bash
dmv () {
	ncdmv-driver-license-office-availability | jq '.[] | select(.office_name == "Raleigh West") | .is_reservable' -r

}

# replace `say` if you're not on macOS
# you can change the frequency of the check by changing the `sleep` duration
dmv_monitor() {
	(while :; do [[ $(dmv) == true ]] && say 'go to dmv and reserve now'; sleep 60; done)&
}

# start monitoring every 60s, in the background
# don't close your terminal tab :)
dmv_monitor

# to stop it, run
# kill %1
# or just close the terminal tab. :)
```

### GitHub Actions

Email notification via sendgrid if the DMV office of your choice is reservable.

[The workflow file](https://gist.github.com/tddschn/a3da8a200f3599b29533e02945264d3f)




## Thoughts

After I wrote this I remembered that I should check GitHub first to see if someone else has already done it. 

Fortunately, their solutions are outdated, and I did not reinvent the wheel. :)


## Develop

```
$ git clone https://github.com/tddschn/ncdmv-reservation.git
$ cd ncdmv-reservation
$ poetry install
```

## Links

- Blog post: https://teddysc.me/blog/ncdmv-reservation
- Source code: https://github.com/tddschn/ncdmv-reservation
- PyPI: https://pypi.org/project/ncdmv-reservation/
