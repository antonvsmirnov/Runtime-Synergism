#============================================================================#
#                                                                            #
# Github Repository: Runtime-Synergism                                       #
# Code Description:  Python socket SERVER for real-time byte string exchange #
#                                                                            #
#============================================================================#
from sys import exc_info


class Socket_Server:

    def __init__( self,
                  host_SERVER='127.0.0.1',
                  port_SERVER=55555,
                  backlog=1,
                  timeout=10,
                  **KWARGS ):
        from socket import socket as socket_socket
        from socket import AF_INET as socket_AF_INET
        from socket import SHUT_RDWR as socket_SHUT_RDWR
        from socket import SOCK_STREAM as socket_SOCK_STREAM
        self.SHUT_RDWR=socket_SHUT_RDWR
        self.host=host_SERVER
        self.port=port_SERVER
        self.timeout=timeout
        self.backlog=backlog
        self.socket=socket_socket( socket_AF_INET, socket_SOCK_STREAM )
        self.socket.bind(( self.host, self.port ))
        self.socket.settimeout( self.timeout )
        self.socket.listen( self.backlog )
        self.link=None
        print(f'\nSocket_Server.__init__():\n  {self.socket}')
# ....... End of __init__() .......




    def connect(self):
        try:
            print(f'\nSocket_Server.connect(): ======= timeout {self.timeout} sec.\n  {self.socket}')
            self.link,_ = self.socket.accept()
            print(f'  {self.link}')
        except:
            print(f"\n\nEXCEPTION: Socket_Server.connect()\n  {exc_info()}")
        finally:
            return self.link
# ....... End of connect() .......




    def write(self, message=None):
        try:
            self.link.sendall( message )
        except:
            print(f"\n\nEXCEPTION: Socket_Server.write()\n  {exc_info()}")
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
            print(f"\n\nEXCEPTION: Socket_Server.read_prefix()\n  {exc_info()}")
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
            print(f"\n\nEXCEPTION: Socket_Server.read_segment()\n  {exc_info()}")
        finally:
            return b''.join( message )
# ....... End of read_segment() .......




    def __del__(self):
        try:
            if self.link:
                self.link.shutdown(self.SHUT_RDWR)
                self.link.close()
                del self.link
            if self.socket:
                self.socket.shutdown(self.SHUT_RDWR)
                self.socket.close()
                del self.socket
        except:
            print(f"\n\nEXCEPTION: Socket_Server.__del__()\n  {exc_info()}\n")
        finally:
            self.link=None
            self.socket=None
# ....... End of __del__() .......




    def main( port_SERVER=44444,
              message=None,
              repeat=1,
              verbosity=1,
              **kwargs ):

        from time import time_ns
        from binascii import crc32

        server_outbound = Socket_Server( port_SERVER=port_SERVER, **kwargs )
        server_inbound = Socket_Server( port_SERVER=port_SERVER-1, **kwargs )
        outbound_link = server_outbound.connect()
        inbound_link = server_inbound.connect()
        
        inbound_fd, outbound_fd = inbound_link.fileno(), outbound_link.fileno()
        message_SERVER = message*repeat
        loop, T0, T1 = 0, 0, 0
        if verbosity>=1: print(f"\n======= Socket_Server activity log =======")
        while(True):
            loop += 1
            try:
                # >> outbound activity: send message to the CLIENT
                outbound_bytes = bytes( f"{loop}. {message_SERVER}",'UTF-8')
                outbound_size = len( outbound_bytes )
                outbound_hash = crc32(outbound_bytes)
                outbound_prefix = bytes( str(outbound_size)+'\n','UTF-8')
                T1=time_ns()
                server_outbound.write( outbound_prefix )
                server_outbound.write( outbound_bytes )
                T2=time_ns()

                # << inbound activity: verify the inbound_hash reported by the CLIENT 
                T3=time_ns()
                inbound_prefix = server_inbound.read_prefix( delimiter=b'\n' )
                inbound_size = int( inbound_prefix.decode('UTF-8') )
                inbound_bytes = server_inbound.read_segment( expected_size=inbound_size,buffer=100000 )
                T4=time_ns()
                inbound_hash = outbound_hash if inbound_bytes==bytes(str(outbound_hash),'utf-8') else crc32(inbound_bytes)
            except:
                print(f"\n\nEXCEPTION: Socket_Server.main() read\n  {exc_info()}")
                raise
            finally:
                if verbosity>=1: print(f'{loop:>5}. Socket_Server.main():{T2-T1:>12}:nsec{outbound_fd:>4}|>{outbound_hash:>11}_crc32 [byte]{outbound_size:<10} {T4-T3:>12}:nsec{inbound_fd:>4}|<{inbound_hash:>11}_crc32 [byte]{inbound_size:<10}')
# ....... End of main() .......
# ....... End of Socket_Server .......




if __name__=="__main__":
    from socket_parser import Socket_Parser as Parser
    config = Parser().parse() 
    Socket_Server.main( **config )



