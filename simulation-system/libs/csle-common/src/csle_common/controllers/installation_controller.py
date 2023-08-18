import subprocess
import sys


class InstallationController:
    """
    Controller managing installation of CSLE
    """

    @staticmethod
    def install_all_emulations() -> None:
        """
        Installs all emulations in the metastore

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/envs/ && make install"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_emulation(emulation_name: str) -> None:
        """
        Installs a given emulation in the metastore

        :param emulation_name: the name of the emulation to install

        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/envs/ && make install_{emulation_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_emulation(emulation_name: str) -> None:
        """
        Uninstalls a given emulation in the metastore

        :param emulation_name: the name of the emulation to uninstall

        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/envs/ && make uninstall_{emulation_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("stdout is None")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_all_emulations() -> None:
        """
        Uninstalls all emulations from the metastoer

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/envs/ && make uninstall"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_all_simulations() -> None:
        """
        Installs all simulations in the metastore

        :return: None
        """
        cmd = "cd $CSLE_HOME/simulation-system/envs/ && make install"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("stdout is None")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_simulation(simulation_name: str) -> None:
        """
        Installs a given simulation in the metastore

        :param simulation_name: the name of the simulation to uninstall
        :return: None
        """
        cmd = f"cd $CSLE_HOME/simulation-system/envs/ && make install_{simulation_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_simulation(simulation_name: str) -> None:
        """
        Uninstalls a given simulation in the metastore

        :param simulation_name: the name of the simulation to install
        :return: None
        """
        cmd = f"cd $CSLE_HOME/simulation-system/envs/ && make uninstall_{simulation_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_all_simulations() -> None:
        """
        Uninstalls all simulations from the metastore

        :return: None
        """
        cmd = "cd $CSLE_HOME/simulation-system/envs/ && make uninstall"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_derived_images() -> None:
        """
        Installs all derived Docker images

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/derived_images/ && make build"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_derived_image(image_name: str) -> None:
        """
        Installs a given derived Docker image

        :param image_name: the name of the image to install
        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/derived_images/ && make {image_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_derived_images() -> None:
        """
        Uninstalls all derived Docker images

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/derived_images/ && make rm_image"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_derived_image(image_name: str) -> None:
        """
        Uninstalls a given derived Docker image

        :param image_name: the name of the image to uninstall
        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/derived_images/ && make rm_{image_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_base_images() -> None:
        """
        Installs all base Docker images

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/base_images/ && make build"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_base_image(image_name: str) -> None:
        """
        Installs a given base Docker image

        :param image_name: the name of the image to install
        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/base_images/ && make {image_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_base_images() -> None:
        """
        Uninstalls all base Docker images

        :return: None
        """
        cmd = "cd $CSLE_HOME/emulation-system/base_images/ && make rm_image"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_base_image(image_name: str) -> None:
        """
        Uninstalls a given base Docker image

        :param image_name: the name of the image to uninstall
        :return: None
        """
        cmd = f"cd $CSLE_HOME/emulation-system/base_images/ && make rm_{image_name}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def uninstall_metastore() -> None:
        """
        Uninstalls the metastore

        :return: None
        """
        cmd = "cd $CSLE_HOME/metastore/ && make clean"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

    @staticmethod
    def install_metastore() -> None:
        """
        Installs the metastore

        :return: None
        """
        cmd = "cd $CSLE_HOME/metastore/ && make build"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to None type")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()
