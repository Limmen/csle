import csle_rest_api.rest_api as rest_api

if __name__ == '__main__':
    static_folder_path = "../../../../management-system/csle-mgmt-webapp/build"
    rest_api.start_server(static_folder=static_folder_path, port=7777, num_threads=100, host="0.0.0.0", https=False)