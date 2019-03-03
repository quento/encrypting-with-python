import socket
import helper
from helper import ceasarCipher

class CertServer:
    """
    This class creates a simple certificate server that verifies a server belongs to a certain certificate
    """    
    def __init__( self, host = '127.0.2.1', port = 9000 ):        
        self._host = host
        self._port = port
            
    def create_socket(self):        
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        except socket.error as err:
            print("socket creation failed with error: \n {0}".format(err))

    def start_server( self ):
        display_helper("CA Server")
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
                                print( "Server sending back - 'Hi' response" )
                                # send thank you msg
                                conn.sendall(b'Hi')                    
                            else:
                                print( "Server received '{0}'".format(data.decode()) )
                                print( "Server sending back - 'Goodbye' response" )
                                print()
                                conn.sendall(b'Goodbye')  
                                break  
                    print("Connection closed ..")                    
                    conn.close()

                    # TODO: Need a better way to shutdown server without interrupting listening feature.
                    # exit_input = input("Do you want to exit/shutdown the server (y/n): ")
                    # if self.shutdown_server():
                    #     break
        except socket.error as err:
            print("Socket use error: \n {0}".format(err))           
        
        
        print("Server shutting down ...")
        sock.close()
    

    def readCert(self, cert):
        """ Check server certificate. If valid, return true. If not return false """
        
        server_cert = "I am Simple Server"

        decipher_cert = ceasarCipher(cert, -shift)
        
        result = False

        if server_cert == decipher_cert:
            result = True
        else:
            result = False

        return result

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