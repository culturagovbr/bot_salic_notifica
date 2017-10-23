# bot_salic_pojetoaprovado_notifica

O bot_salic_projetoaprovado_notifica tem o objetivo de criar canal de notificações automaticas de novos projetos aprovados na lei Ruanet utilizando a api de informações abertas do sistema salic.

## Requisitos

* Python3
* PIP
* python3-virtualenv
* SQlite

As dependencias de pacotes estão no requirements.txt

## Usando Docker

Você precisa ter instalado o Docker para executar os procedimentos abaixo.

1. Entre na pasta do projeto e crie a imagem do projeto:

```
docker build -t salic_bot:latest .
```

2. Crie um novo container com a imagem recém criada:

```
docker run --name salic_bot -e SALIC_BOT_TOKEN=<seu token aqui> salic_bot:latest
```

## Docker no desenvolvimento

No caso de desenvolvimento, é recomendado o uso do [docker-compose](https://docs.docker.com/compose/install/) para testar as implementações do bot.

Para definir o token, crie um arquivo `.env` e defina o o valor gerado pelo @BotFather:

```
SALIC_BOT_TOKEN=<seu token aqui>
```

Feito isso é só rodar via `run`. O Compose irá gerar a imagem e levanta-lo:

```
docker-compose build salic_bot
```

## Passos da Instalação para Debian/Ubuntu

1. Instale o PIP, instalador dos pacotes python3

    Baixe o arquivo get-pip.py que é um arquivo instalador executado pelo Python. O arquivo se encontra no link https://bootstrap.pypa.io/get-pip.py.
O arquivo pode ser baixado de forma direta e rápida utilizando o comando wget -c. A opção -c tem a função de continuar o download em caso de perda de conexão.

    ```
    wget -c https://bootstrap.pypa.io/get-pip.py

    sudo python3 get-pip.py
    
    ```

2. Instale o construtor de ambiente virtual
    ```
    sudo apt-get install python3-virtualenv python3-venv
    
    ```

3. Adcione o repositorio do SQlitedrowser, atualize o apt-get e instale o pacote
    ```
    sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser
    
    ```
    ``` 
    sudo apt-get update
    
    ```
    
    ```
    sudo apt-get install sqlitebrowser
    
    ```
4. Crie seu ambiente virtual e entre no diretório
    ```
    pyvenv /caminho/para/o/ambiente/virtual

    ```
    
    ```
    cd  /caminho/para/o/ambiente/virtual

    ```
5. Clone o repositório do projeto do github
    ```
    git clone https://github.com/ShinNin-chan/bot_salic_notifica.git

    ```

6. Ative o ambiente virtual instale as dependências python do projeto
    ```
    source /caminho/para/o/ambiente/virtual/bin/activate

    ```
    
    ```
    pip3 install -r requirements.txt
    
    
    ```
    
7. Configure o banco de dados

```
Essa instrução esta sendo desenvolvida...

```

11. Execute a aplicação (É preciso ter o ambiente virtual ativado)
    ```
    python3 bot.py runservice

    ```
