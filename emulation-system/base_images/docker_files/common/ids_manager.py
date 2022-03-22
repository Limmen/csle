import csle_collector.ids_manager.ids_manager as ids_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the ids_manager server", type=int)
    args = parser.parse_args()
    ids_manager.serve(port=args.port)