# circuitpython-usyslog
This CircuitPython module implements a simple syslog client for CircuitPython. Currently only UDP-based remote logging without timestamps is implemented. This is a fork of [micropython-usyslog](https://github.com/kfricke/micropython-usyslog) which has been updated to incorporate changes required for modern CircuitPython usage.

## Features
- **UDP Transport**: Sends syslog messages over UDP via the CircuitPython-compatible `socketpool` module.
- **Facility & Severity Constants**: Predefined constants for all standard RFC 3164 facilities (KERN, USER, MAIL, DAEMON, …, LOCAL7) and severities (EMERG, ALERT, CRIT, ERR, WARN, NOTICE, INFO, DEBUG).
- **RFC 3164-Style Header**: Optional inclusion of a timestamp (`Mmm dd hh:mm:ss`), hostname, and application tag in each message.
- **Configurable Defaults**: Instantiation parameters allow setting default facility code, program tag, hostname, and whether timestamps are included.
- **Runtime Overrides**: Per-message overrides for tag, hostname, and timestamp inclusion in the `log()` call.
- **Convenience Methods**: Shortcut methods (`alert()`, `critical()`, `error()`, `warning()`, `notice()`, `info()`, `debug()`) for each severity level.
- **Context Manager Support**: The `UDPClient` implements `__enter__`/`__exit__` for use with Python’s `with` statement, ensuring sockets are closed automatically.
- **Resource Cleanup**: Explicit `close()` method on `UDPClient` to free socket resources when done.

## Background
An important part of creating IoT devices is the ability to gain observability through logging. One of the most widely-used methods of collecting logs from network devices is using syslog. This library can help when integrating logging capabilities in CircuitPython creations.

## Dependencies
This module requires use of the [`socketpool`](https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/index.html) library and the [`time`](https://docs.circuitpython.org/en/latest/shared-bindings/time/) module in CircuitPython for timestamp generation.

## Requirements
In order to use this module, a remote syslog server is also necessary to accept remote messages.

## API Reference

### Facility Constants (RFC 3164)
- `F_KERN`, `F_USER`, `F_MAIL`, `F_DAEMON`, `F_AUTH`, `F_SYSLOG`, `F_LPR`, `F_NEWS`,
  `F_UUCP`, `F_CRON`, `F_AUTHPRIV`, `F_FTP`, `F_NTP`, `F_AUDIT`, `F_ALERT`, `F_CLOCK`,
  `F_LOCAL0`-`F_LOCAL7`

### Severity Constants (RFC 3164)
- `S_EMERG`, `S_ALERT`, `S_CRIT`, `S_ERR`, `S_WARN`, `S_NOTICE`, `S_INFO`, `S_DEBUG`

## Limitations
- No TCP transport or acknowledgment of receipt.
- Structured data (RFC 5424) is not supported.
- Timestamps are local and require a synchronized RTC or NTP on the device.

## Reference Material
- **RFC 3164**: The BSD Syslog Protocol
- **CircuitPython `socketpool`** documentation
- **CircuitPython `time`** documentation

## Disclaimer
This library is probably unstable and full of bugs. Like everything else on the internet, run/use at your own risk.

