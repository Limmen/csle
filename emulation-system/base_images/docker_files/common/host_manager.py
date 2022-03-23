import csle_collector.host_manager.host_manager as host_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the host_manager server", type=int)
    args = parser.parse_args()
    host_manager.serve(port=args.port)