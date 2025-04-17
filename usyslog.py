# circuitpython-usyslog 20250416a
# https://github.com/ageagainstthemachine/circuitpython-usyslog

"""
This syslog client can send UDP packets to a remote syslog server.

Features:
- Supports sending log messages using the UDP protocol.
- Supports syslog message priority formatting (facility + severity).
- Supports optional RFC 3164-style timestamps, hostnames, and program tags.
- Designed for use with CircuitPython and its `socketpool` module.

Limitations:
- No TCP transport or acknowledgment of receipt.
- Structured data (RFC 5424) is not supported.
- Timestamps are local and require a synchronized RTC or NTP.

For more information, see RFC 3164 (The BSD Syslog Protocol).
"""

import time
import socketpool

# Facility constants (per RFC 3164)
F_KERN = 0      # kernel messages
F_USER = 1      # user-level messages
F_MAIL = 2      # mail system
F_DAEMON = 3    # system daemons
F_AUTH = 4      # security/authorization messages
F_SYSLOG = 5    # messages generated internally by syslogd
F_LPR = 6       # line printer subsystem
F_NEWS = 7      # network news subsystem
F_UUCP = 8      # UUCP subsystem
F_CRON = 9      # clock daemon
F_AUTHPRIV = 10 # security/authorization messages (private)
F_FTP = 11      # FTP daemon
F_NTP = 12      # NTP subsystem
F_AUDIT = 13    # log audit
F_ALERT = 14    # log alert
F_CLOCK = 15    # clock daemon (not standard, but used by some systems)
# Local use facilities
F_LOCAL0 = 16
F_LOCAL1 = 17
F_LOCAL2 = 18
F_LOCAL3 = 19
F_LOCAL4 = 20
F_LOCAL5 = 21
F_LOCAL6 = 22
F_LOCAL7 = 23

# Severity constants (per RFC 3164)
S_EMERG = 0
S_ALERT = 1
S_CRIT = 2
S_ERR = 3
S_WARN = 4
S_NOTICE = 5
S_INFO = 6
S_DEBUG = 7

class SyslogClient:
    """
    Base class for syslog clients. Provides log level methods and
    builds properly formatted syslog messages according to RFC 3164.
    
    Args:
        facility (int): The default syslog facility code.
        tag (str, optional): An application name or identifier (TAG). Default is None.
        hostname (str, optional): Hostname of the sender. Default is None.
        include_timestamp (bool): If True, include RFC 3164-style timestamp. Default is True.
    """
    def __init__(self, facility=F_USER, tag=None, hostname=None, include_timestamp=True):
        self._facility = facility
        self._tag = tag
        self._hostname = hostname
        self._include_timestamp = include_timestamp

    def _format_timestamp(self):
        """Returns a timestamp string in RFC 3164 format: 'Mmm dd hh:mm:ss'"""
        now = time.localtime()
        month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = month_abbr[now.tm_mon - 1]
        day = f"{now.tm_mday:2}"  # Space-padded day
        timestamp = f"{month} {day} {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"
        return timestamp

    def _build_message(self, severity, message, tag=None, hostname=None, include_timestamp=None):
        """
        Formats the complete syslog message according to RFC 3164.

        Supports runtime overrides for tag, hostname, and timestamp.
        """
        pri = (self._facility << 3) + severity
        header_parts = []

        # Use runtime or instance timestamp setting
        if include_timestamp is None:
            include_timestamp = self._include_timestamp

        if include_timestamp:
            header_parts.append(self._format_timestamp())

        actual_hostname = hostname if hostname is not None else self._hostname
        if actual_hostname:
            header_parts.append(actual_hostname)

        header = " ".join(header_parts)

        actual_tag = tag if tag is not None else self._tag
        if actual_tag:
            formatted_msg = f"{actual_tag}: {message}"
        else:
            formatted_msg = message

        if header:
            return f"<{pri}>{header} {formatted_msg}"
        else:
            return f"<{pri}>{formatted_msg}"

    def log(self, severity, message, tag=None, hostname=None, include_timestamp=None):
        """
        Send a log message with the specified severity.

        Optional runtime overrides:
        - tag (str): overrides default tag for this message
        - hostname (str): overrides default hostname for this message
        - include_timestamp (bool): whether to include timestamp for this message
        """
        data = self._build_message(severity, message, tag, hostname, include_timestamp)
        self._sock.sendto(data.encode(), self._addr)

    # Common severity-level shortcuts
    def alert(self, msg):
        self.log(S_ALERT, msg)

    def critical(self, msg):
        self.log(S_CRIT, msg)

    def error(self, msg):
        self.log(S_ERR, msg)

    def warning(self, msg):
        self.log(S_WARN, msg)

    def notice(self, msg):
        self.log(S_NOTICE, msg)

    def info(self, msg):
        self.log(S_INFO, msg)

    def debug(self, msg):
        self.log(S_DEBUG, msg)

class UDPClient(SyslogClient):
    """
    UDP implementation of the SyslogClient. Sends messages using the
    CircuitPython-compatible socketpool module over a UDP socket.

    Args:
        pool (socketpool.SocketPool): The socket pool, typically from wifi.radio or esp32spi.
        ip (str): IP address of the syslog server.
        port (int): UDP port number (default 514).
        facility (int): Syslog facility code.
        tag (str, optional): Optional TAG for the application.
        hostname (str, optional): Optional hostname string to include.
        include_timestamp (bool): Whether to prepend a timestamp.
    """
    def __init__(self, pool, ip='127.0.0.1', port=514,
                 facility=F_USER, tag=None, hostname=None, include_timestamp=True):
        super().__init__(facility, tag, hostname, include_timestamp)
        self._pool = pool
        self._addr = pool.getaddrinfo(ip, port)[0][-1]
        self._sock = self._pool.socket(pool.AF_INET, self._pool.SOCK_DGRAM)

    def close(self):
        """Closes the UDP socket to free resources."""
        self._sock.close()

    def __enter__(self):
        """Enables use with 'with' statements for automatic cleanup."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
