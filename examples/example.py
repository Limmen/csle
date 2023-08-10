def _convert_gaussian_mixture_system_model_record_to_dto(gaussian_mixture_system_model_record) -> \
        GaussianMixtureSystemModel:
    """
    Converts a gaussian mixture system model record fetched from the metastore into a DTO

    :param gaussian_mixture_system_model_record: the record to convert
    :return: the DTO representing the record
    """
    gaussian_mixture_system_model_config_json = json.dumps(gaussian_mixture_system_model_record[1], indent=4,
                                                            sort_keys=True)
    gaussian_mixture_system_model_config: GaussianMixtureSystemModel = \
        GaussianMixtureSystemModel.from_dict(json.loads(gaussian_mixture_system_model_config_json))
    gaussian_mixture_system_model_config.id = gaussian_mixture_system_model_record[0]
    return gaussian_mixture_system_model_config

if __name__ == "__main__":
            """
        :return: A list of gaussian mixture system models in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: _convert_gaussian_mixture_system_model_record_to_dto(x),
                                   records))
                print(records)