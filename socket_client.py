#============================================================================#
#                                                                            #
# Github Repository: Runtime-Synergism                                       #
# Code Description:  Python socket CLIENT for real-time byte string exchange #
#                                                                            #
#============================================================================#
from sys import exc_info


class Socket_Client:

    def __init__( self,
                  host_CLIENT='127.0.0.1',
                  port_CLIENT=0,
                  host_SERVER='127.0.0.1',
                  port_SERVER=5555,
                  timeout=10,
                  **KWARGS):
        from socket import socket as socket_socket
        from socket import AF_INET as socket_AF_INET
        from socket import SHUT_RDWR as socket_SHUT_RDWR
        from socket import SOCK_STREAM as socket_SOCK_STREAM
        self.SHUT_RDWR=socket_SHUT_RDWR
        self.host_CLIENT=host_CLIENT
        self.host_SERVER=host_SERVER
        self.port_CLIENT=port_CLIENT
        self.port_SERVER=port_SERVER
        self.timeout=timeout
        self.link=None
        self.link=socket_socket(socket_AF_INET, socket_SOCK_STREAM)
        self.link.bind(( self.host_CLIENT, self.port_CLIENT ))
        self.link.settimeout( self.timeout )
        print(f'\nSocket_Client.__init__():\n  {self.link}')
# ....... End of __init__() .......




    def connect(self):
        try:
            self.link.connect(( self.host_SERVER, self.port_SERVER ))
            print(f'\nSocket_Clent.connect()\n  {self.link}')
        except:
            print(f"\n\nEXCEPTION: Socket_Clent.connect()\n  {exc_info()}")
        finally:
            return self.link
# ....... End of connect() .......




    def write(self, message=None):
        try:
            self.link.sendall(message)
        except:
            print(f"\n\nEXCEPTION: Socket_Client.write()\n  {exc_info()}")
        finally:
            pass
# ....... End of write() .......




    def read_prefix( self, buffer=1, delimiter=b'\n' ):
        message=[]
        token=None
        try:
            while (token != delimiter):
                 token = self.link.recv(buffer)
                 if not token: break
                 message.append( token )
        except:
            print(f"\n\nEXCEPTION: Socket_Client.read_prefix()\n  {exc_info()}")
        finally:
            return b''.join( message )
# ....... End of read_prefix() .......




    def read_segment( self,expected_size=0,buffer=1024 ):
        message = []
        collected_size = 0
        try:
            while (collected_size < expected_size):
                segment = self.link.recv( buffer )
                if not segment: break
                message.append( segment )
                collected_size += buffer
        except:
            print(f"\n\nEXCEPTION: Socet_Client.read_segment()\n  {exc_info()}")
        finally:
            return b''.join( message )
# ....... End of read_segment() .......




    def __del__(self):
        try:
            if self.link:
                self.link.shutdown(self.SHUT_RDWR)
                self.link.close()
                del self.link
        except:
            print(f"\n\nEXCEPTION: Socket_Client.__del__()\n  {exc_info()}")
        finally:
            self.link=None
# ....... End of __del__() .......




    def main( port_SERVER=44444,
              port_CLIENT=44445,
              verbosity=1,
              **kwargs ):

        from binascii import crc32
        from time import sleep, time_ns
        client_inbound = Socket_Client( port_SERVER=port_SERVER, port_CLIENT=port_CLIENT, **kwargs )
        client_outbound = Socket_Client( port_SERVER=port_SERVER-1, port_CLIENT=port_CLIENT+1, **kwargs )
        inbound_link = client_inbound.connect()
        outbound_link = client_outbound.connect()

        inbound_fd, outbound_fd = inbound_link.fileno(), outbound_link.fileno()
        loop, T0, T1 = 0, 0, 0
        if verbosity>=1: print(f"\n======= Socket_Client activity log =======")
        while(True):
            loop += 1
            try:
                # << inbound activity: read message from the SERVER
                T1=time_ns()
                inbound_prefix = client_inbound.read_prefix( delimiter=b'\n' )
                inbound_size = int( inbound_prefix.decode('UTF-8') )
                inbound_bytes = client_inbound.read_segment( expected_size=inbound_size,buffer=100000 )
                T2=time_ns()
                inbound_hash = crc32(inbound_bytes)

                # >> outbound activity: report the inbound_hash to the SERVER
                outbound_bytes = bytes( str(inbound_hash),'utf-8' )
                outbound_size = len( outbound_bytes )
                outbound_prefix = bytes( str(outbound_size)+'\n','UTF-8')
                outbound_hash = crc32(outbound_bytes)
                T3=time_ns()
                client_outbound.write( outbound_prefix )
                client_outbound.write( outbound_bytes )
                T4=time_ns()
            except:
                print(f"\n\nEXCEPTION: Socket_Client.main()\n  {exc_info()}")
                raise
            finally:
                if verbosity>=1: print(f'{loop:>5}. Socket_Client.main():{T2-T1:>12}:nsec{inbound_fd:>4}|<{inbound_hash:>11}_crc32 [byte]{inbound_size:<10} {T4-T3:>12}:nsec{outbound_fd:>4}|>{outbound_hash:>11}_crc32 [byte]{outbound_size:<10}')
# ....... End of main() .......
# ....... End of Socket_Client .......




if __name__=="__main__":
    from socket_parser import Socket_Parser as Parser
    config = Parser().parse() 
    Socket_Client.main( **config )



