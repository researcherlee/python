UDP/TCP Echo Server

----

To test:
$ python test.py

To run:
(1) tcp server with default port (8081)
    $ python echo_server.py -t

    (2) udp server with specific port 8888
    $ python echo_server.py -u -p 8888

    To get help:
    $ python echo_server.py

    Test using telnet:
    (1) run tcp server
    $ python echo_server.py -t
    (2) run telnet and enter any key
    $ telnet <server ip> <server port>

    Report bugs to <reliablelee@samsung.com> or <reliablelee@gmail.com> 

