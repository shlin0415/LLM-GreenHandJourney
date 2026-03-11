
(base) root@zzz:~# docker pull modelbest-registry.cn-beijing.cr.aliyuncs.com/public/soar-toolkit:latest
latest: Pulling from public/soar-toolkit
7f7602a82106: Pull complete
2fd29ef2cfeb: Pull complete
0d009e49c2e9: Pull complete
bc94a9448b8d: Pull complete
e87500e69896: Pull complete
da6dc683e975: Pull complete
78c122654f0d: Pull complete
15a17189b2df: Pull complete
02cb0e091e33: Pull complete
d283c9a464b6: Pull complete
de048ed20f1f: Pull complete
644e9b203583: Pull complete
9c3d619183d2: Pull complete
5a2aba542b08: Pull complete
02559cd4bc8d: Pull complete
6e8af4fd0a07: Pull complete
2cd52cbb1ebe: Pull complete
6cb9b761b877: Pull complete
d95b4faf644c: Pull complete
Digest: sha256:1add7d7752281f3fe3868568e50fe49abd1286183cc57a636862c8e67b1e21de
Status: Downloaded newer image for modelbest-registry.cn-beijing.cr.aliyuncs.com/public/soar-toolkit:latest
modelbest-registry.cn-beijing.cr.aliyuncs.com/public/soar-toolkit:latest
(base) root@zzz:~#
(base) root@zzz:~#
(base) root@zzz:~#
(base) root@zzz:~# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(base) root@zzz:~# docker images
REPOSITORY                                                          TAG       IMAGE ID       CREATED       SIZE
modelbest-registry.cn-beijing.cr.aliyuncs.com/public/soar-toolkit   latest    1add7d775228   13 days ago   37.2GB

pull the docker on win wsl 16gb gpu 32gb cpu, which use 98% cpu memory and almost crash my pc, docker on linux seem break so.

for docker engine setting,
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "max-concurrent-downloads": 1,
  "max-concurrent-uploads": 1
}

.wslconfig
[wsl2]
memory=24GB
localhostForwarding=true
swap=30GB
processors=8

A 37.2GB image is massive—it likely contains the full CUDA Toolkit, multiple versions of Torch, and potentially some pre-compiled backends. Running this on 32GB of RAM with WSL is risky because WSL's memory management (vmmem) tends to be aggressive.

docker run --rm \
  --memory="4g" \
  --entrypoint /bin/bash \
  modelbest-registry.cn-beijing.cr.aliyuncs.com/public/soar-toolkit:latest \
  -c "
echo '--- OS INFO ---'
cat /etc/os-release | grep PRETTY_NAME
echo ''
echo '--- PYTHON VERSION ---'
python3 --version
echo ''
echo '--- CUDA VERSION ---'
nvcc --version || echo 'NVCC not in PATH'
echo ''
echo '--- SGLANG LOCATION ---'
python3 -c 'import sglang; print(sglang.__file__)'
echo ''
echo '--- COMPONENT VERSIONS ---'
pip list | grep -E 'torch|sglang|triton|flashinfer|transformer-engine|vllm|flash-attn'
echo ''
echo '--- ENV VARIABLES ---'
env | grep -E 'CUDA|PATH|LD_LIBRARY_PATH'
" > soar_env_report.txt

