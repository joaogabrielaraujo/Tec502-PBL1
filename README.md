<h1 align="center">
  <br>
  Projeto da disciplina TEC 502 - Concorrência e Conectividade
  <br>
</h1>

<div>


## Comunicação entre os Componentes:
O sistema é composto por três partes principais: a interface HTML, o broker.py e o dispositivo.py. A comunicação entre esses componentes é fundamental para o funcionamento adequado do sistema.

## Interface HTML e Broker.py:

A interface HTML envia solicitações HTTP para o broker.py para enviar comandos aos dispositivos de ar condicionado e receber atualizações de status. O broker.py recebe essas solicitações HTTP, processa-as e encaminha os comandos para os dispositivos conectados via TCP. Além disso, o broker.py também recebe atualizações de status dos dispositivos via UDP e atualiza a interface HTML com as informações mais recentes.

## Broker.py e Dispositivo.py:
O broker.py atua como intermediário entre a interface HTML e os dispositivos de ar condicionado. Ele recebe comandos da interface HTML e os envia para os dispositivos conectados via TCP. O dispositivo.py, por sua vez, simula um dispositivo de ar condicionado e se comunica com o broker.py para enviar seu status (estado e temperatura) via UDP e receber comandos de controle (ligar, desligar, modificar temperatura) via TCP. Essa comunicação é essencial para garantir que os dispositivos de ar condicionado possam ser controlados de forma remota e que a interface HTML exiba informações precisas sobre o estado e a temperatura desses dispositivos em tempo real.

## Funcionalidades:
### 1. Interface HTML:
A interface HTML é a parte visual do sistema, onde você pode interagir com os dispositivos de ar condicionado conectados. Ela exibe informações sobre os dispositivos, como seu estado atual (ligado/desligado) e temperatura, e permite controlar esses dispositivos enviando comandos através de botões.

Obter Lista de Dispositivos: Ao clicar neste botão, a interface solicita ao servidor uma lista atualizada de dispositivos conectados.
Botões de Controle: Para cada dispositivo listado, há botões de controle, como "Ligar", "Desligar" e "Enviar Temperatura". Você pode utilizar esses botões para controlar o estado e a temperatura dos dispositivos.
### 2. Broker.py:
O broker.py desempenha um papel central no sistema, facilitando a comunicação entre a interface HTML e os dispositivos de ar condicionado. Aqui está uma explicação detalhada das principais funcionalidades do broker.py:

Gestão de Conexões TCP e UDP: O broker.py utiliza sockets TCP e UDP para se comunicar com os dispositivos de ar condicionado. Ele estabelece conexões TCP com os dispositivos para enviar comandos e recebe atualizações de status, enquanto utiliza o UDP para receber atualizações de status dos dispositivos.
Processamento de Mensagens HTTP e UDP: Quando a interface HTML envia uma solicitação HTTP, o broker.py a recebe e a processa. Ele extrai as informações relevantes da mensagem, como o tipo de comando (ligar, desligar, modificar temperatura) e o endereço IP do dispositivo alvo, e encaminha essas informações para o dispositivo apropriado via TCP. O broker.py também recebe mensagens UDP dos dispositivos de ar condicionado, contendo atualizações de status. Ele processa essas mensagens, atualiza a lista de dispositivos conectados e suas informações de estado e temperatura, e fornece essas informações à interface HTML para exibição.
Gestão de Filas de Mensagens: Para lidar com o envio e recebimento assíncrono de mensagens, o broker.py utiliza filas de mensagens. As mensagens recebidas via UDP são colocadas em uma fila para processamento posterior, enquanto as mensagens HTTP recebidas da interface HTML são colocadas em outra fila para envio aos dispositivos via TCP.
### 3. Dispositivo.py:
O dispositivo.py representa um dispositivo de ar condicionado simulado que se comunica com o broker.py para enviar seu status e receber comandos de controle. Aqui está uma explicação mais detalhada das principais funcionalidades do dispositivo.py:

Comunicação com o Broker.py: O dispositivo.py utiliza sockets UDP para enviar periodicamente seu status (estado e temperatura) para o broker.py. Isso permite que o broker.py mantenha uma visão atualizada do estado de todos os dispositivos de ar condicionado conectados.

Envio de Status via UDP: Em intervalos regulares, o dispositivo.py envia uma mensagem UDP para o broker.py contendo seu status atual, incluindo se está ligado ou desligado e a temperatura configurada. Essa mensagem é formatada como "status-estado-temperatura" e enviada para o endereço IP e porta UDP do broker.py.

Recepção de Comandos via TCP: O dispositivo.py também fica aguardando por comandos de controle enviados pelo broker.py via TCP. Ele mantém uma conexão TCP persistente com o broker.py, permitindo que receba comandos como "ligar", "desligar" e "modificar temperatura" em tempo real.

Tratamento de Mensagens TCP: Quando recebe uma mensagem TCP do broker.py, o dispositivo.py a decodifica e executa a ação correspondente. Por exemplo, se receber o comando "ligar", ele altera seu estado para "ligado". Da mesma forma, se receber o comando "desligar", altera seu estado para "desligado". Se receber o comando "modificar temperatura", ajusta a temperatura conforme especificado na mensagem.

Gerenciamento de Conexão TCP: O dispositivo.py implementa uma lógica de reconexão para lidar com falhas na conexão TCP com o broker.py. Se a conexão for perdida, ele tenta reconectar automaticamente ao broker.py após um intervalo de tempo, garantindo uma comunicação contínua.
</div>
