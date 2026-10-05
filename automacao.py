import csv
import json
import re
from datetime import datetime


def validar_email(email):
    email = email.strip().lower()

    if email.count("@") == 1:
        parte_local, dominio = email.split("@")

        if (
            parte_local != ""
            and "." in dominio
            and not dominio.startswith(".")
            and not dominio.endswith(".")
        ):
            return email

    return ""


def classificar_lead(mensagem):
    mensagem = mensagem.lower()

    if (
        "financiar" in mensagem
        or "financiamento" in mensagem
        or "troca" in mensagem
        or "test drive" in mensagem
        or "hoje" in mensagem
    ):
        return "Quente"

    elif (
        "preço" in mensagem
        or "valor" in mensagem
        or "quanto custa" in mensagem
    ):
        return "Morno"

    else:
        return "Frio"


# Leitura dos leads
with open("leads.json", "r", encoding="utf-8") as arquivo:
    leads = json.load(arquivo)


leads_validos = []
leads_invalidos = []


# Processamento e validação
for lead in leads:

    # Normalização do nome
    nome = " ".join(lead["nome"].strip().split()).title()

    # Guarda o telefone original para os leads inválidos
    # Normalização do telefone
    telefone_original = lead["telefone"]

    # Normalização do telefone
    telefone = telefone_original
    telefone = re.sub(r"\D", "", telefone)

    if len(telefone) == 13 and telefone.startswith("55"):
        telefone = telefone[2:]

    # Validação do e-mail
    email_valido = validar_email(lead["email"])

    lead["nome"] = nome
    lead["email"] = email_valido

    # Validação do telefone
    if telefone == "":
        leads_invalidos.append({
            "id": lead["id"],
            "nome": nome,
            "telefone_original": telefone_original,
            "motivo": "telefone ausente"
        })

    elif len(telefone) != 11 or telefone[2] != "9":
        leads_invalidos.append({
            "id": lead["id"],
            "nome": nome,
            "telefone_original": telefone_original,
            "motivo": "telefone inválido"
        })

    else:
        lead["telefone"] = telefone
        leads_validos.append(lead)


# Remoção de duplicidades
leads_unicos = {}

for lead in leads_validos:
    telefone = lead["telefone"]

    if telefone not in leads_unicos:
        leads_unicos[telefone] = lead

    elif (
        datetime.fromisoformat(lead["data_hora"])
        > datetime.fromisoformat(leads_unicos[telefone]["data_hora"])
    ):
        leads_unicos[telefone] = lead


leads_validos = list(leads_unicos.values())


# Classificação dos leads
for lead in leads_validos:
    lead["classificacao"] = classificar_lead(lead["mensagem"])


# Prioridade das classificações
prioridade = {
    "Quente": 1,
    "Morno": 2,
    "Frio": 3
}


# Ordenação dos leads
leads_validos.sort(
    key=lambda lead: (
        prioridade[lead["classificacao"]],
        -datetime.fromisoformat(lead["data_hora"]).timestamp()
    )
)


# Geração do CSV de leads processados
with open(
    "leads_processados.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:

    campos = [
        "nome",
        "telefone",
        "email",
        "origem",
        "classificacao",
        "data_hora"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos,
        extrasaction="ignore"
    )

    escritor.writeheader()
    escritor.writerows(leads_validos)

leads_invalidos.sort(key=lambda lead: lead["id"])

# Geração do CSV de leads inválidos
with open(
    "leads_invalidos.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:

    campos = [
        "id",
        "nome",
        "telefone_original",
        "motivo"
    ]

    escritor = csv.DictWriter(arquivo, fieldnames=campos)

    escritor.writeheader()
    escritor.writerows(leads_invalidos)


# Contagem das classificações
quantidade_quentes = 0
quantidade_mornos = 0
quantidade_frios = 0

for lead in leads_validos:

    if lead["classificacao"] == "Quente":
        quantidade_quentes += 1

    elif lead["classificacao"] == "Morno":
        quantidade_mornos += 1

    else:
        quantidade_frios += 1


# Quantidade de duplicados removidos
duplicados_removidos = (
    len(leads)
    - len(leads_invalidos)
    - len(leads_validos)
)


# Resumo da execução
print()
print("========== RESUMO ==========")
print("Leads recebidos:", len(leads))
print("Leads inválidos:", len(leads_invalidos))
print("Duplicados removidos:", duplicados_removidos)
print("Leads finais:", len(leads_validos))
print()
print("Quentes:", quantidade_quentes)
print("Mornos:", quantidade_mornos)
print("Frios:", quantidade_frios)
print("============================")

#análise adicional(opcional) por origem com gráfico
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("leads_processados.csv")


quantidade_por_origem = df["origem"].value_counts()


ax = quantidade_por_origem.plot(kind="bar")

plt.title("Quantidade de leads por origem")
plt.xlabel("Origem")
plt.ylabel("Quantidade de leads")
plt.yticks(range(0, quantidade_por_origem.max() + 1))
plt.xticks(rotation=0)

for i, valor in enumerate(quantidade_por_origem):
    ax.text(i, valor, str(valor), ha="center", va="bottom")

plt.tight_layout()

plt.savefig("leads_por_origem.png")


plt.show()