<h1 align="center">
  <br>
  Projeto da disciplina TEC 502 - Concorrência e Conectividade
  <br>
</h1>
<div>
 
> Este projeto foi desenvolvido como parte da disciplina MI - Concorrência e Conectividade, do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS).



# Descrição do projeto 
O projeto consiste em um sistema de controle e monitoramento de dispositivos IoT (Internet das Coisas) que visa facilitar a interação entre usuários e dispositivos conectados. Através de uma interface intuitiva, os usuários podem monitorar o estado dos dispositivos, como ar-condicionado, e controlar suas operações remotamente. O sistema utiliza um servidor Broker como intermediário na comunicação entre a interface de usuário e os dispositivos, garantindo uma comunicação eficiente e segura
<div>
  <img width="800px" align="center" src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/esquema1.png">
</div>

# Broker
O Broker é o componente central deste sistema, desempenhando um papel vital como intermediário na comunicação entre as interfaces e os dispositivos. Ele é responsável por facilitar a troca de mensagens entre essas duas entidades principais, garantindo uma comunicação eficaz e confiável.

### Funcionalidades do Broker:
* Registro de Dispositivos Conectados:
     O Broker mantém uma lista de dispositivos que conseguiram estabelecer conexão com sucesso. Cada dispositivo conectado é registrado em uma estrutura de dados, contendo informações como o socket de conexão, endereço IP, porta TCP utilizada, estado atual do dispositivo e sua temperatura.
* Comunicação Bidirecional:
    O Broker atua como um intermediário para a comunicação bidirecional entre as interfaces e os dispositivos. Ele recebe mensagens das interfaces, encaminha para os dispositivos relevantes e vice-versa, garantindo uma troca contínua de informações.
*  Processamento de Mensagens UDP:
    O Broker inicializa e aguarda mensagens UDP dos dispositivos conectados. Quando uma mensagem é recebida, ela é colocada em uma fila para processamento. As mensagens são então tratadas e processadas, permitindo que o Broker interprete e aja com base nas informações recebidas.

* Verificação de Conexão:
    Periodicamente, o Broker verifica a conexão com cada dispositivo na lista. Isso é feito enviando uma mensagem TCP para cada dispositivo e aguardando uma resposta. Se o dispositivo não responder, é considerado offline e removido da lista de dispositivos conectados.

# Dispositivo
O Dispositivo é uma representação virtual de um ar condicionado no ambiente de software. Ele simula as funcionalidades básicas de um ar condicionado, como ligar, desligar e ajustar a temperatura, e comunica-se com o Broker para troca de informações.

### Funcionalidades do Dispositivo:
* Emulação do Ar Condicionado:
O Dispositivo emula as operações de um ar condicionado, permitindo que o usuário controle remotamente suas funcionalidades. Isso é feito através de uma interface CLI, onde o usuário pode enviar comandos para ligar, desligar e modificar a temperatura manualmente.

* Envio de Dados via UDP:
O Dispositivo periodicamente envia seus dados captados para o Broker através de mensagens UDP. Esses dados são enviados em formato de string concatenada, contendo informações como o status atual do ar condicionado e sua temperatura.

* Verificação de Conexão:
Para garantir a integridade da conexão, o Dispositivo verifica continuamente a comunicação com o Broker. Isso é feito enviando uma confirmação TCP sempre que uma mensagem é recebida com sucesso do Broker, garantindo uma conexão estável e confiável.

# Interface
A Interface é a camada através da qual os usuários interagem com os dispositivos IoT, proporcionando controle remoto e visualização do estado dos dispositivos. Aqui estão alguns detalhes adicionais sobre suas funcionalidades:

### Funcionalidades da Interface:
* Obtenção e Exibição de Dispositivos:
A Interface obtém regularmente uma lista de dispositivos conectados ao Broker e exibe suas informações, como endereço IP, porta TCP, estado atual (ligado/desligado) e temperatura.
* Controle Remoto de Dispositivos:
Os usuários podem interagir com os dispositivos através da Interface, enviando comandos como ligar, desligar e ajustar a temperatura. Quando um comando é selecionado, a Interface envia a mensagem correspondente para o Broker, que a encaminha para o dispositivo relevante.
* Feedback ao Usuário:
A Interface fornece feedback em tempo real sobre as ações realizadas. Por exemplo, se um usuário tentar ligar um dispositivo que já está ligado, a Interface informará ao usuário que o dispositivo já está ligado, garantindo uma experiência de usuário fluida e intuitiva.
<div>
  <img width="800px" src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/tela.jpg">
</div>

# API
A API neste projeto atua como uma ponte entre a aplicação cliente e o servidor Broker, facilitando a comunicação e o controle dos dispositivos IoT. Aqui está como a API é implementada e utilizada:

Endpoints:

* Obtenção de Dispositivos Conectados:
  * O endpoint /tcp-clients/ é utilizado pela aplicação cliente para obter uma lista dos dispositivos IoT conectados ao servidor Broker. Essa lista inclui informações como endereço IP, porta TCP, estado atual (ligado/desligado) e temperatura dos dispositivos.

```
   # Exemplo de resposta do endpoint /tcp-clients/
[
    {
        "ip": "192.168.1.100",
        "port": 5000,
        "status": "ligado",
        "temperatura": 25
    },
    {
        "ip": "192.168.1.101",
        "port": 5001,
        "status": "desligado",
        "temperatura": 0
    }
]
 ``` 
* Envio de Comandos para Dispositivos:
  * O endpoint /send-message/ permite que a aplicação cliente envie comandos para controlar os dispositivos conectados. Os comandos disponíveis incluem ligar, desligar e ajustar a temperatura do dispositivo. As mensagens são enviadas no formato JSON e incluem informações sobre o tipo de comando, o endereço IP do dispositivo, a porta TCP e outros parâmetros necessários.

# Uso de Threads
Threads no Broker e no Dispositivo
As threads desempenham um papel fundamental no projeto, tanto no Broker quanto no Dispositivo, permitindo a execução concorrente de várias tarefas de forma eficiente. Aqui está uma visão geral das threads utilizadas em cada componente:
* No Broker:
  * Thread de Aceitação de Conexões TCP (`tcp_thread`):
  Responsável por aceitar novas conexões TCP dos dispositivos.
  Esta thread fica em um loop infinito, aguardando novas conexões.
  * Cada nova conexão é tratada por uma nova thread, garantindo a capacidade de lidar com múltiplas conexões simultaneamente.
  * Thread de Gerenciamento de Conexões TCP:
    Cada nova conexão TCP estabelecida com um dispositivo é tratada por uma thread dedicada.
    Essas threads são responsáveis por registrar o dispositivo conectado, verificar periodicamente a conexão e processar as mensagens recebidas.
  * Thread de Recebimento de Mensagens UDP(`handle_udp_connection`):
    Responsável por receber as mensagens enviadas pelos dispositivos via UDP.

    As mensagens recebidas são colocadas em uma fila para processamento posterior.
  * Thread de Processamento de Mensagens UDP(`process_udp_thread`):
    Fica em um loop infinito processando as mensagens recebidas via UDP.
    As mensagens são analisadas e as informações relevantes são atualizadas no registro do dispositivo.
  * Thread de Processamento de Mensagens HTTP(`http_thread`):
    Responsável por processar as mensagens recebidas via HTTP a partir da interface de usuário.
    As mensagens contêm comandos para controlar os dispositivos, como ligar, desligar e ajustar a temperatura.
    Após o processamento, as mensagens são encaminhadas para os dispositivos correspondentes.
  * Thread de Verificação de Conexão de Dispositivos(`verificação_conexão_thread`):
    Periodicamente verifica o status de conexão dos dispositivos registrados.
    Envia mensagens de verificação para os dispositivos e remove os dispositivos desconectados da lista de registros.
* No Dispositivo:
  * Thread de Envio de Informações via UDP(`envio_informações`):
Responsável por enviar periodicamente as informações do dispositivo para o Broker via UDP.
As informações incluem o estado atual do dispositivo e a temperatura.Garante uma comunicação contínua e atualizada com o Broker.
  * Thread de Tratamento de Mensagens TCP(`receive_thread`):
Fica em um loop infinito aguardando mensagens TCP do Broker.
As mensagens recebidas são processadas e as ações correspondentes são executadas no dispositivo, como ligar, desligar ou ajustar a temperatura.


# Protocolos de Comunicação Utilizados:
### Entre a Aplicação e o Servidor Broker: HTTP (Hypertext Transfer Protocol)
O HTTP é um protocolo de comunicação amplamente utilizado para transferência de dados na World Wide Web. Ele opera em um modelo cliente-servidor, onde a aplicação age como cliente, enviando solicitações HTTP para o servidor Broker, que atua como servidor, respondendo a essas solicitações.

### Características do HTTP:
* Stateless: O HTTP é um protocolo stateless, o que significa que não mantém informações sobre as conexões entre as solicitações. Cada solicitação HTTP é tratada de forma independente, sem conhecimento do contexto das solicitações anteriores.

### Entre os Dispositivos e o Servidor Broker: TCP (Transmission Control Protocol) e UDP (User Datagram Protocol)

Para a comunicação entre os dispositivos e o servidor Broker, são utilizados os protocolos TCP e UDP, cada um com suas características específicas:
* TCP (Transmission Control Protocol):
    * Orientado à Conexão: O TCP estabelece uma conexão confiável e orientada à conexão entre os dispositivos e o servidor Broker. Ele garante a entrega dos dados na ordem correta, sem perdas ou corrupção.
    * Garantia de Entrega: O TCP utiliza mecanismos de confirmação e retransmissão para garantir que os dados sejam entregues com sucesso ao destino.
* UDP (User Datagram Protocol):
    * Não Orientado à Conexão: O UDP é um protocolo de comunicação não orientado à conexão, o que significa que não há estabelecimento prévio de conexão antes da transmissão dos dados.
    * Menor Overhead: Comparado ao TCP, o UDP possui um menor overhead devido à ausência de mecanismos de garantia de entrega e controle de fluxo. Isso o torna mais adequado para aplicações onde a latência é crítica e a perda ocasional de dados é tolerável.

## Camada de Aplicação
A Camada de Aplicação é responsável por fornecer serviços de comunicação entre os diferentes dispositivos e interfaces do sistema. Ela define os protocolos e formatos de mensagem utilizados para a troca de informações e comandos entre os componentes do sistema.

* Funcionalidades da Camada de Aplicação:
    * Definição de Protocolos de Comunicação:
    Na Camada de Aplicação, são definidos os protocolos de comunicação utilizados para facilitar a interação entre os dispositivos, interfaces e o Broker. Isso inclui o formato das mensagens, os tipos de dados suportados e os procedimentos para a troca de informações.
* Processamento de Comandos:
    * A Camada de Aplicação é responsável por interpretar os comandos recebidos das interfaces e encaminhá-los para os dispositivos correspondentes. Isso envolve o processamento de mensagens de controle, como ligar, desligar e ajustar a temperatura, e garantir que esses comandos sejam executados corretamente pelos dispositivos.
* Gerenciamento de Dados:
    * Além do processamento de comandos, a Camada de Aplicação também é responsável pelo gerenciamento e armazenamento de dados. Isso inclui a manutenção de informações sobre os dispositivos conectados, o registro de eventos e o histórico de operações realizadas.

## Camada de Transporte
A Camada de Transporte é responsável por garantir a entrega confiável e eficiente das mensagens entre os dispositivos e o Broker. Ela define os protocolos e mecanismos utilizados para estabelecer e manter conexões de comunicação, bem como para controlar o fluxo e a integridade dos dados transmitidos.

Funcionalidades da Camada de Transporte:
* Estabelecimento de Conexões:
    * A Camada de Transporte é responsável por estabelecer conexões confiáveis entre os dispositivos e o Broker. Isso é feito através de protocolos como TCP, que garantem a entrega ordenada e confiável dos dados, e UDP, que oferece uma alternativa de baixa latência e menor overhead.
* Controle de Fluxo:
    * Para garantir uma comunicação eficiente, a Camada de Transporte controla o fluxo de dados entre os dispositivos e o Broker. Isso envolve o gerenciamento da taxa de transmissão de dados, a prevenção de congestionamentos na rede e a garantia de uma transferência suave e contínua das informações.
* Manutenção da Conexão:
    * Além de estabelecer conexões, a Camada de Transporte também é responsável por manter e monitorar ativamente a integridade das conexões existentes. Isso inclui a detecção e o tratamento de falhas na rede, a retransmissão de dados quando perdidos e a garantia de uma comunicação contínua e estável entre os dispositivos e o Broker.
## Conclusão
Em resumo, o projeto mostra como os dispositivos IoT, o Broker e a interface do usuário se comunicam de maneira eficiente. O uso de diferentes protocolos de comunicação, como HTTP, TCP e UDP, garante uma interação confiável entre os componentes. As threads são usadas para permitir a execução simultânea de várias tarefas em cada parte do sistema. A API simplifica o acesso aos recursos do sistema, facilitando o desenvolvimento de aplicativos. Em conjunto, esses elementos criam um sistema capaz de lidar com as demandas de conectividade e controle em ambientes IoT de forma eficaz e escalável.
## Manual de uso 
### Primeiro passo: Inicialização Broker
- É necessário a instalação das bibliotecas dependentes nesse caso os com o seguintes comando no prompt de comando:
  ```
   pip install Flask
   pip install flask-cors
  ```

- Execute o código broker em um ambiente ou idle compátivel com python
- Deve-se verificar se as constantes de conexão estão corretas para que o servidor broker seja inicializado corretamente

### Segundo passo: Inicialização do(s) Dispositivo(s) envolvido(s)
- Execute o código que simula um ar condicionado em um ambiente ou idle que seja compatível com python

- Deve-se verificar se as constantes de conexão do dispositivo estão iguais ao do servidor para prosseguir

- O Dispositivo começará a funcionar quando sua conexão for aceita pelo servidor além de exibir o menu via terminal que pode ser controlado também como via de controle manual

### Último passo: Inicialização da interface gráfica
- É necessário acessar o html em um navegador

- Deve-se verificar se a interface está configurada com o URL e porta corretas
<div>
  <img width="800px" src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/tela.jpg">
</div>

- Clique no botão de Obter lista de Dispositivos

- Utilize os botões de controle para ligar/desligar o dispositivo

- Utilize a caixa de seleção de temperatura e em seguida o botão Enviar Temperatura para modificar a temperatura

- É necessário ressaltar que não é impossível alterar a temperatura de um dispositivo desligado
## Execução via Docker
Para executar sem precisar contruir uma imagem, já existe uma imagem feita que está hospedada no site https://www.docker.com/

*Siga pos seguintes passos para executar o broker:*

* `docker pull joaogabrielaraujo/broker`
* `docker run --network=host -it -e IP=<ip do servidor> joaogabrielaraujo/broker `

Com isso o broker já estará rodando

*Para emular o dispositivo:*
* `docker pull joaogabrielaraujo/device`
* `docker run --network=host -it -e SERVER_IP=<ip do servidor> joaogabrielaraujo/device`

*Para executar a interface gráfica*
* `git clone https://github.com/joaogabrielaraujo/Tec502-PBL1`
<div>
  <img  src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/rota PBL.jpg">
</div>

* Navegue até a pasta PBL
<div>
  <img  src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/rota Interface.jpg">
</div>
<div>
  <img  src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/rota arquivo_interface.jpg">
</div>


* Continue pela pasta Interface e dê dois clicks no arquivo `interface.html` para abrir o navedor que estive utilizando a interface 

<div>
  <img width="800px" src="https://github.com/joaogabrielaraujo/Tec502-PBL1/blob/main/img/tela.jpg">
</div>

</div>
