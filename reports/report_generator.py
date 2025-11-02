import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")  # Sube a la carpeta raiz del proyecto
sys.path.append(project_root)

from extraction.exchange_rate import get_tipo_de_cambio

from config.settings import DATA_TRANSFORM_PATH
from config.settings import DATA_MERGE_PATH
from config.settings import OUTPUT_PATH
from config.settings import OUTPUT_GRAFICOS

try:

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    if not os.path.exists(OUTPUT_GRAFICOS):
        os.makedirs(OUTPUT_GRAFICOS)

    # Leer archivos READ CSV
    transacciones = pd.read_csv(DATA_TRANSFORM_PATH + "/transacciones_transform.csv")
    clientes = pd.read_csv(DATA_TRANSFORM_PATH + "/clientes_transform.csv")
    cuentas = pd.read_csv(DATA_TRANSFORM_PATH + "/cuentas_transform.csv")
    data_merge = pd.read_csv(DATA_MERGE_PATH + "/data_merge.csv")

    # Exportando data merge a EXCEL:
    data_merge.to_excel(os.path.join(OUTPUT_PATH, "data_report.xlsx"), index=False)
    print(f"Reporte Excel generado en: {OUTPUT_PATH}")

    USD_a_PEN = get_tipo_de_cambio()
    # Generando graficos PNG

    # --------------------------------------------------------------------
    # - Gráfico de Barras: Monto Total por Tipo de Transacción (PEN - USD)
    # --------------------------------------------------------------------
    fecha_hora_actual = datetime.datetime.now()
    fecha_formateada = fecha_hora_actual.strftime("%d/%m/%y %H:%M:%S")

    monto_por_tipo = (
        data_merge.groupby("tipo_transaccion")[["monto", "monto_usd"]]
        .sum()
        .sort_values(by="monto", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    x = range(len(monto_por_tipo))
    width = 0.35  # Ancho de cada barra

    bars1 = ax.bar(
        [i - width / 2 for i in x],
        monto_por_tipo["monto"],
        width,
        label="PEN",
        color="#2CC595C9",
    )
    bars2 = ax.bar(
        [i + width / 2 for i in x],
        monto_por_tipo["monto_usd"],
        width,
        label="USD",
        color="#F2BA3AC9",
    )

    # Agregar valores en las barras: Itera sobre ambas colecciones de barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 50,  # Pequeño offset vertical
                f"{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

    ax.set_title(
        "Monto Total por Tipo de Transacción PEN vs USD",
        fontsize=14,
        fontweight="book",
    )

    fig.text(
        0.16,  # Posición X
        0.90,  # Posición Y
        f"USD-PEN: {USD_a_PEN}",
        ha="center",  # Alineación horizontal centrada
        fontweight="medium",
        fontsize=11,  # Tamaño de fuente menor que el título principal
        color="green",  # Color más sutil
        fontstyle="normal",
    )

    fig.text(
        0.98,  # Posición X (cercana al borde derecho)
        0.01,  # Posición Y (cercana al borde inferior)
        f"Fecha de creación del reporte: {fecha_formateada}",
        ha="right",  # Alineación horizontal a la derecha
        fontsize=10,
        color="black",
        style="italic",
    )

    ax.set_xlabel("Tipo de Transacción", fontsize=12)
    ax.set_ylabel(f"Monto (PEN - USD)", fontsize=12)
    ax.set_xticks(range(len(monto_por_tipo)))
    ax.set_xticklabels(monto_por_tipo.index, rotation=45, ha="right")

    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")

    plt.subplots_adjust(top=0.82, bottom=0.25)

    fig.savefig(
        os.path.join(OUTPUT_GRAFICOS, "transacciones_por_tipo_monto_total_PEN_USD.png"),
        dpi=300,
    )
    plt.close(fig)

    # -----------------------------------------------------------
    # - Gráfico de barras doble: TOP 10 - Comparación PEN vs USD
    # -----------------------------------------------------------

    # Obtener las 10 transacciones con el monto más alto en PEN
    top_10 = data_merge.nlargest(10, "monto")[
        ["id_transaccion", "monto", "monto_usd"]
    ].reset_index(drop=True)

    x = range(len(top_10))
    width = 0.35  # Ancho de cada barra

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(
        [i - width / 2 for i in x],
        top_10["monto"],
        width,
        label="PEN",
        color="#06A77CB5",
    )
    bars2 = ax.bar(
        [i + width / 2 for i in x],
        top_10["monto_usd"],
        width,
        label="USD",
        color="#D62828C4",
    )

    # Agregar valores en las barras: Itera sobre ambas colecciones de barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 50,  # Pequeño offset vertical
                f"{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )
    ax.set_title(
        f"Top 10 Transacciones: Comparación PEN vs USD",
        fontsize=14,
        fontweight="book",
    )

    fig.text(
        0.16,  # Posición X
        0.93,  # Posición Y
        f"USD-PEN: {USD_a_PEN}",
        ha="center",  # Alineación horizontal centrada
        fontweight="medium",
        fontsize=11,
        color="green",
        fontstyle="normal",
    )

    fig.text(
        0.98,  # Posición X (cercana al borde derecho)
        0.03,  # Posición Y (cercana al borde inferior)
        f"Fecha de creación del reporte: {fecha_formateada}",
        ha="right",  # Alineación horizontal a la derecha
        fontsize=10,
        color="black",
        style="italic",
    )
    ax.set_xlabel("ID Transacción", fontsize=12)
    ax.set_ylabel("Monto", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(top_10["id_transaccion"], rotation=45, ha="right")
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.subplots_adjust(top=0.90, bottom=0.16)

    fig.savefig(
        os.path.join(OUTPUT_GRAFICOS, "transacciones_top10_PEN_USD.png"), dpi=300
    )
    plt.close(fig)

    # -----------------------------------------------------
    # Grafico de Dona : Distribución por Tipos de Cuenta
    # -----------------------------------------------------
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(1, 1, 1)

    distribucion_cuentas = cuentas["tipo_cuenta"].value_counts()
    colores = ["#FF9800", "#F44336", "#9C27B0"]
    colores_con_alpha = [
        "#FF980099",  # Naranja con 60% de opacidad
        "#F4433699",  # Rojo con 60% de opacidad
        "#9C27B099",  # Púrpura con 60% de opacidad
    ]

    wedges, texts, autotexts = ax.pie(
        distribucion_cuentas,
        labels=distribucion_cuentas.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colores_con_alpha,
        wedgeprops=dict(width=0.4, edgecolor="w"),  # Estilo de Dona
    )

    for text in texts:
        text.set_fontweight("book")
        text.set_fontsize(16)

    for autotext in autotexts:
        autotext.set_fontweight("book")
        autotext.set_fontsize(18)

    ax.set_title("Distribución por Tipos de Cuenta", fontsize=18, fontweight="book")

    fig.text(
        0.98,  # Posición X (cercana al borde derecho)
        0.03,  # Posición Y (cercana al borde inferior)
        f"Fecha de creación del reporte: {fecha_formateada}",
        ha="right",  # Alineación horizontal a la derecha
        fontsize=13,
        color="black",
        style="italic",
    )
    ax.axis("equal")

    plt.subplots_adjust(top=0.90, bottom=0.12)
    fig.savefig(
        os.path.join(OUTPUT_GRAFICOS, "cuentas_distribucion_por_tipos.png"), dpi=300
    )
    plt.close(fig)

    # ------------------------------------------------------
    # - Gráfico de Lineas: Volumen Diario de Transacciones
    # ------------------------------------------------------
    volumen_diario = (
        data_merge.groupby("fecha")[["monto", "monto_usd"]].sum().reset_index()
    )
    volumen_diario["fecha"] = pd.to_datetime(volumen_diario["fecha"])

    fig, ax = plt.subplots(figsize=(12, 6))

    # Líneas
    ax.plot(
        volumen_diario["fecha"],
        volumen_diario["monto"],
        marker="o",
        color="purple",
        linewidth=2,
        label="Volumen diario (PEN)",
    )
    ax.plot(
        volumen_diario["fecha"],
        volumen_diario["monto_usd"],
        marker="o",
        color="green",
        linewidth=2,
        label="Volumen diario (USD)",
    )

    # Etiquetas con desplazamiento dinámico
    for i, row in volumen_diario.iterrows():
        # Offset proporcional al rango de cada serie
        offset_pen = max(volumen_diario["monto"]) * 0.02
        offset_usd = max(volumen_diario["monto_usd"]) * 0.02

        # Texto para PEN
        ax.text(
            row["fecha"],
            row["monto"] + offset_pen,
            f'{row["monto"]:,.0f}',
            ha="center",
            va="bottom",
            fontsize=8,
            color="black",
            bbox=dict(
                facecolor="white", alpha=0.8, edgecolor="none", boxstyle="round,pad=0.2"
            ),
        )

        # Texto para USD (debajo para que no se superponga)
        ax.text(
            row["fecha"],
            row["monto_usd"] - offset_usd,
            f'{row["monto_usd"]:,.0f}',
            ha="center",
            va="top",
            fontsize=8,
            color="black",
            bbox=dict(
                facecolor="white", alpha=0.8, edgecolor="none", boxstyle="round,pad=0.2"
            )
        )

    # Formato del eje X
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
    ax.tick_params(axis="x", rotation=30,labelsize=9 )

    # Estilos
    ax.set_title("Volumen Diario de Transacciones (PEN y USD)", fontsize=14)
    ax.set_ylabel("Monto", fontsize=12)
    ax.set_xlabel("Fecha", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()

    fig.text(
        0.16,  # Posición X
        0.93,  # Posición Y
        f"USD-PEN: {USD_a_PEN}",
        ha="center",  # Alineación horizontal centrada
        fontweight="medium",
        fontsize=11,
        color="green",
        fontstyle="normal",
    )
    fig.text(
        0.98,
        0.03,
        f"Fecha de creación del reporte: {fecha_formateada}",
        ha="right",
        fontsize=10,
        color="black",
        style="italic",
    )
    plt.subplots_adjust(top=0.90, bottom=0.16)
    fig.savefig(
        os.path.join(OUTPUT_GRAFICOS, "transacciones_volumen_diario.png"), dpi=300
    )
    plt.close(fig)

    print(f"Graficos generados en: {OUTPUT_PATH}")

except Exception as e:
    print(f"Error al generar reporte de los datos: {e}")
    sys.exit(1)
