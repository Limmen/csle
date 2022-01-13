import docker
import csle_common.constants.constants as constants
from csle_common.envs_model.config.generator.env_info import EnvInfo

def calculateCPUPercentUnix(v):
    cpuPercent = 0.0
    previousCPU = v['precpu_stats']['cpu_usage']['total_usage']
    cpuDelta = v['cpu_stats']['cpu_usage']['total_usage'] - previousCPU
    previousSystem = v['precpu_stats']['system_cpu_usage']
    systemDelta = v['cpu_stats']['system_cpu_usage'] - previousSystem
    if systemDelta > 0.0 and cpuDelta > 0.0:
        cpuPercent = (cpuDelta / systemDelta) * len(v['cpu_stats']['cpu_usage']['percpu_usage']) * 100
        return "{0:.2f}".format(cpuPercent)
    else:
        return cpuPercent

def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent

# again taken directly from docker:
#   https://github.com/docker/cli/blob/2bfac7fcdafeafbd2f450abb6d1bb3106e4f3ccb/cli/command/container/stats_helpers.go#L168
# precpu_stats in 1.13+ is completely broken, doesn't contain any values
def calculate_cpu_percent2(d, previous_cpu, previous_system):
    # import json
    # du = json.dumps(d, indent=2)
    # logger.debug("XXX: %s", du)
    cpu_percent = 0.0
    cpu_total = float(d["cpu_stats"]["cpu_usage"]["total_usage"])
    cpu_delta = cpu_total - previous_cpu
    cpu_system = float(d["cpu_stats"]["system_cpu_usage"])
    system_delta = cpu_system - previous_system
    online_cpus = d["cpu_stats"].get("online_cpus", len(d["cpu_stats"]["cpu_usage"]["percpu_usage"]))
    if system_delta > 0.0:
        cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0
    return cpu_percent, cpu_system, cpu_total


def calculate_blkio_bytes(d):
    """
    :param d:
    :return: (read_bytes, wrote_bytes), ints
    """
    bytes_stats = graceful_chain_get(d, "blkio_stats", "io_service_bytes_recursive")
    if not bytes_stats:
        return 0, 0
    r = 0
    w = 0
    for s in bytes_stats:
        if s["op"] == "Read":
            r += s["value"]
        elif s["op"] == "Write":
            w += s["value"]
    return r, w


def calculate_network_bytes(d):
    """
    :param d:
    :return: (received_bytes, transceived_bytes), ints
    """
    networks = graceful_chain_get(d, "networks")
    if not networks:
        return 0, 0
    r = 0
    t = 0
    for if_name, data in networks.items():
        r += data["rx_bytes"]
        t += data["tx_bytes"]
    return r, t

def graceful_chain_get(d, *args, default=None):
    t = d
    for a in args:
        try:
            t = t[a]
        except (KeyError, ValueError, TypeError) as ex:
            return default
    return t


def parse_stats(x):
    cpu_total = 0.0
    cpu_system = 0.0
    cpu_percent = 0.0
    # for x in self.d.stats(self.container_id, decode=True, stream=True):
    blk_read, blk_write = calculate_blkio_bytes(x)
    net_r, net_w = calculate_network_bytes(x)
    mem_current = x["memory_stats"]["usage"]
    mem_total = x["memory_stats"]["limit"]

    try:
        cpu_percent, cpu_system, cpu_total = calculate_cpu_percent2(x, cpu_total, cpu_system)
    except KeyError:
        cpu_percent = calculate_cpu_percent(x)

    r = {
        "pids": x["pids_stats"]["current"],
        "timestamp": x["read"],
        "cpu_percent": cpu_percent,
        "mem_current": mem_current,
        "mem_total": x["memory_stats"]["limit"],
        "mem_percent": (mem_current / mem_total) * 100.0,
        "blk_read": blk_read,
        "blk_write": blk_write,
        "net_rx": net_r,
        "net_tx": net_w,
    }
    return r


def docker_stats2():
    client1 = docker.from_env()
    client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
    parsed_containers = EnvInfo.parse_running_containers(client1=client1, client2=client2)
    streams = []
    for pc in parsed_containers:
        stream=pc.container_handle.stats(decode=True, stream=True)
        streams.append((stream, pc))

    while True:
        for st, pc in streams:
            # for stats in st:
            #     print(stats)
            #     if "system_cpu_usage" in stats["precpu_stats"]:
            #         cpu = calculateCPUPercentUnix(stats)
            #         print(f"cont: {pc.name}, CPU:{cpu}")
            #         break
            # print(next(st))
            # n = next(st)
            n = next(st)
            parsed_stats = parse_stats(n)
            print(parsed_stats)
            # print(n)
            # if "system_cpu_usage" in n["precpu_stats"]:
            #     cpu = calculateCPUPercentUnix(n)
            #     print(f"cont: {pc.name}, CPU:{cpu}")

def docker_stats():
    client1 = docker.from_env()
    client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
    parsed_containers = EnvInfo.parse_running_containers(client1=client1, client2=client2)
    for pc in parsed_containers:
        stream=pc.container_handle.stats(decode=True, stream=True)
        for i in stream:
            print("container:{}".format(pc.name))
            try:
                cpuPercent = calculateCPUPercentUnix(i)
            except KeyError:
                continue
            print(cpuPercent)
        break



if __name__ == '__main__':
    docker_stats2()