import socket
import helper
from helper import ceasarCipher
import json

class SimpleServer:
    """
    This class creates a simple socket server that listens on a specific port.
    """    
    def __init__( self, host = '127.0.0.1', port = 9500 ):        
        self._host = host
        self._port = port
            
    def create_socket(self):        
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        except socket.error as err:
            print("socket creation failed with error: \n {0}".format(err))

    def start_server( self ):
        display_helper("Simple Server")
        # Create socket
        sock = self.create_socket()
        print("Socket created...")

                
        try:            
            with sock:
                # bind to port
                sock.bind( (self._host, self._port) )
                print("Socket bound to ", self._host)

                while True:
                    sock.listen(5)
                    print("Server is listening on port ", self._port)
                    
                    conn, addr = sock.accept()

                    #Establish client connection
                    print("Got connection from ", addr)
                    with conn:
                        while True:
                            data = conn.recv( 1024 )
                            if data == b'Hello':                        
                                print( "Server received '{0}'".format(data.decode()) )
                                print( "Server sending back - Certificate" )
                                # send Cert
                                server_cert = self.getCert()
                                conn.sendall(server_cert.encode('utf-8'))                    
                            else:
                                print( "Server received '{0}'".format(data.decode()) )
                                print( "Server sending back - 'Goodbye' response" )
                                print()
                                conn.sendall(b'Goodbye')  
                                break  
                    print("Connection closed ..")                    
                    conn.close()

        except socket.error as err:
            print("Socket use error: \n {0}".format(err))           
        
        
        print("Server shutting down ...")
        sock.close()
    

    def getCert(self):
        """ Create a mock certificate used by this server """
        
        return "CA: I am Simple Server Certificate"
        

    def shutdown_server( self ):
        exit_input = input("Do you want to exit/shutdown the server (y/n): ")
        decision = False
        if exit_input == 'y':
            decision = True
        
        return decision

def display_helper(msg):
    print("\n****************** ", msg, "******************\n")

if __name__ == "__main__":
    # Create simple server
    host = '127.0.0.1'
    port = 9500
    simple_server = SimpleServer( host, port )
    # Open connection
    simple_server.start_server()