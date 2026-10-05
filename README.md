# Automação de Processamento de Leads

## Descrição

Este projeto foi desenvolvido para automatizar o processamento de leads de uma revenda de veículos.

A automação recebe uma lista de leads em formato JSON, realiza a limpeza e validação dos dados, identifica contatos inválidos, remove duplicidades, classifica os leads de acordo com a intenção demonstrada na mensagem e gera arquivos CSV com os resultados.

O objetivo é entregar ao time de vendas uma lista organizada, sem duplicidades e com os leads mais quentes priorizados.

---

## Tecnologias utilizadas

- Python 3
- Biblioteca `json`
- Biblioteca `re`
- Biblioteca `csv`
- Biblioteca `datetime`
- Pandas e Matplotlib para a análise adicional por origem

---

## Estrutura do projeto

```text
automacao-leads/
├── automacao.py
├── leads.json
├── leads_processados.csv
├── leads_invalidos.csv
├── leads_por_origem.png
└── README.md

```
## Como instalar e executar
### Pré-requisitos

É necessário ter o Python 3 instalado.

Instalação das bibliotecas

As bibliotecas json, re, csv e datetime fazem parte da biblioteca padrão do Python.

Para gerar a análise adicional em gráfico, instale:

pip install pandas matplotlib
Execução

Mantenha o arquivo leads.json na mesma pasta do automacao.py.

Depois, execute:

python automacao.py

Ao finalizar, a automação irá gerar os arquivos CSV e o gráfico de análise por origem.

Como a automação funciona
### 1. Leitura dos dados

O programa lê os leads diretamente do arquivo leads.json.

### 2. Tratamento dos dados

Os nomes, telefones e e-mails são normalizados conforme as regras do desafio.

### 3. Validação

Os telefones são validados e os leads com telefone ausente ou inválido são separados.

E-mails inválidos são deixados em branco sem invalidar o lead.

### 4. Remoção de duplicidades

Os leads válidos são comparados pelo telefone.

Quando existem dois leads com o mesmo telefone, o registro com a data_hora mais recente é mantido.

### 5. Classificação

Os leads são classificados como:

Quente
Morno
Frio

A classificação é feita de acordo com as palavras-chave definidas no desafio.

### 6. Ordenação

Os leads são ordenados por temperatura:

Quente → Morno → Frio

Dentro de cada grupo, os mais recentes aparecem primeiro.

### 7. Geração dos arquivos

A automação gera:

leads_processados.csv
leads_invalidos.csv
### 8. Resumo

Ao final da execução, o programa apresenta no terminal a quantidade de:

leads recebidos;
leads inválidos;
duplicados removidos;
leads finais;
leads Quentes;
leads Mornos;
leads Frios.
Decisões tomadas
E-mail inválido

Um e-mail inválido não elimina o lead. Nesse caso, o campo fica vazio.

### Duplicidades

O telefone normalizado foi utilizado para identificar duplicidades.

Em caso de duplicidade, o lead mais recente é mantido.

### Classificação

A classificação segue a ordem:

Quente → Morno → Frio

conforme especificado no desafio.

Análise adicional

Além dos requisitos principais, foi criada uma análise simples da origem dos leads processados.

O Pandas é utilizado para contar a quantidade de leads por origem e o Matplotlib para gerar um gráfico de barras.

O gráfico é uma funcionalidade complementar e não interfere no processamento principal.

### Arquivo gerado:

leads_por_origem.png
Resultado esperado

Com os dados fornecidos no desafio, o resultado esperado é:

Leads recebidos: 12
Leads inválidos: 4
Duplicados removidos: 2
Leads finais: 6

Quentes: 3
Mornos: 1
Frios: 2

## Vídeo da solução

O vídeo apresenta a execução da automação e explica o funcionamento do código.

[Assistir ao vídeo no YouTube](https://youtu.be/osyd5rzPHB0)