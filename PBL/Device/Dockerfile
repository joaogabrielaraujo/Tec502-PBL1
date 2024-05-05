# Use a imagem base do Python
FROM python:3.8-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /Device

# Copia os arquivos necessários para o contêiner
COPY device.py ./

# Define as variáveis de ambiente
ENV SERVER_IP=127.0.0.1
ENV SERVER_UDP_PORT=8889
ENV SERVER_TCP_PORT=9999


# Comando para iniciar a aplicação Flask
CMD ["python", "device.py"]