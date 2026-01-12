docker is really a good tool to fast deploy, use and block a env

industry docker usage see: 
https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/engineer/how-to-use-docker/readme_en.md

find your needed env docker at dockerhub and use docker pull to get it

example:
docker run -it --name <container-name> --shm-size 16g --gpus all --network host -v <host-path>:<container-path> IMAGE

the core points:
1, -v <host-path>:<container-path>, share the path, reduce the dup cache
2, --network host, use network outside; or use -p <host-port>:<container-port> to reflect