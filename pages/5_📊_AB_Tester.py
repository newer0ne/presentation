import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import norm
import altair as alt

st.set_page_config(
    page_title="A/B Tester", page_icon="📊", initial_sidebar_state="expanded"
)


def conversion_rate(conversions, visitors):
    """Возвращает коэффициент конверсии для заданного количества конверсий и количества посетителей.
    Параметры:
    ----------
    conversions: int
        Общее количество конверсий
    visitors: int
        Общее количество уникальных посетителей
    Returns
    -------
    float
        Коэффициент конверсии
    """
    return (conversions / visitors) * 100


def lift(cra, crb):
    """Возвращает относительный рост коэффициента конверсии.
     Параметры
    ----------
    cra: float
        Коэффициент конверсии группы А
    crb: float
        Коэффициент конверсии группы B
    Returns
    -------
    float
        Относительный рост коэффициента конверсии
    """
    return ((crb - cra) / cra) * 100


def std_err(cr, visitors):
    """
    Возвращает стандартную ошибку коэффициента конверсии.
    Стандартная ошибка используется для расчета отклонения 
    показателей конверсии для конкретной группы, 
    если эксперимент повторяется несколько раз.
    Для данного коэффициента конверсии (cr) и 
    количества попыток (посетителей) 
    стандартная ошибка рассчитывается как:
    Стандартная ошибка (std_err) = квадратный корень из (cr * (1-cr) / посетители)
    Параметры
    ----------
    cr: float
        Коэффициент конверсии группы (A или B)
    visitors: float
        Общее количество уникальных посетителей
    Returns
    -------
    float
        Возвращает стандартную ошибку коэффициента конверсии.
    """
    return np.sqrt((cr / 100 * (1 - cr / 100)) / visitors)


def std_err_diff(sea, seb):
    """Возвращает статистику теста z-оценки.
    Параметры
    ----------
    sea: float
        Стандартная ошибка коэффициента конверсии группы А
    seb: float
        Стандартная ошибка коэффициента конверсии группы B
    Returns
    -------
    float
        Стандартная ошибка разности выборочного распределения между
        Группой А и Группой B
    """
    return np.sqrt(sea ** 2 + seb ** 2)


def z_score(cra, crb, error):
    """Возвращает статистику теста z-оценки, точно определяющую,
    на сколько стандартных отклонений выше или ниже
    среднего значение точки данных.
    Параметры
    ----------
    cra: float
        Коэффициент конверсии группы А
    crb: float
        Коэффициент конверсии группы B
    error: float
        Стандартная ошибка разности выборочного распределения между
        Группой А и Группой B
    Returns
    -------
    float
        статистика z-оценки (стандартная оценка)
    """
    return ((crb - cra) / error) / 100


def p_value(z, hypothesis):
    """Возвращает p-значение, которое представляет собой вероятность
    получения предельно вероятных результатов теста,
    при условии, что нулевая гипотеза верна. Это просто способ 
    использовать неожиданность в качестве основы для принятия разумного решения.
    Параметры
    ----------
    z: float
        статистика z-оценки (стандартная оценка)
    hypothesis: str
        Тип проверки гипотез: «Односторонний» или «Двусторонний».
        «Односторонний» - это проверка статистической гипотезы, 
        предназначенная для демонстрации того, что среднее значение
        выборки будет выше или ниже среднего значения генеральной 
        cовокупности, но не того и другого одновременно.
        «Двусторонний» - это проверка статистической гипотезы,
        в которой критическая область распределения является 
        двусторонней и проверяет, больше или меньше выборка 
        диапазона значений.
    Returns
    -------
    float
        p-value
    """
    if hypothesis == "One-sided" and z < 0:
        return 1 - norm().sf(z)
    elif hypothesis == "One-sided" and z >= 0:
        return norm().sf(z) / 2
    else:
        return norm().sf(z)


def significance(alpha, p):
    """Возвращает, является ли p-value статистически значимым или нет.
    Значение p-value (p) меньше уровня значимости (alpha) является статистически значимым.
    Параметры
    ----------
    alpha: float
        Уровень значимости (α) — это вероятность ошибки первого рода —
        вероятность отклонения нулевой гипотезы, когда она верна.
    p: float
        p-value
    Returns
    -------
    str
        "YES" если значимый результат, "NO" если нет
    """
    return "YES" if p < alpha else "NO"


def plot_chart(df):
    """Отображает гистограмму коэффициентов конверсии групп тестов A/B,
    где ось Y обозначает коэффициенты конверсии.
    Параметры
    ----------
    df: pd.DataFrame
        Исходный DataFrame, содержащий данные для построения графика
    Returns
    -------
    streamlit.altair_chart
        Гистограмма с текстом над каждым столбцом,
        обозначающим коэффициент конверсии.
    """
    chart = (
        alt.Chart(df)
        .mark_bar(color="#61b33b")
        .encode(
            x=alt.X("Group:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Conversion:Q", title="Conversion rate (%)"),
            opacity="Group:O",
        )
        .properties(width=500, height=500)
    )

    # Place conversion rate as text above each bar
    chart_text = chart.mark_text(
        align="center", baseline="middle", dy=-10, color="black"
    ).encode(text=alt.Text("Conversion:Q", format=",.3g"))

    return st.altair_chart((chart + chart_text).interactive())


def style_negative(v, props=""):
    """Вспомогательная функция для окрашивания текста в DataFrame, 
    если он отрицательный.
    Параметры
    ----------
    v: float
        Текст (v) в DataFrame для окрашивания
    props: str
        Строка с парой атрибут-значение CSS. 
        Например, «цвет: красный;»
        Подглядеть можно здесь:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
    Returns
    -------
    Стилизованный DataFrame с отрицательными значениями, 
    окрашенными в красный цвет.
    Пример
    -------
    >>> df.style.applymap(style_negative, props="color:red;")
    """
    return props if v < 0 else None


def style_p_value(v, props=""):
    """Вспомогательная функция для окрашивания p-value в DataFrame. 
    Если p-value статистически значимо, 
    текст окрашивается в зеленый цвет; иначе красный.
    Параметры
    ----------
    v: float
        Текст (v) в DataFrame для окрашивания в цвет
    props: str
        Строка с парой атрибут-значение CSS. 
        Например, "цвет:зеленый;"
        Подглядеть можно здесь:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
    Returns
    -------
    Стилизованный DataFrame с отрицательными значениями,
    окрашенными в красный цвет.
    Пример
    -------
    >>> df.style.apply(style_p_value, props="color:red;", axis=1, subset=["p-value"])
    """
    return np.where(v < st.session_state.alpha, "color:green;", props)


def calculate_significance(
    conversions_a, conversions_b, visitors_a, visitors_b, hypothesis, alpha
):
    """Вычисляет все отображаемые показатели, включая коэффициенты конверсии,
    прирост, стандартные ошибки, z-оценку, p-значение, значимость,
    и сохраняет их как сессионные переменные.
    Параметры
    ----------
    conversions_a: int
        Количество пользователей, которые совершили покупку
        при показе варианта / группа A
    conversions_b: int
        Количество пользователей, которые совершили покупку
        при показе варианта / группа B
    visitors_a: int
        Общее количество пользователей, 
        которым показан вариант / группа A
    visitors_b: int
        Общее количество пользователей,
        которым показан вариант / группа B
    hypothesis: str
        Тип проверки гипотез: «Односторонний» или «Двусторонний».
    «Односторонний» - это проверка статистической гипотезы, 
    предназначенная для демонстрации того, что среднее значение выборки
    будет выше или ниже среднего значения генеральной совокупности,
    но не того и другого одновременно.
    «Двусторонний» - это проверка статистической гипотезы,
    в которой критическая область распределения является двусторонней
    и проверяет, больше или меньше выборка диапазона значений.
    alpha: float
        Уровень значимости (α) — это вероятность ошибки первого рода
        — вероятность отклонения нулевой гипотезы, когда она верна.
    """
    st.session_state.cra = conversion_rate(int(conversions_a), int(visitors_a))
    st.session_state.crb = conversion_rate(int(conversions_b), int(visitors_b))
    st.session_state.uplift = lift(st.session_state.cra, st.session_state.crb)
    st.session_state.sea = std_err(st.session_state.cra, float(visitors_a))
    st.session_state.seb = std_err(st.session_state.crb, float(visitors_b))
    st.session_state.sed = std_err_diff(st.session_state.sea, st.session_state.seb)
    st.session_state.z = z_score(
        st.session_state.cra, st.session_state.crb, st.session_state.sed
    )
    st.session_state.p = p_value(st.session_state.z, st.session_state.hypothesis)
    st.session_state.significant = significance(
        st.session_state.alpha, st.session_state.p
    )


st.write(
    """
# 📊 A/B Tester
Загрузите результаты эксперимента, чтобы увидеть значимость вашего A/B-теста.
"""
)

uploaded_file = st.file_uploader("Загрузка .CSV фалов", type=".csv")

use_example_file = st.checkbox(
    "Использовать файл с примером", False, help="Используйте встроенный файл с примером для демонстрации работы приложения"
)

ab_default = None
result_default = None

# If CSV is not uploaded and checkbox is filled, use values from the example file
# and pass them down to the next if block
if use_example_file:
    uploaded_file = "Website_Results.csv"
    ab_default = ["variant"]
    result_default = ["converted"]


if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("### Обзор данных")
    st.dataframe(df.head())

    st.markdown("### Выберите столбцы для анализа")
    with st.form(key="my_form"):
        ab = st.multiselect(
            "Колонки A/B тестирования",
            options=df.columns,
            help="Выберите, какой столбец относится к вашим ярлыкам A/B-тестирования.",
            default=ab_default,
        )
        if ab:
            control = df[ab[0]].unique()[0]
            treatment = df[ab[0]].unique()[1]
            decide = st.radio(
                f"Колонка датафрейма *{treatment}* относится к группе Б?",
                options=["Да", "Нет"],
                help="Выберите «Да», если это группа B из вашего теста.",
            )
            if decide == "Нет":
                control, treatment = treatment, control
            visitors_a = df[ab[0]].value_counts()[control]
            visitors_b = df[ab[0]].value_counts()[treatment]

        result = st.multiselect(
            "Колонка с результатом",
            options=df.columns,
            help="Выберите, в каком столбце отображается результат теста.",
            default=result_default,
        )

        if result:
            conversions_a = (
                df[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][control]
            )
            conversions_b = (
                df[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][treatment]
            )

        with st.expander("Отрегулируйте параметры теста"):
            st.markdown("### Параметры")
            st.radio(
                "Тип гипотезы",
                options=["Односторонняя", "Двусторонняя"],
                index=0,
                key="hypothesis",
                help="TBD",
            )
            st.slider(
                "Уровень значимости (α)",
                min_value=0.01,
                max_value=0.10,
                value=0.05,
                step=0.01,
                key="alpha",
                help=" Вероятность ошибочного отклонения нулевой гипотезы, если нулевая гипотеза верна. Это также называется ложным срабатыванием и ошибкой первого рода. ",
            )

        submit_button = st.form_submit_button(label="Submit")

    if not ab or not result:
        st.warning("Выберите **Колонки A/B тестирования** и **Колонка с результатом**.")
        st.stop()

    # type(uploaded_file) == str, means the example file was used
    name = (
        "Website_Results.csv" if isinstance(uploaded_file, str) else uploaded_file.name
    )
    st.write("")
    st.write("## Результаты A/B-тестирования файла ", name)
    st.write("")

    # Obtain the metrics to display
    calculate_significance(
        conversions_a,
        conversions_b,
        visitors_a,
        visitors_b,
        st.session_state.hypothesis,
        st.session_state.alpha,
    )

    mcol1, mcol2 = st.columns(2)

    # Use st.metric to diplay difference in conversion rates
    with mcol1:
        st.metric(
            "Delta",
            value=f"{(st.session_state.crb - st.session_state.cra):.3g}%",
            delta=f"{(st.session_state.crb - st.session_state.cra):.3g}%",
        )
    # Display whether or not A/B test result is statistically significant
    with mcol2:
        st.metric("Significant?", value=st.session_state.significant)

    # Create a single-row, two-column DataFrame to use in bar chart
    results_df = pd.DataFrame(
        {
            "Group": ["Control", "Treatment"],
            "Conversion": [st.session_state.cra, st.session_state.crb],
        }
    )
    st.write("")
    st.write("")

    # Plot bar chart of conversion rates
    plot_chart(results_df)

    ncol1, ncol2 = st.columns([2, 1])

    table = pd.DataFrame(
        {
            "Converted": [conversions_a, conversions_b],
            "Total": [visitors_a, visitors_b],
            "% Converted": [st.session_state.cra, st.session_state.crb],
        },
        index=pd.Index(["Control", "Treatment"]),
    )

    # Format "% Converted" column values to 3 decimal places
    table1 = ncol1.write(table.style.format(formatter={("% Converted"): "{:.3g}%"}))

    metrics = pd.DataFrame(
        {
            "p-value": [st.session_state.p],
            "z-score": [st.session_state.z],
            "uplift": [st.session_state.uplift],
        },
        index=pd.Index(["Metrics"]),
    )

    # Color negative values red; color significant p-value green and not significant red
    table2 = ncol1.write(
        metrics.style.format(
            formatter={("p-value", "z-score"): "{:.3g}", ("uplift"): "{:.3g}%"}
        )
        .applymap(style_negative, props="color:red;")
        .apply(style_p_value, props="color:red;", axis=1, subset=["p-value"])
    )
