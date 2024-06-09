---
layout: default
title: WSL2 Portforwarding을 위한 NGINX Reverse Proxy 자동화
nav_order: 1
parent: WSL2
---

# WSL2 Portforwarding을 위한 NGINX Reverse Proxy 자동화
WSL2로 내부 인스턴스를 띄우면 해당 인스턴스는 hyper-v 스위치 중 WSL용 internal switch에 연결되어 private ip 대역을 할당 받게 된다.  
wsl2의 내부 인스턴스를 외부에서 접근하고 싶어서 위 스위치를 bridge 모드로 physical nic에 연결도 해봤는데 제대로 안되는 느낌이 들어 포기했다.(불안정하다. 되다가 안되다가..)  
최종적으로 윈도우즈에서 nginx를 실행하고 내부 wsl2 인스턴스를 reverse proxy로 연결하는 방법으로 해결했다.  
서비스에 올려서 완전 자동화하는 방법(powershell 스크립트를 사용하여 내부 방화벽 설정으로 port forwarding하는 방법)이 더 깔끔한데  
방화벽 건들기 싫어서, 포워딩 실행/중지를 간단하게 하고 싶어서 아래와 같은 python 스크립트를 구현하여 사용하고 있다.  

## 설치
적당한 위치에 nginx를 다운로드 받고 압축을 푼다.  
아래 스크립트를 nginx 폴더 아래에 작성한다.  
참고로, 아래 스크립트는 개인적인 용도로 사용하려 만든거라 범용성이나 에러처리가 아예 안되어 있으니 추후 사용 시 확인하여 디버깅 후 사용해야 한다.  


```python
import subprocess
import sys
import multiprocessing


# wsl default 인스턴스에서 hostname -I로 출력한 IP 중 제일 앞에 있는 IP를 가져온다.  
# hostname -I의 출력 순서를 모르겠는데 대부분 외부 연결된 IP(라우팅 테이블에서 gateway와 연결된 인터페이스의 IP)가 출력되고 있기 때문에 그냥 쓴다.
# 만약 정확성을 기하고 싶다면 위에서 출력한 ip와 "ip route"로 출력한 리스트 중 dev eth0의 IP를 비교하여 b클래스까지 동일한 IP가 있으면 그게 인터페이스 IP이니 그걸 쓰도록 아래 코드를 수정하면 된다.
def get_wsl2_ip() -> str|None:
    try:
        result = subprocess.run(["wsl", "hostname", "-I"], capture_output=True)
        result.check_returncode()
        output = result.stdout.decode("utf-8").strip()
        return output.split()[0]
    except subprocess.CalledProcessError as e:
        print(f"Error getting WSL2 IP: {e}")
        return None

# Nginx 설정 파일 자동 생성
# 20022:22, 11434:11434, 20080:8080 3개 규칙을 작성했다.  
# 예시 파일 수정한거라 이상한것도 있을테니 수정해서 사용할 것.
# internal_ip에 위 get_wsl2_ip에서 얻은 ip를 입력한다.
def generate_nginx_config(internal_ip: str) -> None:
    with open("./conf/nginx.conf", "w") as f:
        f.write("""
worker_processes  1;
events {
}
stream {
    # target
    upstream ssh {
        server """ + internal_ip + """:22;
    }
    upstream ollama {
        server """ + internal_ip + """:11434;
    }
    upstream webui {
        server """ + internal_ip + """:8080;
    }

    # tcp
    server {
        listen 20022;
        proxy_pass ssh;
        proxy_connect_timeout 1s;
    }
    server {
        listen 11434;
        proxy_pass ollama;
        proxy_connect_timeout 1s;
    }
    server {
        listen 20080;
        proxy_pass webui;
        proxy_connect_timeout 1s;
    }
}
""")

# windows의 tasklist 명령으로 proc 프로세스의 실행된 pid를 전부 찾아서 리턴한다.
def get_process_id_for_windows(proc: str):
    process = subprocess.Popen(["tasklist", "/FI", f"imagename eq {proc}"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    spl = output.decode("cp949").split()
    if len(spl) < 13:
        return []
    spl = spl[13:]
    index = 0
    pids = []
    for item in spl:
        if index % 6 == 1:
            pids.append(item)
        index += 1
    return pids

# nginx 실행 or kill
def main(action):
    process = "nginx.exe"
    if action == "start":
        # Nginx 프로세스 확인
        if len(get_process_id_for_windows(process)) > 1:
            print("Nginx is already running.")
        else:
            # Nginx 실행
            generate_nginx_config(get_wsl2_ip())
            process = subprocess.Popen([process], stdout=subprocess.PIPE)
            print("Nginx started successfully.")

    elif action == "stop":
        # Nginx 프로세스 ID 확인
        pids = get_process_id_for_windows(process)
        if len(pids) < 1:
            print("Nginx is not running.")
        else:
            for pid in pids:
                subprocess.call(["taskkill", "/F", "/PID", str(pid)])
            print("Nginx terminated successfully.")
    else:
        print(f"Invalid action: {action}")

if __name__ == "__main__":
    # 인자값 확인
    if len(sys.argv) != 2 or sys.argv[1] not in ["start", "stop"]:
        print("Usage: python nginx_manager.py [start|stop]")
        sys.exit(1)

    action = sys.argv[1]
    main(action)
```

port forwarding이 필요할 때 마다 위 스크립트를 실행하면 된다.  
추가적은 포트가 필요하거나 기타  설정이 필요할 경우 generate_nginx_config()의 내부 설정 스트링을 수정하여 사용한다.  
