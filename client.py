import socket
import helper
from helper import simpleCipher, randomString

class SimpleClient:
    "Simple client that communicats with a socket server."

    server_public_key = ""
    # append a random string to client secret for each connection.
    client_secret = "This is Client Secret - UniqueKey=" + randomString(10)


    def __init__( self, host = '127.0.0.1', port = 9500  ):
        self._server = host
        self._port = port

    def create_socket( self ):
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        except socket.error as err:
            print("socket creation failed with error")

    def connect_to_server( self ):
        try:
            sock = self.create_socket()
            sock.connect( (self._server, self._port) )

            msg = input("Type in 'Hello' to get Hi response from server: ")

            print('Sending msg: ', msg ) 

            sock.sendall( msg.encode() )

            result = sock.recv( 4096 )

            response_msg = result.decode()
            print( 'Response received: ', response_msg )

            # Check if response has Certificate marker in msg.
            if response_msg.find("CA:") > -1 or response_msg.find("DB:") > -1:
                response_cert = response_msg
                
                print("Sending cert to CA server .....")
                # Verify Cert. with CA
                CA_status = self.checkWithCA('127.0.2.1', 9000, response_cert)

                if CA_status == True:
                    print("Certificate is valid. You may proceed")
                    print("Recieved public key for CA server...") 
                    print("Public Key = " + self.server_public_key) 
                    # TODO: Send Secret using "server public key"   
                    print("Sending Secret using server public key")     
                    
                    encrypt_client_secret = simpleCipher( self.server_public_key + "~" + self.client_secret,1,'e' )
                    print("Encrypted Secret = " + encrypt_client_secret)                                
                    sock.sendall( encrypt_client_secret.encode('utf-8') ) 
                else:
                    print("Warning: Certificate is invalid!!!")
            elif response_msg.find("VojrvfLfz") > -1:
                print('Received secret response: ' + response_msg)
            else:
                print("Response not secure!!")    
        except Exception as err:    
            print("Connection Error:\n {0}".format(err))

    def sendToServer(self,announce,msg):
        """ 
            Create a socket and send a message 
            @msg = Message to send
            @return: Return the response received.
        """ 
        response_msg = ""
        try:
            sock = self.create_socket()
            sock.connect( (self._server, self._port) )            

            print( announce + "...." ) 

            sock.sendall( msg.encode() )

            result = sock.recv( 4096 )

            response_msg = result.decode()
            
        except Exception as err:    
            print("Msg Send Error:\n {0}".format(err))
        
        return response_msg

    def checkCA(self, cert):
        status = False
        try:
            sock = self.create_socket()
            sock.connect( (self._server, self._port) )            

            print( "Sending CA cert for verification...." ) 

            sock.sendall( cert.encode() )

            result = sock.recv( 4096 )

            response_msg = result.decode()
            print( 'Response received: ', response_msg )

            if response_msg != 'INVALID':
                status = True
                self.server_public_key = response_msg
            
        except Exception as err:    
            print("CheckCA() Connection Error:\n {0}".format(err))
        
        return status

    def checkWithCA(self, host, port, cert):
        """ A certificate has been received, Check with CA if it's valid """
        ca_client = SimpleClient(host, port)
        ca_response = ca_client.checkCA(cert)
        # Bring public key over from CA server instance.
        self.server_public_key = ca_client.server_public_key
        return ca_response

def display_helper(msg):
    print("****************** ", msg, "******************")

if __name__ == "__main__":
    display_helper("Simple Client")

    # Test Simple Client
    simple_client = SimpleClient()

    # Connect to server
    simple_client.connect_to_server()

    display_helper("End Simple Client")