import csle_rest_api.rest_api_proxy as rest_api_proxy

if __name__ == '__main__':
    static_folder_path = "../../../../management-system/csle-mgmt-webapp/build"
    proxy_server = 'http://172.31.212.92:7777/'
    rest_api_proxy.start_proxy_server(static_folder=static_folder_path, port=7777, num_threads=100, host="0.0.0.0",
                                      proxy_server=proxy_server, https=False)