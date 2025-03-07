# Imagen base de Python
FROM python:3.11

# Definir directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Definir el comando por defecto para mantener el contenedor corriendo
CMD ["tail", "-f", "/dev/null"]
