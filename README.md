# circuitpython-usyslog
This CircuitPython module implements a simple syslog client for CircuitPython. Currently only UDP-based remote logging without timestamps is implemented. This is a fork of [micropython-usyslog](https://github.com/kfricke/micropython-usyslog) which has been updated to incorporate changes required for modern CircuitPython usage.

## Background
An important part of creating IoT devices is the ability to gain observability through logging. One of the most widely-used methods of collecting logs from network devices is using syslog. This library can help when integrating logging capabilities in CircuitPython creations.

## Dependencies
This module requires use of the [socketpool](https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/index.html) library for CircuitPython. 

## Requirements
In order to use this module, a remote syslog server is also necessary to accept remote messages.
