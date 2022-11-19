import csle_collector.traffic_manager.traffic_manager as traffic_manager
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the Traffic manager server", type=int)
    parser.add_argument("-ld", "--logdir", help="the directory to save log files", type=str)
    parser.add_argument("-lf", "--logfile", help="the name of the log file", type=str)
    parser.add_argument("-m", "--maxworkers", help="the maximum number of gRPC workers", type=int)
    args = parser.parse_args()
    traffic_manager.serve(port=args.port, log_dir=args.logdir, max_workers=args.maxworkers, log_file_name=args.logfile)