import shutil
import io
from getpass import getpass
import subprocess

RELEASE_CONFIG = {
    "csle-ryu": {
        "new_version": "0.0.22",
    },
    "csle-collector": {
        "new_version": "0.0.73",
    },
    "csle-attacker": {
        "new_version": "0.0.4",
    },
    "csle-defender": {
        "new_version": "0.0.4",
    },
    "csle-system-identification": {
        "new_version": "0.0.4",
    },
    "gym-csle-stopping-game": {
        "new_version": "0.0.4",
    },
    "csle-agents": {
        "new_version": "0.0.4",
    },
    "csle-rest-api": {
        "new_version": "0.0.4",
    },
    "csle-cli": {
        "new_version": "0.0.4",
    },
}


if __name__ == '__main__':
    username = input("Enter PyPi username: ")
    password = getpass()
    print(password)
    print(username)

    # Verify versions
    for lib, versions in RELEASE_CONFIG:
        with io.open(f"{lib}/src/{lib.replace('-', '_')}/__version__.py", 'r', encoding='utf-8') as f:
            version = f.read().split("=")[-1].lstrip()
            versions["old_version"] = version
            if versions["old_version"] == versions["new_version"]:
                raise ValueError(f"Release with version {versions['old_version']} of {lib} already exists")

    # Update __version__.py files
    for lib, versions in RELEASE_CONFIG:
        with io.open(f"{lib}/src/{lib.replace('-', '_')}/__version__.py", 'rw', encoding='utf-8') as f:
            file_contents = f.read()
            file_contents = file_contents.replace(versions["old_version"], versions["new_version"])
            f.write(file_contents)

    # Update requirements.txt files
    for lib, versions in RELEASE_CONFIG:
        with io.open(f"{lib}/requirements.txt", 'rw', encoding='utf-8') as f:
            file_contents = f.read()
            file_contents = file_contents.replace(f"{lib}=={versions['old_version']}",
                                                  f"{lib}=={versions['new_version']}")
            file_contents = file_contents.replace(f"{lib}>={versions['old_version']}",
                                                  f"{lib}>={versions['new_version']}")
            file_contents = file_contents.replace(f"{lib}=>{versions['old_version']}",
                                                  f"{lib}=>{versions['new_version']}")
            f.write(file_contents)

    # Update setup.cfg files
    for lib, versions in RELEASE_CONFIG:
        with io.open(f"{lib}/setup.cfg", 'rw', encoding='utf-8') as f:
            file_contents = f.read()
            file_contents = file_contents.replace(f"{lib}=={versions['old_version']}",
                                                  f"{lib}=={versions['new_version']}")
            file_contents = file_contents.replace(f"{lib}>={versions['old_version']}",
                                                  f"{lib}>={versions['new_version']}")
            file_contents = file_contents.replace(f"{lib}=>{versions['old_version']}",
                                                  f"{lib}=>{versions['new_version']}")
            f.write(file_contents)

    # Delete old build directories
    for lib, versions in RELEASE_CONFIG:
        shutil.rmtree(f"{lib}/dist", ignore_errors=True)

    # Build
    for lib, versions in RELEASE_CONFIG:
        p = subprocess.Popen(f"cd {lib}; python3 -m build", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        output = str(output)
        print(output)

    # Push
    for lib, versions in RELEASE_CONFIG:
        p = subprocess.Popen(f"cd {lib}; python3 -m twine upload dist/* -p {password} -u {username}", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        output = str(output)
        print(output)


