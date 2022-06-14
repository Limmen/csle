import csle_collector.ossec_ids_manager.ossec_ids_manager as ossec_ids_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the OSSEC ids_manager server", type=int)
    args = parser.parse_args()
    ossec_ids_manager.serve(port=args.port)