# Change Log

## 1.7.2
- Added Nest Cam sensor support and fixed some lint errors

## 1.7.1
- Extended lock feature can't be performed via local control. Set with online.
- Cleaned up imports/tests/style
- Use string formatting when logging

## 1.7.0
- Thermostat fixes for away mode.
- Support for Dome Siren/Chime

## 1.6.0
- Support for water heaters. Added support for adding new lock key codes.

## 1.5.2
- Fixed firmware update and added device deletion

## 1.5.1
- Support all binary_switches which use a binary field of powered or opened

## 1.5.0
- Change device names and hub pairing commands

## 1.4.2
- Changed try/except in local control calls to catch all errors

## 1.4.1
- Added timeout to local control calls

## 1.4.0
- Local control support for lights, locks, and switches

## 1.3.1
- Fixed fans speed selection

## 1.3.0
- Support for switch and light groups

## 1.2.6
- Calling set_user_agent sets the API_HEADERS user_agent

## 1.2.5
- Added functions for auth URL and getting token from code

## 1.2.4
- Added call to return users account details /users/me

## 1.2.3
- Wink Aros Bugfix

## 1.2.2
- Siren inherits from Base device

## 1.2.1
- Set default endpoint in wink_api_fetch

## 1.2.0
- Robot and Scene support

## 1.1.1
- Bugfix for Lutron lights missing object_id and object_type

## 1.1.0
- Support for Quirky Aros AC units
- Support for Quirky Refuel
- Support for Dropcam sensors
- Fix for leaksmart valves

## 1.0.0
- Switch to object_type for device type detection
- Hard coded user agent
- Support for Lutron connected bulb remotes
- Support for Sprinklers
- Support for main Powerstrip device
- Support for Wink Relay buttons
- Support for Smoke and CO severity sensors
- Support for Canary cameras
- Throttle API calls to /users/me/wink_devices to once every 60 seconds
- Sensor object are built based on capability not returned object_type

## 0.13.0
- Support for Ring door bell motion and button press.

## 0.12.1
- Added support for additional lock, garage door, siren, and sensor attributes/features

## 0.12.0
- Wink fan support

## 0.11.0
- Support for Wink hubs as sensors
- Added more generic attributes to base Wink device (manufacturer_device_model, manufacturer_device_id, device_manufacturer, model_name)

## 0.10.1
- Set the correct objectprefix for Wink Smoke/CO detectors and Piggy banks
- Remove all desired state code

## 0.10.0
- Support for Thermostats

## 0.9.0
- Support for Wink Smoke and CO detectors

## 0.8.0
- Support for Wink relay sensors and email/password auth

## 0.7.15
- Fix for PIR multisensors

## 0.7.14
- Return False on RGB support if HSB is also supported.

## 0.7.13
- Changed method of detecting WinkBulb capabilities

## 0.7.12
- Made WinkBulb constructor python 3-compatible.

## 0.7.11
- Added Wink leak sensor support

## 0.7.10
- Changed API URL

## 0.7.9
- Added Wink keys (Wink Lock user codes)

## 0.7.8
- Added support for retrieving the PubNub subscription details

## 0.7.7
- Stopped duplicating door switches in `get_devices_from_response_dict`
- Add support for Wink Shades

## 0.7.6
- Added ability to return the battery level if a device is battery powered

## 0.7.5
- Fixed bug where light bulb states were not updating.

## 0.7.4
- Fixed bug where we shouldn't have been indexing into an object

## 0.7.3
- Can now require desired_state to have been reached before updating state

## 0.7.2
- Conserving brightness when setting color (temperature, hue sat, etc.)

## 0.7.1
- Exposed bulb color support methods (E.g. supports_hue_saturation())

## 0.7.0
- Expanded color support for WinkBulbs
- Added ability to supply client_id, client_secret, and refresh_token
instead of access_token.  This should get around tokens expiring.

## 0.6.4
- Added available method to report "connection" status

## 0.6.3
- Override capability sensor device_id during update.

## 0.6.2
- Changed sensor brightness to boolean.
- Added UNIT to all sensors.

## 0.6.1
- Return the capability of a sensor as part of the name.

## 0.6.0
- Major structural change.  Using modules to avoid circular dependencies.
- Added support for devices that contain multiple onboard sensors.

## 0.5.0
- Major bug fix.  Methods like `get_bulbs` were always returning empty lists.

## 0.4.3
- Added better error handling for API authorization problems.

## 0.4.2
- Added init method for WinkSiren

## 0.4.1
- Treating offline binary switches as if they have a powered state of false

## 0.4.0
- Removed API responses from docstring and moved into unit tests.
- Refactored __init__.py to support easier unit testing

## 0.3.3
- Added init method for Wink Power strip

## 0.3.2
- Added init method for WinkGarageDoor

## 0.3.1.1
- Changed mock to test-only dependency

## 0.3.1
- Added init method for WinkEggTray

## 0.3.0
- Breaking change: Renamed classes to satisfy pylint

## 0.2.1
- Added ability to change color via setState
- Added ability to request color from wink_bulb object

## 0.2.0
- Initial work by balloob, ryanturner, and miniconfig
