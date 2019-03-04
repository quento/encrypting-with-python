import socket
import helper
from helper import simpleCipher

class SimpleServer:
    """
    This class creates a simple socket server that listens on a specific port.
    """   

    server_private_key = ""
    _server_certificate = ""
    _server_public_key = ""
    _client_secret = ""

    def __init__( self, host = '127.0.0.1', port = 9500 ):        
        self._host = host
        self._port = port
        self._server_certificate = "CA: I am Simple Server Certificate"
        self._server_public_key = "Server Public Key"
                   
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
        status = False
                
        try:            
            with sock:
                # bind to port
                sock.bind( (self._host, self._port) )
                print("Socket bound to ", self._host)

                while True:
                    sock.listen(15)
                    print("Server is listening on port ", self._port)
                    
                    conn, addr = sock.accept()

                    #Establish client connection
                    print("Got connection from ", addr)
                    with conn:
                        while True:
                            data = conn.recv( 1024 )
                            print( "length of data received " + str(len(data)) )
                            if status == False:
                                if data == b'Hello':                        
                                    print( "Server received '{0}'".format(data.decode()) )
                                    print( "Server sending back - Certificate + Public Key" )
                                    # Put Cert + Public Key together and encrypt                                
                                    server_cert = simpleCipher( self.compileCertificate(),1,'e' ) 
                                    print("server_cert: " + server_cert)                              
                                    conn.sendall(server_cert.encode('utf-8'))                                                    
                                elif len(data) == 0:                             
                                    conn.sendall(b'Goodbye')  
                                    break 
                                else:
                                    print( "Server received '{0}'".format(data.decode()) )
                                    print( "Key+Secret Decrypted = " + simpleCipher( data.decode(),1,'d') )
                                    decrypt_secret = simpleCipher( data.decode(),1,'d')
                                    self.setClientSecret(decrypt_secret)

                                    print( "Server sending back - 'Ready to communicate' will use client secret " + self._client_secret )
                                    print()
                                    #Send response using secret
                                    secret_response = simpleCipher('Read to commnicate using secret~' + self.getClientSecret(),1,'e')
                                    conn.sendall(secret_response.encode()) 
                                    status == True
                            elif data.decode().find('VojrvfLfz') > -1:  # the word 'UniqueKey' encrypted
                                    conn.sendall(b'Recieved: ' + data.decode())
                    print("Connection closed ..")                    
                    conn.close()

        except socket.error as err:
            print("Socket use error: \n {0}".format(err))           
        
        
        print("Server shutting down ...")
        sock.close()
    
    def setClientSecret(self, client_msg):
        """ Retrieve client secret from msg sent using public key """
        self._client_secret = client_msg.split("~")[1]        

    def getClientSecret(self):
        """ Return client secret """        
        return self._client_secret

    def getCert(self):
        """ Return the mock certificate used by this server """

        return self._server_certificate

    def getPublicKey(self):
        """ Create a simple string to represent the public key"""

        return self._server_public_key  

    def compileCertificate(self):
         """ Put together both the Certificate and Public Key """

         return  self.getCert() + "~" + self.getPublicKey()

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