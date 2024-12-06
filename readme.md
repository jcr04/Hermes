# Hermes: API de Machine Learning para Elegibilidade de Aluguel de Veículos

## Descrição do Projeto

Hermes é uma API desenvolvida para integrar Machine Learning ao sistema **LocadãoV3**. O objetivo principal é analisar a elegibilidade de aluguéis de veículos com base em critérios e regras predefinidos, evoluindo para soluções mais complexas ao longo do tempo.

A API coleta dados de **clientes**, **agências**, **veículos** e **aluguéis** através de integrações com o LocadãoV3 e utiliza um modelo de Machine Learning para treinar e prever a elegibilidade dos aluguéis.

---

## Estrutura do Projeto

- **`app/controllers`**:
  - Controladores que gerenciam as rotas e lógica de integração com serviços externos e Machine Learning.
- **`app/services`**:
  - Contém serviços para integração com a API LocadãoV3 e manipulação de dados de ML.
- **`app/models`**:
  - Modelos para organizar os dados utilizados pela API.
- **`models/`**:
  - Diretório para armazenar o modelo treinado de Machine Learning.
- **`readme.md`**:
  - Documento de descrição e guia do projeto.

---

## Fluxo de Funcionamento

1. **Coleta de Dados**:
   - A API Hermes utiliza os endpoints do LocadãoV3 para coletar dados sobre agências, veículos, clientes e aluguéis.
   - Detalhes específicos de agências e veículos são recuperados usando os GUIDs fornecidos.

2. **Treinamento do Modelo**:
   - Dados históricos são utilizados para treinar um modelo de **Random Forest** que analisa a elegibilidade.

3. **Previsão de Elegibilidade**:
   - Para cada aluguel, a API avalia os critérios predefinidos e retorna o resultado:
     ```json
     {
         "id": "b2c614c1-134f-4948-a2cc-ae4784ab5d00",
         "elegivel": true,
         "motivo": "Atende a todos os critérios."
     }
     ```

---

## Rotas da API

### 1. **`/eligibility`**
- **Descrição**: Processa dados para treino ou previsão de elegibilidade.
- **Método**: `POST`
- **Exemplo de Corpo da Requisição**:
  ```json
  {
      "train": true
  }
  ```
## Resposta para Previsão
```json
[
    {
        "id": "b2c614c1-134f-4948-a2cc-ae4784ab5d00",
        "elegivel": true,
        "motivo": "Atende a todos os critérios."
    }
]
```
## Resposta para Treinamento
```json
{
    "message": "Modelo treinado com sucesso!"
}
```

### 2. **`/process`**
**Descrição**: Processa dados de Machine Learning para treino ou previsão.
- **Método**: `POST`
- **Exemplo de Corpo da Requisição**:
  ```json
  {
    "data": [
        {
            "features": [1, 1, 150],
            "label": 1
        }
    ],
    "train": true
  } 
  ```
## Resposta para Previsão:
  ```json
  [
      {
          "id": "b2c614c1-134f-4948-a2cc-ae4784ab5d00",
          "elegivel": true,
          "motivo": "Atende a todos os critérios."
      }
  ]
  ```

## Resposta para Treinamento:
  ```json
  {
    "message": "Modelo treinado com sucesso!"
  }
  ```
