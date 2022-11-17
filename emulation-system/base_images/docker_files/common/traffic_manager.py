import csle_collector.traffic_manager.traffic_manager as traffic_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the Traffic manager server", type=int)
    args = parser.parse_args()
    traffic_manager.serve(port=args.port)