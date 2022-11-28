import csle_rest_api.rest_api as rest_api

if __name__ == '__main__':
    static_folder_path = "../../../../../management-system/csle-mgmt-webapp/build"
    app_path = "../../../../../management-system/csle-mgmt-webapp/server/server.py"
    rest_api.start_server(static_folder=static_folder_path, port=7777, num_threads=100, host="0.0.0.0", https=False)