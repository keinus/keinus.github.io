---
layout: default
title: onedev
nav_order: 1
parent: onedev
---
                

# Onedev
개인 프로젝트의 형상관리를 위해 사용하던 YONA 프로젝트가 소스코드 관리와 이슈 관리, 게시판 등의 기능을 사용하기 좋아서 잘 썼었으나 기능 부족 등의 이유로 gitlab으로 이전했다.  
문제는 gitlab이 개인용으로 사용하기에는 너무 무겁다는게 문제였다.  
개인용 nas에서 운용하기에는 sidekiq 프로세스가 너무 많이 뜨고 램도 많이 쳐묵으시는 바람에 다른 솔루션을 많이 알아봤으나 YONA만큼 괜찮은게 안 보였었다.  
그래서 다시 YONA로 이전할까 고민중에 geeknews에서 onedev를 소개하는 글을 보고 시험삼아 설치/운용해보려 한다.  
java로 구현되어 있으며 mysql 계열 DB를 내부에서 사용하고 있는듯 한데 개인용이니 외부 DB는 배제하고 하나의 컨테이너로만 사용하려 한다.

## 설치
OneDev의 아래 사이트에서 참조하여 docker-compose를 작성했다.

[OneDev Run As Docker](https://docs.onedev.io/installation-guide/run-as-docker-container)

아래는 docker-compose 파일이다.

```yaml
services:
  onedev:
    image: 1dev/server
    container_name: onedev
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - onedev-data:/opt/onedev
    ports:
      - 6610:6610
      - 6611:6611



volumes:
  onedev-data: {}
```

## 초기 설정
`http://<Server IP>:6610/~init`로 접속하면 아래와 같은 화면이 나온다.

![alt text](images/image.png)

적당히 입력해주자.  

</br>

다음으로 서버 URL을 입력하라는 아래와 같은 화면이 나온다.

![alt text](images/image-1.png)

IP 주소 또는 도메인 이름으로 입력해주자.  

![alt text](images/image-2.png)

설치가 끝났다.

## 프로젝트 migration
내 기존 프로젝트는 Gitlab에 있었다.  
이 프로젝트를 전부 이전해야하는데, 스크립트로 만드는 방법이 있고 아래와 같이 GUI에서 이전하는 방법도 있다.  
API로 이전하기로 한다.  

### gitlab 프로젝트 백업
아래 스크립트를 실행하여 백업을 실행한다.  
dependency는 아래와 같다.
1. python-gitlab
2. GitPython

두 패키지를 설치하고 gitlab에서 계정의 API 키를 생성한다. 키의 권한은 API 권한을 부여한다.  
아래 코드에 위에서 부여받은 API 토큰, HOST IP, PORT, ID, PW를 추가한다.


```python
import os
import gitlab
from git import Repo


GITLAB_TOKEN = "<GITLAB_API_TOKEN>" # "glpat-F6YufVUeNkiPza7ytwN9"
HOST = '<GITLAB_HOST_IP:PORT>'
username = "<GITLAB_ID>"
password = "<GITLAB_PASSWORD>"

gl = gitlab.Gitlab(url=f'https://{HOST}', private_token=GITLAB_TOKEN, ssl_verify=False)

gitBasePathRelativeAbsolut = os.path.expanduser("./backup/")
os.makedirs(gitBasePathRelativeAbsolut, exist_ok=True)

for p in gl.projects.list(all=True):
    print("Cloning project " + p.name)
    pathToFolder = f"{gitBasePathRelativeAbsolut}{p.path_with_namespace}"
    if not os.path.exists(pathToFolder):
        print("\tCreating directory for project " + pathToFolder)
        os.makedirs(pathToFolder)
        remote = f"https://{username}:{password}@{HOST}/{p.path_with_namespace}.git"
        Repo.clone_from(remote, pathToFolder)
```

### OneDev upload
gitlab으로 백업 받은 디렉토리명을 ./backup 으로 설정한다. 다른 디렉토리 쓰고 싶으면 위 코드에서 수정한다.  
아래 코드에서 <>로 되어 있는 부분을 수정하여 실행한다.  
gitlab에서 namespace는 onedev에 프로젝트로 생성하고, gitlab의 namespace의 하위 프로젝트들을 onedev에서 생성한 프로젝트의 하위 프로젝트로 push하였다.  



```python
import os
from git import Repo
import requests


ONEDEV_HOST = '<ONEDEV_HOST_IP:PORT>'
username = "<ONEDEV_ID>"
password = "<ONEDEV_PASSWORD>"

ONEDEV_URL = f'http://{username}:{password}@{ONEDEV_HOST}'
BACKUP_DIR = "./backup"
COUNT = 100     # 프로젝트 개수

response: requests.Response = requests.get(f'{ONEDEV_URL}/~api/projects?offset=0&count={COUNT}')
onedev_projects: list = [item['name'] for item in response.json()]
folders: list = os.listdir(BACKUP_DIR)

for namespace in os.listdir(BACKUP_DIR):
    if namespace not in onedev_projects:
        response = requests.post(
            url = ONEDEV_HOST+'/~api/projects', 
            json = {
                "name" : namespace,
                "codeManagement" : True ,
                "packManagement" : True ,
                "issueManagement" : True ,
                "timeTracking" : False ,
                "pendingDelete" : False
            }
        )
        if response.status_code != 200:
            raise Exception("can't not create project.")
        namespace_id = response.json()
    for project_name in os.listdir(f'{BACKUP_DIR}/{namespace}'):
        if project_name not in onedev_projects:
            response = requests.post(
                url = ONEDEV_HOST+'/~api/projects', 
                json = {
                    "parentId" : namespace_id,
                    "name" : project_name ,
                    "codeManagement" : True ,
                    "packManagement" : True ,
                    "issueManagement" : True ,
                    "timeTracking" : False ,
                    "pendingDelete" : False
                }
            )
            if response.status_code != 200:
                raise Exception("can't not create project.")
        repo: Repo = Repo(f"{BACKUP_DIR}/{namespace}/{project_name}")
        repo.delete_remote('origin')
        remote = repo.create_remote("origin", f"{ONEDEV_HOST}/{namespace}/{project_name}")
        remote.push(refspec='main')
```

## 총평
일단 Gitlab보다 UI가 정돈된 느낌이 없다.  
모든 창에 검색 쿼리 박스를 넣어놔서 검색으로 해결하세요라는 느낌인데 개인용으로 쓰기엔 검색이나 기타 방법보단 디렉토리 방식이 더 좋아서 맘에 안든다.  
그렇다고 대규모로 쓰기엔 gitlab의 기능들을 따라가진 못 하는듯 싶고...  
빌드 스크립트나 패키지 관리자를 넣어놔서 간단히 쓰기엔 gitlab보단 편할거 같긴 한데 아직 잘 써보진 못해서 좀 시간이 필요할듯 하다.  
그래도 gitlab보단 램 덜 처묵하고 cpu도 덜 먹고 여러모로 경량화된거 같아 좋다.  
