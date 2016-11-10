###
# MTPot is a simple open source honeypot, released under the MIT license for the use of the community.
#
# Cymmetria Research, 2016.
# http://www.cymmetria.com/
#
# Please consider trying out the MazeRunner Community Edition, the free version of our cyber deception platform.
#
# Written by: Itamar Sher (@itamar_sher), Dean Sysman (@DeanSysman), Imri Goldberg (@lorgandon)
# Contact: research@cymmetria.com
###

import logging
import logging.handlers
import socket

class InvalidSyslogSocktype(Exception):
    pass

class MySysLogHandler(logging.handlers.SysLogHandler):
    def emit(self, record):
        """
        Emit a record.

        The record is formatted, and then sent to the syslog server. If
        exception information is present, it is NOT sent to the server.
        """
        msg = self.format(record) + '\n'
        # We need to convert record level to lowercase, maybe this will
        # change in the future.

        prio = '<%d>' % self.encodePriority(self.facility,
                                            self.mapPriority(record.levelname))
        # Message is a string. Convert to bytes as required by RFC 5424
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        msg = prio + msg
        try:
            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except socket.error:
                    self.socket.close() # See issue 17981
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def get_syslog_logger(syslog_address, syslog_port, sock_type):
    if sock_type == "TCP":
        syslog_handler_tcp = MySysLogHandler(
            address=(syslog_address, syslog_port),
            socktype=socket.SOCK_STREAM)
    elif sock_type == "UDP":
        syslog_handler = MySysLogHandler(
            address=(syslog_address, syslog_port),
            socktype=socket.SOCK_DGRAM)
    else:
        raise InvalidSyslogSocktype("Invalid socktype={} (TCP/UDP)".format(sock_type))
    syslogger = logging.getLogger("HoneySyslog")
    syslogger.setLevel(logging.INFO)
    syslogger.addHandler(syslog_handler)
    return syslogger
