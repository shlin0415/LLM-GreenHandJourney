# setting conda when vpn
conda config --set proxy_servers.http http://127.0.0.1:7890
conda config --set proxy_servers.https http://127.0.0.1:7890
conda config --set ssl_verify False