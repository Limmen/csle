import csle_collector.kafka_manager.kafka_manager as kafka_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the kafka_manager server", type=int, default=50051)
    parser.add_argument("-i", "--ip", help="the ip of the kafka server", type=str, default=None)
    parser.add_argument("-ho", "--hostname", help="the hostname of the kafka server", type=str, default=None)
    args = parser.parse_args()
    # kafka_manager.serve(port=args.port, ip=args.ip, hostname=args.hostname)
    kafka_manager.serve(port=50051, ip="55.254.1.72", hostname=None)