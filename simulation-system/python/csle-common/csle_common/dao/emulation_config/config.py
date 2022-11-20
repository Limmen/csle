from typing import Dict, Any
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol


class Credential:
    """
    A DTO Class to represent a credential to a service of some component in the infrastructure
    """

    def __init__(self, management_admin_username_default: str, management_admin_password_default: str,
                 management_admin_first_name_default: str, management_admin_last_name_default: str,
                 management_admin_email_default: str, management_admin_organization_default: str,
                 management_guest_username_default: str, management_guest_password_default: str,
                 management_guest_first_name_default: str, management_guest_last_name_default: str,
                 management_guest_email_default: str, management_guest_organization_default: str,
                 ):

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Credential":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = Credential(username = d["username"], port = d["port"],
                         protocol=TransportProtocol._from_str(d["protocol"]), pw=d["pw"], service=d["service"],
                         root = d["root"])
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return "username:{},pw:{},port:{},protocol:{},service:{},root:{}".format(self.username, self.pw, self.port,
                                                                                 self.protocol, self.service, self.root)

    def __eq__(self, other) -> bool:
        """
        Tests equality

        :param other: the credential to test equality with
        :return: true if equal otherwise false
        """
        if not isinstance(other, Credential):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.username == other.username and self.pw == other.pw and self.service == other.service

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.username) + 31 * hash(self.pw)+ + 31 * hash(self.service)

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "Credential":
        """
        :return: a copy of the DTO
        """
        return Credential.from_dict(self.to_dict())

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        return 6

    @staticmethod
    def schema() -> "Credential":
        """
        :return: get the schema of the DTO
        """
        return Credential(username="", pw="", port=-1, protocol=TransportProtocol.TCP, service="", root=False)