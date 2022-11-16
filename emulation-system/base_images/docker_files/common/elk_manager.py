import csle_collector.elk_manager.elk_manager as elk_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the ELK manager server", type=int)
    args = parser.parse_args()
    elk_manager.serve(port=args.port)