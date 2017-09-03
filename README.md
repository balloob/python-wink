<img align="left" src="https://cloud.githubusercontent.com/assets/2147630/15595400/f5d7f8bc-237b-11e6-95b8-bb0353728e51.png"> Python Wink API

[![Join the chat at https://gitter.im/python-wink/python-wink](https://badges.gitter.im/python-wink/python-wink.svg)](https://gitter.im/bradsk88/python-wink?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/python-wink/python-wink.svg?branch=master)](https://travis-ci.org/python-wink/python-wink)
[![Coverage Status](https://coveralls.io/repos/github/python-wink/python-wink/badge.svg?branch=master)](https://coveralls.io/github/python-wink/python-wink?branch=master)

_This library is an attempt to implement the entire Wink API in Python 3._
_Documentation for the Wink API can be found here http://docs.winkapiv2.apiary.io/# however, from my experience it isn't kept up-to-date._

_This library also has support for the unoffical local API and doesn't require a rooted hub._

This library provides support for Wink in Home Assistant!

## To install
```bash
pip3 install python-wink
```

## Get developer credentials

1. Vist https://developer.wink.com/login
2. Crate an account and request your credentials. (Approval can take several days)
3. Enter in a redirect URL to point at your application.
4. Plug in your details into the test script below.

## Example usage

Print all light names and state, and toggle their states.

```python
import pywink

print("Please vist the following URL to authenticate.")
print(pywink.get_authorization_url("YOUR_CLIENT_ID", "YOUR_REDIRECT_URL"))
code = input("Enter code from URL:")
auth = pywink.request_token(code, "YOUR_CLIENT_SECRET")
pywink.set_wink_credentials("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET",
                                         auth.get("access_token"), auth.get("refresh_token"))

lights = pywink.get_light_bulbs()
for light in lights:
    print("Name: " + light.name())
    print("State: " + light.state())
    light.set_state(not light.state())
```
