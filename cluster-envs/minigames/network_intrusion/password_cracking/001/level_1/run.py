import json
import argparse
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description='Parse flags for running the cluster network')
    parser.add_argument("-r", "--run", help="Boolean parameter, if true, run containers",
                        action="store_true")
    parser.add_argument("-b", "--build", help="Boolean parameter, if true build containers",
                        action="store_true")
    args = parser.parse_args()
    return args

def read_config() -> dict():
    with open('./config.json') as json_file:
        data = json.load(json_file)
        return data

def prepare_args(config:dict) -> dict:
    args = {}
    for container in config["containers"]:
        cmd=""
        cmd = cmd + " PROJECT=" + config["project"]
        cmd = cmd + " NETWORK=" + config["network"]
        cmd = cmd + " MINIGAME=" + config["minigame"]
        cmd = cmd + " CONTAINER=" + container["name"]
        cmd = cmd + " VERSION=" + config["version"]
        cmd = cmd + " SUBNET=" + config["subnet"]
        cmd = cmd + " SUBNET_MASK_1=" + config["subnet_mask_1"]
        cmd = cmd + " SUBNET_MASK_2=" + config["subnet_mask_2"]
        cmd = cmd + " ROOT_USERS_FILE=" + config["root_users_file"]
        cmd = cmd + " NON_ROOT_USERS_FILE=" + config["non_root_users_file"]
        cmd = cmd + " FLAG_INFO_FILE=" + config["flag_info_file"]
        root_user_count = 1
        for root_user in container["root_users"]:
            cmd = cmd + " ROOT_USER_" + str(root_user_count) + "=" + root_user["username"]
            cmd = cmd + " ROOT_PW_" + str(root_user_count) + "=" + root_user["password"]
            root_user_count += 1

        non_root_user_count = 1
        for non_root_user in container["non_root_users"]:
            cmd = cmd + " NON_ROOT_USER_" + str(non_root_user_count) + "=" + non_root_user["username"]
            cmd = cmd + " NON_ROOT_PW_" + str(non_root_user_count) + "=" + non_root_user["password"]
            non_root_user_count += 1

        flag_count = 1
        for flag in container["flags"]:
            cmd = cmd + " FLAG_PATH_" + str(flag_count) + "=" + flag["path"]
            cmd = cmd + " FLAG_NAME_" + str(flag_count) + "=" + flag["name"]
            flag_count += 1
        args[container["name"]] = cmd
    return args

def run(config: dict, args: dict):
    for container in config["containers"]:
        cwd = "./containers/" + container["name"] + "/"
        cmd = "./run.sh"
        cmd = cmd + args[container["name"]]
        subprocess.Popen(cmd, shell=True, cwd=cwd)
        update_ssh_cmd = "ssh-keygen -f '~/.ssh/known_hosts' -R '" + container["ip"] + "'"
        subprocess.Popen(update_ssh_cmd, shell=True)

def build(config: dict, args: dict):
    for container in config["containers"]:
        cwd = "./containers/" + container["name"] + "/"
        cmd = "./build.sh"
        cmd = cmd + args[container["name"]]
        subprocess.Popen(cmd, shell=True, cwd=cwd)

if __name__ == '__main__':
    args = parse_args()
    config = read_config()
    cmd_args = prepare_args(config)
    if args.run:
        run(config, cmd_args)
    if args.build:
        build(config, cmd_args)
