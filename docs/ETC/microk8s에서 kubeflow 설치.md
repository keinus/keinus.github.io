https://charmed-kubeflow.io/docs/quickstart

아래 명령으로 기본 애드온을 설치한다.

```
microk8s enable dns storage ingress metallb:10.64.140.43-10.64.140.49
```

juju를 설치한다.

```
sudo snap install juju --classic
```

juju 실행

```
juju bootstrap microk8s --agent-version="2.9.22"
```

kubeflow 모델을 추가한다.
```
juju add-model kubeflow
```

kubeflow 설치
```
juju deploy kubeflow --trust
```

설정
```
juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io
juju config dex-auth static-username=admin
juju config dex-auth static-password=admin
```
