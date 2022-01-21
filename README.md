The Runtime-Synergism is a library for real-time length-prefixed byte string exchange between separate Python runtimes based on socket streams:

- Real-time
- Inter-process communication
- Length-prefixed byte string
- Socket streams
- Python


<br></br>

---
<h2 align="center"><b>Python Sockets:  socket_server.py  &  socket_client.py</b><br></br></h2>

The tandem of *Socket_Server* and *Socket_Client* classes handles system socket resources for inter-process communication (tested with Python 3.10.2). The *socket_server.py* runtime should be in a state of *accepting connections* before the *socket_client.py* runtime connects to it. The usage with socket transfer rate performance test is in the *main()* function.

The command line syntax and parsing logic are accessible by calling a *PYTHON* interpreter followed by the script name and one of help switch options ("-h", "--help"):

    `PYTHON socket_server.py --help`
    `PYTHON socket_client.py -h`

The command line import from file of socket configuration parameters is accessible with:

    `PYTHON socket_server.py @python_sockets.cfg`
    `PYTHON socket_client.py @python_sockets.cfg`

<br></br>
