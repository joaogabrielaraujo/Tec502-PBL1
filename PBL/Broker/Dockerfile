# Use a imagem base do Python
FROM python:3.8-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /Broker

# Copia os arquivos necessários para o contêiner
COPY broker.py ./

# Instala as dependências e remove os arquivos temporários em uma única camada
RUN pip install Flask
RUN pip install flask-cors
    

# Define as variáveis de ambiente
ENV IP=127.0.0.1
ENV SERVER_UDP_PORT=8889
ENV SERVER_TCP_PORT=9999



# Comando para iniciar a aplicação Flask
CMD ["python", "broker.py"]