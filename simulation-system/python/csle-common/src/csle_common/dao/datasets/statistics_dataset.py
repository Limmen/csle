from typing import Dict, Any


class StatisticsDataset:
    """
    DTO representing a dataset of statistics
    """

    def __init__(self, name: str, description: str, download_count: int, file_path: str, url: str, date_added,
                 num_measurements: int, num_metrics: int, size_in_gb: float, compressed_size_in_gb: float,
                 citation: str, num_files: int, file_format: str, added_by: str, conditions: str, metrics: str,
                 num_conditions: int):
        """
        Initializes the DTO

        :param name: the name of the dataset
        :param description: the description of the dataset
        :param download_count: the download count
        :param file_path: the file path to the dataset
        :param url: the url to the dataset
        :param date_added: the date the dataset was added
        :param num_measurements: the number of measurements
        :param num_metrics: the number of metrics for collecting the measurements
        :param size_in_gb: the size in gb of the dataset (uncompressed)
        :param compressed_size_in_gb: the size of the dataset in gb (compresse)
        :param citation: the citation information
        :param num_files: the number of files
        :param added_by: the name of the person that added the dataset
        :param conditions: the list of conditions considered for the statistics
        :param metrics: the list of metrics included in the statistics
        :param num_conditions: the number of conditions the statistics were collected for
        """
        self.name = name
        self.description = description
        self.download_count = download_count
        self.file_path = file_path
        self.url = url
        self.date_added = date_added
        self.num_measurements = num_measurements
        self.num_metrics = num_metrics
        self.size_in_gb = size_in_gb
        self.compressed_size_in_gb = compressed_size_in_gb
        self.citation = citation
        self.num_files = num_files
        self.file_format = file_format
        self.added_by = added_by
        self.conditions = conditions
        self.metrics = metrics
        self.num_conditions = num_conditions
        self.id = -1

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["description"] = self.description
        d["download_count"] = self.download_count
        d["file_path"] = self.file_path
        d["url"] = self.url
        d["date_added"] = self.date_added
        d["num_measurements"] = self.num_measurements
        d["num_metrics"] = self.num_metrics
        d["size_in_gb"] = self.size_in_gb
        d["compressed_size_in_gb"] = self.compressed_size_in_gb
        d["num_files"] = self.num_files
        d["citation"] = self.citation
        d["file_format"] = self.file_format
        d["added_by"] = self.added_by
        d["conditions"] = self.conditions
        d["metrics"] = self.metrics
        d["num_conditions"] = self.num_conditions
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StatisticsDataset":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StatisticsDataset(
            name=d["name"], description=d["description"], download_count=d["download_count"], file_path=d["file_path"],
            url=d["url"], date_added=d["date_added"], num_measurements=d["num_measurements"],
            num_metrics=d["num_metrics"], size_in_gb=d["size_in_gb"],
            compressed_size_in_gb=d["compressed_size_in_gb"], citation=d["citation"], num_files=d["num_files"],
            file_format=d["file_format"], added_by=d["added_by"], metrics=d["metrics"], conditions=d["conditions"],
            num_conditions=d["num_conditions"])
        if "id" in d:
            obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, description: {self.description}, download_count: {self.download_count}, " \
               f"file_path: {self.file_path}, url: {self.url}, date_added: {self.date_added}, " \
               f"num_measurements: {self.num_measurements}, " \
               f"num_metrisc: {self.num_metrics}," \
               f"size_in_gb: {self.size_in_gb}, compressed_size_in_gb: {self.compressed_size_in_gb}, " \
               f"citation: {self.citation}, num_files: {self.num_files}, " \
               f"file_format: {self.file_format}, added_by: {self.added_by}, metrics: {self.metrics}, " \
               f"conditions: {self.conditions}, num_conditions: {self.num_conditions}"

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
