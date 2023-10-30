# Версия python 
FROM python:3.11.5

# Расположение приложения в Docker контейнере
WORKDIR /app

# Копирование файлов в Docker контейнер с приложением
COPY Presentation.py /app/Presentation.py
COPY requirements.txt /app/requirements.txt
COPY abresults.csv /app/abresults.csv
COPY ads.csv /app/ads.csv
COPY eche.xlsx /app/eche.xlsx
COPY file.xlsx /app/file.xlsx
COPY leads.csv /app/leads.csv
COPY materials.xlsx /app/materials.xlsx
COPY experement.xlsx /app/experement.xlsx
COPY purchases.csv /app/purchases.csv
COPY readme.md /app/readme.md
COPY pages/1_EPP_calculation.py /app/pages/1_EPP_calculation.py
COPY pages/2_Concentrate.py /app/pages/2_Concentrate.py
COPY pages/3_AB_Tester.py /app/pages/3_AB_Tester.py
COPY pages/4_ADS_analyzer.py /app/pages/4_ADS_analyzer.py
COPY pages/5_DataFrame_visualizer.py /app/pages/5_DataFrame_visualizer.py
COPY .streamlit/config.toml /app/streamlit/config.toml

# Зависимости приложения
RUN pip install -r requirements.txt

# Команда, запуска приложения внутри контейнера
CMD ["streamlit", "run", "./Presentation.py", "--server.port", "8502"]