# Use a imagem oficial do Nginx como base
FROM nginx:latest

# Define o diretório de trabalho como o diretório padrão do Nginx
WORKDIR /usr/share/nginx/html

# Copie os arquivos HTML e CSS para o diretório padrão do Nginx
COPY interface.html ./
COPY general.css ./

# Exponha a porta 80 para permitir o acesso ao Nginx
EXPOSE 80
