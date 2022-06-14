import csle_collector.snort_ids_manager.snort_ids_manager as snort_ids_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the Snort ids_manager server", type=int)
    args = parser.parse_args()
    snort_ids_manager.serve(port=args.port)