import os
from datetime import datetime

from PySide6 import QtGui

import database_controller

FOLDER = "Reports/"


def generate_streamings_report():
    data = database_controller.load_database("streamings")

    os.makedirs(FOLDER, exist_ok=True)

    now = datetime.now()
    file_path = FOLDER + "raport_streamingi_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

    lines = [
        "RAPORT PLATFORM STREAMINGOWYCH - Projekt Audio Opus",
        "Wygenerowano: " + now.strftime("%Y-%m-%d %H:%M:%S"),
        "Liczba platform: " + str(len(data)),
        "=" * 50,
        ""
    ]

    if not data:
        lines.append("Brak platform streamingowych w bazie.")
    else:
        for streaming in data:
            lines.append("Id:       " + str(streaming["id"]))
            lines.append("Nazwa:    " + str(streaming["name"]))
            lines.append("Prowizja: " + str(streaming["cut"]) + "%")
            lines.append("-" * 50)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return file_path


def generate_settlement_pdf(client, items):
    os.makedirs(FOLDER, exist_ok=True)

    now = datetime.now()
    safe_name = str(client["name"]).replace(" ", "_")
    file_path = FOLDER + "raport_" + safe_name + "_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"

    company_cut = float(client["cut"])

    rows = ""
    total_revenue = 0.0
    total_company_fee = 0.0
    total_client = 0.0

    for item in items:
        product = item["product"]
        platform = item["platform"]
        revenue = float(item["revenue"])
        platform_cut = float(platform["cut"])

        company_fee = revenue * company_cut / 100
        for_client = revenue - company_fee

        total_revenue += revenue
        total_company_fee += company_fee
        total_client += for_client

        rows += (
                "<tr>"
                "<td>" + str(product["name"]) + "</td>"
                "<td>" + str(platform["name"]) + "</td>"
                "<td align='center'>" + f"{platform_cut:.0f}" + "%</td>"
                "<td align='right'>" + f"{revenue:.2f}" + " zł</td>"
                "<td align='right'>" + f"{company_cut:.0f}" + "% (" + f"{company_fee:.2f}" + " zł)</td>"
                                                                                                                                                                                                                                                        "<td align='right'><b>" + f"{for_client:.2f}" + " zł</b></td>"
                                                                                                                                                                                                                                                                                                        "</tr>"
        )

    html = """
    <h1 align='center'>Audio Opus - raport rozliczeniowy</h1>
    <p align='center'>Wygenerowano: """ + now.strftime("%Y-%m-%d %H:%M") + """</p>
    <hr>
    <p><b>Klient:</b> """ + str(client["name"]) + """ (id """ + str(client["id"]) + """)<br>
    <b>Prowizja Audio Opus:</b> """ + f"{company_cut:.0f}" + """%</p>

    <table border='1' cellspacing='0' cellpadding='6' width='100%'>
        <tr bgcolor='#dddddd'>
            <th>Produkt</th> <!-- DODANE: Nagłówek produktu -->
            <th>Platforma</th>
            <th>Prowizja platformy</th>
            <th>Wypłata od platformy</th>
            <th>Prowizja Audio Opus</th>
            <th>Dla klienta</th>
        </tr>
        """ + rows + """
        <tr bgcolor='#eeeeee'>
            <td colspan='2'><b>RAZEM</b></td> <!-- ZMIENIONE: colspan='2', żeby wyrównać układ kolumn -->
            <td></td>
            <td align='right'><b>""" + f"{total_revenue:.2f}" + """ zł</b></td>
            <td align='right'><b>""" + f"{total_company_fee:.2f}" + """ zł</b></td>
            <td align='right'><b>""" + f"{total_client:.2f}" + """ zł</b></td>
        </tr>
    </table>

    <p><b>Do wypłaty dla klienta: """ + f"{total_client:.2f}" + """ zł</b></p>
    """

    document = QtGui.QTextDocument()
    document.setHtml(html)

    writer = QtGui.QPdfWriter(file_path)
    writer.setPageSize(QtGui.QPageSize(QtGui.QPageSize.PageSizeId.A4))
    writer.setResolution(96)

    document.print_(writer)

    return file_path