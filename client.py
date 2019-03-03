import socket

class SimpleClient:
    "Simple client that communicats with a socket server."

    def __init__( self ):
        self._server = '127.0.0.1'
        self._port = 9500

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

            print( 'Response received: ', result.decode() )
        except Exception as err:    
            print("Connection Error:\n {0}".format(err))


def display_helper(msg):
    print("****************** ", msg, "******************")

if __name__ == "__main__":
    display_helper("Simple Client")

    # Test Simple Client
    simple_client = SimpleClient()

    # Connect to server
    simple_client.connect_to_server()

    display_helper("End Simple Client")