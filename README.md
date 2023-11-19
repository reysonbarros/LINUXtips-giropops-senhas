# LINUXtips-giropops-senhas

### Objetivo geral
Criar e otimizar uma aplicação Kubernetes segura e eficiente, utilizando o projeto giropops-senhas como base. O foco está em práticas de segurança, eficiência de recursos, monitoramento e automação.

## 1 - Preparação do projeto

### 1.1 - Estruturação do repositório
TODO: Adicionar print da estrutura de arquivos ao finalizar o projeto
- **app.py**: arquivo principal da aplicação python
- **Dockerfile**: arquivo com as instruções para criação das imagens de container
- **LICENSE**: termo onde constam os detalhes de como o source code do projeto pode ser manipulado, divulgado e usado por terceiros
- **README.md**: arquivo contendo detalhes do projeto
- **requirements.txt**: dependências obrigatórias para o correto funcionamento da aplicação(ex: Flask, Redis e Prometheus) 
- **static**: pasta com os arquivos estáticos do projeto(ex: css, js e imagens)
- **templates**: pasta com os arquivos de layout/frontend(ex: html)
- **tailwind.config.js**: arquivo para exportação de módulos(ex: temas, plugins)

### 1.2 - Construção das imagens
> [!IMPORTANT]
> **O que é uma imagem?** No mundo de containers, imagens são formadas por camadas, onde dentro dessas camadas é possível encontrar todas as dependências, blibliotecas e arquivos necessários para criação do container

> [!IMPORTANT]
> **O que é um container?** É um processo isolado do sistema operacional onde utiliza recursos como cgroups, namespaces e chroot para provisionamento de seus processos. Todo container é derivado de uma imagem, ou seja, sua origem tem como base uma imagem.

Executando o comando abaixo construiremos uma imagem do projeto giropops-senhas focando em sua leveza e livre de vulnerabilidades
```
docker image build -f Dockerfile-python-3-11-4-alpine3-18 -t giropops-senhas:1.0 .
```
TODO: Adicionar print da imagem gerada(docker image ls | grep giropops-senhas:1.0)


### 1.3 - Otimização de imagens
> [!TIP]
> **O que é o multistage build?** É uma técnica usada para realizar o build de imagens separados em fases dentro do Dockerfile visando criar imagens menores, otimizadas e sem dependências ou arquivos desnecessários

> [!TIP]
> **O que é distroless?** Distroless é uma filosofia ou abordagem no mundo de containers onde é possível deixar as imagens somente com uma camada(apko) otimizando assim o tempo de execução do container e deixando-o mais seguro devido possuírem somente o necessário(sem gerenciador de pacotes ou shell) o que torna diferente de uma distribuição Linux.

> [!NOTE]
> **Chainguard, já ouviu falar?** Empresas como Chainguard e Google se destacam nesse contexto por serem grandes provedores desse modelo(distroless) de imagem de container. Como exemplo, podemos citar o Wolfi OS mantido pela Chainguard que é uma undistro(sem distribuição), ou seja, usa a filosofia distroless com um modelo minimalista projetado para ambientes em containers contendo somente os recursos necessários para seu funcionamento.

O comando abaixo irá gerar uma imagem distroless com multistage build deixando-a mais otimizada, menor que a versão anterior(1.0) e sem vulnerabilidades
```
docker image build -f Dockerfile-multistage-chainguard-python-latest -t giropops-senhas:2.0 .
```


### 1.4 - Verificação de segurança
A definir

### 1.5 - Manifestos YAML
A definir

### 1.6 - Práticas recomendadas
A definir

### 1.7 - Linting de YAML
A definir




