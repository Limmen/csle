import subprocess

def create_docker_tc_daemon() -> None:
    """
    Creates the docker-tc daemon for controlling the traffic of the docker containers

    :return: None
    """
    # cmd = "docker run -d --name docker-tc --network host --cap-add NET_ADMIN --restart always " \
    #       "-v /var/run/docker.sock:/var/run/docker.sock -v /var/docker-tc:/var/docker-tc lukaszlach/docker-tc"
    cmd = "docker run -d --name docker-tc --network host --cap-add NET_ADMIN --restart always " \
          "-v /var/run/docker.sock:/var/run/docker.sock -v /var/docker-tc:/var/docker-tc https://github.com/Limmen/docker-tc"
    subprocess.Popen(cmd, shell=True)

    # Just pipe it to /dev/null since the container is likely already running and it will give an error
    # subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    #iperf3 -R -c 172.31.212.92
    #tc qdisc add dev eth0 root netem delay 20ms rate 1mbit
    #tc qdisc add dev eth0 root netem delay 20ms rate 10mbit
    #tc qdisc add dev eth0 root netem delay 20ms rate 1gbit limit 30000
    #tc qdisc add dev eth0 root netem delay 20ms rate 1gbit limit 30000
    # https://man7.org/linux/man-pages/man8/tc-netem.8.html


# Creates the docker-tc daemon for controlling the traffic of the docker containers
if __name__ == '__main__':
    create_docker_tc_daemon()
