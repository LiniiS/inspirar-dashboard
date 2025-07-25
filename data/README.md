# Pasta data


**Atenção:**

- Use apenas exemplos ou dados anonimizados para testes.

## Exemplo de estrutura do JSON esperado

O arquivo JSON deve conter um objeto com a seguinte estrutura:

```json
{
  "data": {
    "result": [
      {
        "id": "123",
        "age": 35,
        "height": 1.70,
        "weight": 70,
        "sexo": "F",
        "createdAt": "2025-03-15T10:00:00Z",
        "symptomDiaries": [
          {"createdAt": "2025-03-20T08:00:00Z"}
        ],
        "acqs": [
          {"createdAt": "2025-03-22T09:00:00Z", "average": 1.2, "controlStatus": "Controlada"}
        ],
        "activityLogs": [
          {"createdAt": "2025-03-25T07:00:00Z", "steps": 5000}
        ],
        "prescriptions": [
          {
            "administrations": [
              {"date": "2025-03-21T07:00:00Z"}
            ]
          }
        ],
        "crisis": [
          {
            "initialUsageDate": "2025-04-01T10:00:00Z",
            "finalUsageDate": "2025-04-02T10:00:00Z"
          }
        ]
      }
      // ... outros pacientes ...
    ]
  }
}
```

**Observação:**
- O campo `sexo` deve ser uma string, por exemplo: "M", "F" ou "Outro".
- Todos os campos de data devem estar em formato ISO (ex: `2025-03-15T10:00:00Z`).
- Os arrays podem estar vazios caso o paciente não tenha registros para aquela funcionalidade.
- Adapte os campos conforme necessário, mas mantenha a estrutura principal para garantir o funcionamento do dashboard. 