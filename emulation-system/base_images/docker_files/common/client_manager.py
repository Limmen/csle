import csle_collector.client_manager as client_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the client_manager server", type=int)
    args = parser.parse_args()
    client_manager.serve(port=args.port)