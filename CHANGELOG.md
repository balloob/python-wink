# Change Log

## 0.7.14
- If light supports rgb and hsv default to hsv only

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
- Added support for retrieving the Pubnub subscription details

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
