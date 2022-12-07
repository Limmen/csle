import csle_ryu.constants.constants as constants
import argparse
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="the port to start the RYU controller", type=int)
    parser.add_argument("-w", "--webport", help="the port to start the RYU web interface", type=int)
    parser.add_argument("-c", "--controller", help="the controller file name", type=str)
    args = parser.parse_args()
    cmd = f"{constants.RYU.RYU_MANAGER} {constants.RYU.CONTROLLER_PORT_ARG} {args.port} " \
          f"{constants.RYU.LOG_FILE_ARG} /{constants.RYU.LOG_FILE} {constants.RYU.WEB_APP_PORT_ARG} {args.webport} " \
          f"{constants.RYU.APP_LISTS_ARG} " \
          f"{constants.RYU.OFCTL_REST_APP},{constants.RYU.OFCTL_REST_TOPOLOGY},{constants.RYU.OFCTL_WS_TOPOLOGY}," \
          f"{constants.RYU.OFCTL_GUI_TOPOLOGY},{constants.RYU.CONTROLLERS_PREFIX}{args.controller} " \
          f"{constants.RYU.OBSERVE_LINKS}"
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
    (output, err) = p.communicate()
