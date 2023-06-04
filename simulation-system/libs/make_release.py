import shutil
import io
from getpass import getpass
import subprocess

RELEASE_CONFIG = {
    "csle-ryu": {
        "new_version": "'0.2.8'"
    },
    "csle-collector": {
        "new_version": "'0.2.8'"
    },
    "csle-common": {
        "new_version": "'0.2.8'"
    },
    "csle-attacker": {
        "new_version": "'0.2.8'"
    },
    "csle-defender": {
        "new_version": "'0.2.8'"
    },
    "csle-system-identification": {
        "new_version": "'0.2.8'"
    },
    "gym-csle-stopping-game": {
        "new_version": "'0.2.8'"
    },
    "gym-csle-intrusion-response-game": {
        "new_version": "'0.2.8'"
    },
    "csle-agents": {
        "new_version": "'0.2.8'"
    },
    "csle-rest-api": {
        "new_version": "'0.2.8'"
    },
    "csle-cli": {
        "new_version": "'0.2.8'"
    },
    "csle-cluster": {
        "new_version": "'0.2.8'"
    }
}

if __name__ == '__main__':
    username = input("Enter PyPi username: ")
    password = getpass()

    # Verify versions
    print("Verifying versions")
    for lib, versions in RELEASE_CONFIG.items():
        with io.open(f"{lib}/src/{lib.replace('-', '_')}/__version__.py", 'r', encoding='utf-8') as f:
            version = f.read().split("=")[-1].lstrip()
            versions["old_version"] = version
            if versions["old_version"] == versions["new_version"]:
                raise ValueError(f"Release with version {versions['old_version']} of {lib} already exists")

    # Update __version__.py files
    print("Updating __version__.py files")
    for lib, versions in RELEASE_CONFIG.items():
        print(f"Updating {lib} from version {versions['old_version']} to {versions['new_version']}")
        with io.open(f"{lib}/src/{lib.replace('-', '_')}/__version__.py", 'r', encoding='utf-8') as f:
            version_file_contents = f.read()
        with io.open(f"{lib}/src/{lib.replace('-', '_')}/__version__.py", 'w', encoding='utf-8') as f:
            version_file_contents = version_file_contents.replace(versions["old_version"], versions["new_version"])
            f.write(version_file_contents + "\n")

    for lib, versions in RELEASE_CONFIG.items():
        versions["old_version"] = versions["old_version"].replace("'", "").replace('"', "").replace("\n", '')
        versions["new_version"] = versions["new_version"].replace("'", "").replace('"', "").replace("\n", '')

    # Update requirements.txt files
    print("Updating requirements.txt files")
    for lib, versions in RELEASE_CONFIG.items():
        for lib2, versions2 in RELEASE_CONFIG.items():
            with io.open(f"{lib2}/requirements.txt", 'r', encoding='utf-8') as f:
                requirements_file_contents = f.read()
            with io.open(f"{lib2}/requirements.txt", 'w', encoding='utf-8') as f:
                requirements_file_contents = requirements_file_contents.replace(f"{lib}=={versions['old_version']}",
                                                                                f"{lib}=={versions['new_version']}")
                requirements_file_contents = requirements_file_contents.replace(f"{lib}>={versions['old_version']}",
                                                                                f"{lib}>={versions['new_version']}")
                requirements_file_contents = requirements_file_contents.replace(f"{lib}=>{versions['old_version']}",
                                                                                f"{lib}=>{versions['new_version']}")
                f.write(requirements_file_contents)

    # Update setup.cfg files
    print("Updating setup.cfg files")
    for lib, versions in RELEASE_CONFIG.items():
        for lib2, versions2 in RELEASE_CONFIG.items():
            with io.open(f"{lib2}/setup.cfg", 'r', encoding='utf-8') as f:
                setup_cfg_file_contents = f.read()
            with io.open(f"{lib2}/setup.cfg", 'w', encoding='utf-8') as f:
                setup_cfg_file_contents = setup_cfg_file_contents.replace(f"{lib}=={versions['old_version']}",
                                                                          f"{lib}=={versions['new_version']}")
                setup_cfg_file_contents = setup_cfg_file_contents.replace(f"{lib}>={versions['old_version']}",
                                                                          f"{lib}>={versions['new_version']}")
                setup_cfg_file_contents = setup_cfg_file_contents.replace(f"{lib}=>{versions['old_version']}",
                                                                          f"{lib}=>{versions['new_version']}")
                f.write(setup_cfg_file_contents)

    # Delete old build directories
    print("Delete old build directories")
    for lib, versions in RELEASE_CONFIG.items():
        shutil.rmtree(f"{lib}/dist", ignore_errors=True)

    # Build
    print("Build")
    for lib, versions in RELEASE_CONFIG.items():
        print(f"Building {lib}")
        p = subprocess.Popen(f"cd {lib}; python3 -m build", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        exit_code = p.wait()
        output = str(output)
        err = str(err)
        if exit_code == 0:
            print(f"{lib} built successfully")
        else:
            print(f"There was an error building {lib}; exit code: {exit_code}")
            print(output)
            print(err)

    # Push
    print("Push to PyPi")
    for lib, versions in RELEASE_CONFIG.items():
        print(f"Uploading {lib} to PyPi")
        p = subprocess.Popen(f"cd {lib}; python3 -m twine upload dist/* -p {password} -u {username}",
                             stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        exit_code = p.wait()
        output = str(output)
        err = str(err)
        if exit_code == 0:
            print(f"Successfully uploaded {lib} to PyPi")
        else:
            print(f"There was an error uploading {lib} to PyPi; exit code: {exit_code}")
            print(output)
            print(err)
