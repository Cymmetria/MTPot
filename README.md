### Update:
### Cymmetria Research has released a new honeypot for the Apache Struts exploit, see more info here: https://github.com/Cymmetria/StrutsHoneypot

# CymmetriaResearch

MTPot is a simple open source honeypot, released under the MIT license for the use of the community.
Cymmetria Research, 2016.
http://www.cymmetria.com/
Please consider trying out the MazeRunner Community Edition, the free version of our cyber deception platform.
Written by: Itamar Sher (@itamar_sher), Dean Sysman (@DeanSysman), Imri Goldberg (@lorgandon)
Contact: research@cymmetria.com

Install
-------
* Python 2.7
* pip install telnetsrv
* pip install gevent

Usage
-------
usage: MTPot.py [-h] [-v] [-o OUTPUT] config

positional arguments:
  config                Path to a json config file, see README for all
                        available parameters

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase MTPot verbosity
  -o OUTPUT, --output OUTPUT
                        Output the results to this file

Config file keys
-------
* port - REQUIRED, The port MTPot will bind to.
* commands - REQUIRED, A python dict containing the commands expected to receive from the scanner (Mirai e.g.) as the keys and the responses as values. IMPORTANT: at the moment commands are assumed to be run under /bin/busybox. (e.g. command="ps" means that the command that would actually get handled is "/bin/busybox ps")
* ddos_name - REQUIRED, The name of the attack (Mirai e.g.) that will appear whenever a successful fingerprint has occured
* ip - REQUIRED, The IP address MTPot will bind to.
* syslog_address - OPTIONAL, Syslog IP address to send the fingerprinted IPs to.
* syslog_port - OPTIONAL, Syslog PORT.
* syslog_protocol - OPTIONAL, Protocol used by the syslog (TCP/UDP)


Also included are sample config files (mirai_conf.json, mirai_scanner_conf.json) built for fingerprinting mirai based on the code available from: https://github.com/jgamblin/Mirai-Source-Code

Important note on sample downloading
-------
We had to stop debugging mirai at some point. An issue left open is that the remote mirai infector crashes when it receives an expected response to one of its commands.

We did not have the time to work on this last issue (which apparently some folks see as a feature), but happy to get the help of the community if anyone wants to take a stab at making that aspect of the honeypot work.

Known Issues
-------
Some users reported to us that the telnetsrv library throws this exception:
> Traceback (most recent call last):
> File "/usr/lib/python2.7/dist-packages/gevent/greenlet.py", line 327, in run
> result = self._run(*self.args, **self.kwargs)
> File "/usr/local/lib/python2.7/dist-packages/telnetsrv/telnetsrvlib.py", line 821, in inputcooker
> c2 = self._inputcooker_getc(block=False)
> File "/usr/local/lib/python2.7/dist-packages/telnetsrv/telnetsrvlib.py", line 774, in _inputcooker_> getc
> if not self.inputcooker_socket_ready():
> File "/usr/local/lib/python2.7/dist-packages/telnetsrv/green.py", line 44, in inputcooker_socket_ready
> return gevent.select.select([self.sock.fileno()], [], [], 0) != ([], [], [])
> AttributeError: 'module' object has no attribute 'select'
> <Greenlet at 0x76600080: <bound method MyTelnetHandler.inputcooker of <main.MyTelnetHandler instance at 0x765f5e68>>> failed with AttributeError

This bug appears to be in the libtelnetsrv/gevent library, here's a temporary fix (at your own discretion and risk) to get rid of the exception:
Open green.py in telnetserv and add the following code to the beginning of the file -
```python
import select
```
And replace line 44
```python
return gevent.select.select([self.sock.fileno()], [], [], 0) != ([], [], []):)
```
With:
```python
return select.select([self.sock.fileno()], [], []) != ([], [], [])
```
