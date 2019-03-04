import socket
import helper
from helper import simpleCipher

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
                            msg_recieved = data.decode()
                            cert_valid = False
                            # If msg is a certificate, check if it's valid.
                            if msg_recieved.find("CA:") > -1 or msg_recieved.find("DB:") > -1:
                                print("Certificate received. Checking validity ...")
                                if msg_recieved.find("DB:") > -1: # encrypted msg
                                    # Decrypt returns decrypted array
                                    decrypt_cert_and_key = simpleCipher( msg_recieved,1,'d' )
                                    decrypt_cert_and_key_array = self.readCert(decrypt_cert_and_key)
                                    server_cert = decrypt_cert_and_key_array[0]
                                    server_public_key = decrypt_cert_and_key_array[1]
                                    # TODO: Extract Cert and Public Key

                                    cert_valid = self.checkCertValidity(server_cert)     
                                    
                                if cert_valid == True:
                                    print( "Server received a VALID certificate '{0}'".format(data.decode()) )
                                    print( "Server sending back - Server's Public Key...." )                 
                                    # TODO: Send public key of Certificate.                   
                                    conn.sendall(server_public_key.encode())  
                                else:
                                    print( "Server received INVALID '{0}'".format(data.decode()) )
                                    print( "Server sending back - 'False' response" )
                                    print()
                                    conn.sendall(b'INVALID')  
                                    break
                            elif data == b'':
                                print("No data ...")
                                break
                            else:
                                print( "CA Server received '{0}'".format(data.decode()) )
                                print( "CA Server sending back - 'Goodbye' response" )
                                print()
                                conn.sendall(b'Goodbye')  
                                break  
                              
                    print("Connection closed ..")                    
                    conn.close()

                
        except socket.error as err:
            print("Socket use error: \n {0}".format(err))           
        
        
        print("Server shutting down ...")
        sock.close()
        
    def checkCertValidity(self, cert):
        """ Check if mock certificate is valid """

        cert_validity = False

        if cert == 'CA: I am Simple Server Certificate':  
            cert_validity = True
        
        return cert_validity
   
    def decrypt_cert(self,encrypted_cert):
        return simpleCipher( encrypted_cert,1,'d')

    def readCert(self,cert):
        """ Read certificate and seperate public key from certificate.
            @return = Returns an array with cert and public key.
        """
        
        return cert.split("~")        

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
    host = '127.0.2.1'
    port = 9000
    cert_server = CertServer( host, port )
    # Open connection
    cert_server.start_server()