# LINUXtips-giropops-senhas

## Objetivo geral
Criar e otimizar uma aplicação Kubernetes segura e eficiente, utilizando o projeto giropops-senhas como base. O foco está em práticas de segurança, eficiência de recursos, monitoramento e automação.

## Pré-requisitos
Para um correto funcionamento é preciso que as ferramentas já tenham sido instaladas
- **docker version 24.0.6+(Client e Server)**
```
apt-get update
apt-get install curl -y
curl -fsSL https://get.docker.com/ | bash
docker version
```
- **trivy version 0.47.0+**
```
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.47.0
trivy version
```
- **kind version 0.20.0+**
```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-$(uname)-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```
- **kubernetes version 1.28.2+**
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```
- **go 1.21.4+**
```
sudo su
wget https://go.dev/dl/go1.21.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.4.linux-amd64.tar.gz
echo export PATH=$PATH:/usr/local/go/bin >> $HOME/.bashrc
go version
```
- **kube-linter version development**
```
sudo su
go install golang.stackrox.io/kube-linter/cmd/kube-linter
cd go/bin
mv kube-linter /usr/local/go/bin/
cd ..
cd go/pkg
mv -r mod sumdb /usr/local/go/pkg/
kube-linter version
```
- **yamllint version 1.20.0+**
```
sudo apt-get install yamllint -y
yamllint --version
```
- **cosign version 2.2.1+**
```
curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
sudo chmod +x /usr/local/bin/cosign
```


## 1 - Preparação do projeto

### 1.1 - Fork do repositório
Realizar o fork do repositório https://github.com/badtuxx/giropops-senhas

### 1.2 - Estruturação do repositório
- **app.py**: arquivo principal da aplicação python
- **Dockerfile**: arquivo com as instruções para criação da imagen de container
- **LICENSE**: termo onde constam os detalhes de como o source code do projeto pode ser manipulado, divulgado e usado por terceiros
- **README.md**: arquivo contendo detalhes do projeto
- **requirements.txt**: dependências obrigatórias para o correto funcionamento da aplicação(ex: Flask, Redis e Prometheus) 
- **static**: pasta com os arquivos estáticos do projeto(ex: css, js e imagens)
- **templates**: pasta com os arquivos de layout/frontend(ex: html)
- **tailwind.config.js**: arquivo para exportação de módulos(ex: temas, plugins)
- **k8s**: pasta contendo os manifestos yaml(cluster, deployments e services)

## 2 - Desenvolvimento da imagem Docker

### 2.1 - Construção da imagen
> [!IMPORTANT]
> **O que é uma imagem?** No mundo de containers, imagens são formadas por camadas, onde dentro dessas camadas é possível encontrar todas as dependências, blibliotecas e arquivos necessários para criação do container

> [!IMPORTANT]
> **O que é um container?** É um processo isolado do sistema operacional onde utiliza recursos como cgroups, namespaces e chroot para provisionamento de seus processos. Todo container é derivado de uma imagem, ou seja, sua origem tem como base uma imagem.

### 2.2 - Otimização de imagens
> [!TIP]
> **O que é o multistage build?** É uma técnica usada para realizar o build de imagens separados em fases dentro do Dockerfile visando criar imagens menores, otimizadas e sem dependências ou arquivos desnecessários

> [!TIP]
> **O que é distroless?** Distroless é uma filosofia ou abordagem no mundo de containers onde é possível deixar as imagens somente com uma camada(apko) otimizando assim o tempo de execução do container e deixando-o mais seguro devido possuírem somente o necessário(sem gerenciador de pacotes ou shell) o que torna diferente de uma distribuição Linux.

> [!NOTE]
> **Chainguard, já ouviu falar?** Empresas como Chainguard e Google se destacam nesse contexto por serem grandes provedores desse modelo(distroless) de imagem de container. Como exemplo, podemos citar o Wolfi OS mantido pela Chainguard que é uma undistro(sem distribuição), ou seja, usa a filosofia distroless com um modelo minimalista projetado para ambientes em containers contendo somente os recursos necessários para seu funcionamento.

Os comandos abaixo irão gerar imagens distroless com multistage build deixando-as mais otimizadas, com um tamanho menor que imagens convencionais e sem vulnerabilidades, além de fazer o push para o Dockerhub

Build e push da image do giropops-senhas ao Dockerhub
```
docker image build --no-cache -f Dockerfile-app.yaml -t reysonbarros/giropops-senhas:1.0 .
docker login
docker image push reysonbarros/giropops-senhas:1.0
```

Build e push da image do giropops-redis ao Dockerhub
```
docker image build --no-cache -f Dockerfile-redis.yaml -t reysonbarros/giropops-redis:7.2.3 .
docker login
docker image push reysonbarros/giropops-redis:7.2.3
```

![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/57e9604b-d00f-499d-b932-0f866090e043)

## 3 - Configuração do Kubernetes

### 3.1 - Verificação de segurança
> [!WARNING]
> **O que é o trivy?** É uma ferramenta para scan de vulnerabilidades em containers.
Comando executado no trivy para realizar a análise de vulnerabilidades em imagens:
```
trivy image reysonbarros/giropops-senhas:1.0
trivy image reysonbarros/giropops-redis:7.2.3

```

![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/f96b3ec3-3043-46f5-99d5-d4e1cd1af859)

![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/bdb8cdb6-2741-42e7-b66f-d9ed9f8ca2d2)


### 3.2 - Manifestos YAML
> [!IMPORTANT]
> **O que é um cluster?** Conjunto de 1 ou mais nodes dentro de uma rede

> [!IMPORTANT]
> **O que é um Pod?** Agrupamento com 1 ou mais containers compartilhando o mesmo namespace

> [!IMPORTANT]
> **O que é um Deployment?** É um objeto no Kubernetes que permite gerenciar um conjunto de Pods identificados por uma label

> [!IMPORTANT]
> **O que é um Service?** Um objeto que permite expor uma aplicação para o mundo externo

> [!IMPORTANT]
> **O que é um StatefulSet?** São objetos que servem para que possa criar aplicações que precisam manter a identidade do Pod e persistir dados em volumes locais

> [!IMPORTANT]
> Acessar a pasta k8s para executar os próximos comandos

cd k8s/

Criação do Cluster giropops com 1 node control-plane e 3 nodes workers
```
kind create cluster --config cluster.yaml
```
Criação do Namespace dev
```
kubectl apply -f dev-namespace.yaml
```
Criação do ConfigMap para o redis
```
kubectl apply -f redis-configmap.yaml -n dev
```
Criação do StatefulSet para o redis
```
kubectl apply -f redis-statefulset.yaml -n dev
```
Criação do Service para o redis
```
kubectl apply -f redis-headless-svc.yaml -n dev
```
Criação do Deployment para a aplicação giropops-senhas
```
kubectl apply -f giropops-senhas-deployment.yaml -n dev
```
Criação do Service para a aplicação giropops-senhas
```
kubectl apply -f giropops-senhas-svc.yaml -n dev
```
Listagem dos Pods
```
kubectl get pods -n dev
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/e3b01f17-a0bb-45b2-94c6-2b74f5f5dd40)

Listagem dos Services
```
kubectl get services -n dev
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/731d8a2d-87bb-4488-ae04-1a83f869d031)

Listagem do Persistent Volume Claim
```
kubectl get pvc -n dev
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/8caf66b1-db5d-427e-8290-66e9d2695231)


Listagem do Persistent Volume
```
kubectl get pv -n dev
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/4763f172-1d33-4f2d-8e83-c387cd8f9981)


Teste interno(dentro do cluster) de comunicação entre os pods do giropops-senhas e redis
```
k exec -it giropops-senhas-954766894-cfm6v -n dev -- python
>>> import redis
>>> import os
>>> redis_host = os.environ.get('REDIS_HOST')
>>> redis_password = os.environ.get('REDIS_PASSWORD')
>>> redis_port = 6379
>>> r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
>>> r.ping()
>>> print('connected to redis "{}"'.format(redis_host))
```
Testando a aplicação via browser
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/acb5e385-eb2b-498a-9e7e-9ac8b2118c33)

> [!NOTE]
> Para acessar a aplicação utilizar um dos IPs da coluna INTERNAL-IP dos nodes
```
k get nodes -o wide
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/5793825f-1d60-4382-b26d-aaaafd0703fa)


Porta 32000 mapeada para os nodes no serviço giropops-senhas
```
k get svc -n dev
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/809143e0-f11c-4640-88b4-8f258cd234a2)

### 3.3 - Práticas recomendadas
> [!IMPORTANT]
> **O que são probes?** Probe significa sondar, examinar algo. As probes são uma forma de você monitorar o seu Pod e saber se ele está em um estado saudável ou não

> [!IMPORTANT]
> **O que é uma livenessProbe?** A livenessProbe é a nossa probe de verificação de integridade, o que ela faz é verificar se o que está rodando dentro do Pod está saudável. O que fazemos é criar uma forma de testar se o que temos dentro do Pod está respondendo conforme esperado. Se por acaso o teste falhar, o Pod será reiniciado

> [!IMPORTANT]
> **O que é uma readinessProbe?** A readinessProbe é uma forma de o Kubernetes verificar se o seu container está pronto para receber tráfego, se ele está pronto para receber requisições externas

> [!IMPORTANT]
> **O que é uma startupProbe?** A startupProbe é uma forma de o Kubernetes verificar se o seu container está pronto para receber tráfego, se ele está pronto para receber requisições externas

> [!IMPORTANT]
> **O que é são limites de recursos no K8S?** Limitação de recursos é uma forma de garantirmos os limites máximo e mínimo de cpu e memória que um container deve utilizar em seu ciclo de vida

Nesse projeto, as probes e limites de recursos foram implementados no deployment do giropops-senhas e no statefulset do redis seguindo as boas práticas de monitoramento, estabilidade e eficiência

### 3.4 - Linting de YAML
> [!IMPORTANT]
> **O que é linter?** Lint ou linter é uma ferramenta que realiza uma varredura sobre código estático na tentativa de identificar possíveis bugs e falhas/erros de programação. Um linter é responsável por capturar erros nos dados antes que sejam processados. Dessa forma, isso economiza tempo em análises de erros durante operações de alta robustez e criticidade

> [!IMPORTANT]
> **O que é o kube-linter?** KubeLinter analisa arquivos YAML do Kubernetes e Helm charts para validar se está correspondendo com as melhores práticas com foco na segurança

> [!IMPORTANT]
> **O que é o yamllint?** yamllint não verifica somente a validade de sintaxe, mas também analisa outros aspectos de código, como por exemplo espaços em branco e identação

Exemplo de análise com yamllint
```
yamllint .
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/b42997b7-403b-42a6-b020-779f6918a5b3)

Exemplo de análise com kube-linter
```
kube-linter lint .
```
![image](https://github.com/reysonbarros/LINUXtips-giropops-senhas/assets/4474192/22199ab2-d8b3-4b3a-987e-6189e0faaf10)

## 4 - Segurança e assinatura da imagem com Cosign

### 4.1 - Assinatura com Cosign
> [!IMPORTANT]
> **O que é o cosign?** Utilitário de linha de comando que serve para assinar imagem de container além de validar a assinatura e é mantido pela Linux Foundation sobre o projeto open source Sigstore

> [!TIP]
> **A imagem precisa estar no registry(público/privado, nesse caso no dockerhub) para conseguir assinar/verificar.**

Gerar o par de chaves para as imagens do giropops-senhas e do giropops-redis
```
cosign generate-key-pair --output-key-prefix giropops-senhas
cosign generate-key-pair --output-key-prefix giropops-redis
```

Assinar a imagem do giropops-senhas e do giropops-redis
```
cosign sign --key giropops-senhas.key reysonbarros/giropops-senhas:1.0
cosign sign --key giropops-redis.key reysonbarros/giropops-redis:7.2.3
```

Validar a assinatura da imagem do giropops-senhas e do giropops-redis
```
cosign verify --key giropops-senhas.pub reysonbarros/giropops-senhas:1.0
cosign verify --key giropops-redis.pub reysonbarros/giropops-redis:7.2.3
```

## 5 - Monitoramento com Prometheus

> [!IMPORTANT]
> **O que é o Prometheus?** É uma ferramenta open-source que serve para monitoramento e alerta de todos os componentes do cluster Kubernetes, como por exemplo: kube-scheduler, kube-controller-manager, kubelet, kube-proxy, etc

> [!IMPORTANT]
> **O que é o Grafana?** Grafana é um sistema que permite realizar consultas, visualizar e receber alertas, além de explorar métricas e logs através de dashboards de tudo que for possível coletar

> [!IMPORTANT]
> **O que é o AlertManager?** AlertManager intercepta alertas enviados por aplicações clientes como por exemplo o servidor Prometheus, além de agrupar e rotear esses alertas para seu devido destino

> [!IMPORTANT]
> **O que é o ServiceMonitor?** É uma funcionalidade do Prometheus Operator onde é possível configurá-lo para monitorar um ou mais serviços

### 5.1 - Configuração com Prometheus

Instalação dos CRDs(Custom Resource Definitions) do Kube-Prometheus
```
git clone https://github.com/prometheus-operator/kube-prometheus
cd kube-prometheus
kubectl create -f manifests/setup
```

Instalação do Prometheus, AlertManager e Grafana
```
kubectl apply -f manifests/
```
Validar se a instalação dos servicemonitors e pods do namespace monitoring foi concluída
```
kubectl get servicemonitors -n monitoring
kubectl get pods -n monitoring
```
> [!WARNING]
> Continuar com os próximos passos somente quando os pods estiverem com status READY

Instalação do ClusterRole, ServiceMonitor e PodMonitor referente ao giropops-senhas
```
kubectl apply -f cluster-role.yaml
giropops-senhas-service-monitor.yaml
giropops-senhas-pod-monitor.yaml
```

Validar se a instalação dos serviceMonitors e podMonitors referente ao giropops-senhas foi concluída
```
kubectl get servicemonitors -n dev
kubectl get podmonitors -n dev
```

Mapeamento das portas do Grafana, Prometheus e AlertManager para acesso localhost via port-forward
```
kubectl port-forward -n monitoring svc/grafana 33000:3000
kubectl port-forward -n monitoring svc/prometheus-k8s 39090:9090
kubectl port-forward -n monitoring svc/alertmanager-main 39093:9093
```

Abrir o browser e acessar:

Grafana(user e password = admin) - http://localhost:33000

Prometheus - http://localhost:39090

AlertManager - http://localhost:39093


### Referências
https://www.josehisse.dev/blog/aumentando-disponibilidade-com-inter-pod-anti-affinity

https://github.com/kubernetes-sigs/kind/releases

https://medium.com/@pushkarjoshi0410/assigning-pods-to-nodes-using-affinity-and-anti-affinity-df18377244b9
