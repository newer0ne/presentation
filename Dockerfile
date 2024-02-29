# Версия python 
FROM python:3.10

# Расположение приложения в Docker контейнере
WORKDIR /app

# Копирование файлов в Docker контейнер с приложением
COPY main_page.py /app/main_page.py
COPY requirements.txt /app/requirements.txt
COPY .streamlit/config.toml /app/.streamlit/config.toml
COPY pages/1_epp_calculation.py /app/pages/1_epp_calculation.py
COPY pages/2_concentrate.py /app/pages/2_concentrate.py
COPY materials.xlsx /app/materials.xlsx
COPY config.json /app/config.json
COPY poly_EPP.pkl /app/poly_EPP.pkl
COPY pictures/ /app/pictures/

# Открытие порта 8502
EXPOSE 8502

# Зависимости приложения
RUN pip install -r requirements.txt

# Команда, запуска приложения внутри контейнера
CMD ["streamlit", "run", "./main_page.py", "--server.port", "8502", "--server.maxUploadSize=5"]