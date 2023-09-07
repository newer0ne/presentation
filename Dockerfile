# Версия python 
FROM python:3.11.5

# Расположение приложения в Docker контейнере
WORKDIR /app

# Копирование файлов в Docker контейнер с приложением
COPY 👋_Presentation.py /app/👋_Presentation.py
COPY requirements.txt /app/requirements.txt
COPY abresults.csv /app/abresults.csv
COPY ads.csv /app/ads.csv
COPY eche.xlsx /app/eche.xlsx
COPY file.xlsx /app/file.xlsx
COPY leads.csv /app/leads.csv
COPY Materials.xlsx /app/Materials.xlsx
COPY purchases.csv /app/purchases.csv
COPY readme.md /app/readme.md
COPY pages/1_🧪_Concentrate.py /app/pages/1_🧪_Concentrate.py
COPY pages/2_📊_AB_Tester.py /app/pages/2_📊_AB_Tester.py
COPY pages/3_📄_ADS analyzer.py /app/pages/3_📄_ADS_analyzer.py
COPY pages/4_📊_DataFrame_visualizer.py /app/pages/4_📊_DataFrame_visualizer.py

# Установите зависимости вашего приложения
RUN pip install -r requirements.txt

# Укажите команду, которая будет запускать ваше приложение внутри контейнера
CMD ["streamlit", "run", "./app.py", "--server.port 8502"]
