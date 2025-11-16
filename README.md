# Quizito - Sistema de Quiz Educacional Orientado a Objetos

## 1. Descrição do Projeto e Objetivo

Este projeto consiste no desenvolvimento de um **Sistema de Quiz Educacional** robusto, implementado como uma aplicação de **Linha de Comando (CLI)**, com foco estrito na aplicação de conceitos avançados de **Programação Orientada a Objetos (POO)**.

O objetivo principal é criar uma solução que permita:
1.  **Gerenciar** a criação de perguntas e a montagem de quizzes de múltipla escolha.
2.  **Executar** quizzes, registrando as respostas e calculando a pontuação.
3.  **Analisar** o desempenho dos usuários através de relatórios e estatísticas.
4.  **Demonstrar** o domínio de conceitos de POO, como herança, encapsulamento (@property), métodos especiais e composição, conforme exigido pela disciplina de Programação Orientada a Objetos da UFCA.

A persistência de dados será implementada de forma simples, utilizando **JSON**.

## 2. Estrutura de Arquivos

O projeto seguirá uma estrutura modular para facilitar a manutenção e os testes:

```
sistema_quiz_educacional/
├── quiz_app/
│   ├── modelos.py          # Classes de POO (Pergunta, Quiz, Usuario, Tentativa)
│   ├── dados.py            # Funções de persistência (salvar/carregar JSON)
│   ├── relatorios.py       # Lógica para geração de relatórios
│   └── cli.py              # Lógica da interface de linha de comando
├── tests/
│   ├── test_modelos.py     # Testes unitários para as classes
│   └── test_dados.py       # Testes para a persistência
├── settings.json           # Arquivo de configurações
├── main.py                 # Ponto de entrada da aplicação
└── README.md               # Documentação do projeto
```

## 3. Modelagem Orientada a Objetos (UML Textual)

### 3.1. Classes e Atributos

| Classe | Atributo | Tipo | Descrição | Destaque POO |
| :--- | :--- | :--- | :--- | :--- |
| **Dificuldade** | FACIL, MEDIO, DIFICIL | Enum | Níveis de dificuldade válidos. | Encapsulamento de valores fixos. |
| **Pergunta** | enunciado | str | O texto da pergunta. | |
| | alternativas | list[str] | Lista de 3 a 5 opções de resposta. | **Validação via @property** |
| | indice_correto | int | Índice da alternativa correta (0 a N-1). | **Validação via @property** |
| | dificuldade | Dificuldade | Nível de dificuldade da pergunta. | **Validação via @property** |
| | tema | str | Tema ao qual a pergunta pertence. | |
| **Quiz** | titulo | str | Título do quiz. | |
| | perguntas | list[Pergunta] | Lista de objetos Pergunta. | **Composição** |
| | pontuacao_maxima | int | Pontuação máxima calculada automaticamente. | |
| | tempo_limite | int (opcional) | Tempo máximo em minutos. | |
| | num_tentativas | int (opcional) | Número máximo de tentativas permitidas. | |
| **Usuario** | id | str | Identificador único (matrícula ou ID). | |
| | nome | str | Nome completo do usuário. | |
| | email | str | E-mail do usuário. | |
| | historico_tentativas | list[Tentativa] | Lista de todas as tentativas. | **Composição** |
| **Tentativa** | quiz | Quiz | Referência ao Quiz respondido. | |
| | usuario | Usuario | Referência ao Usuário. | |
| | respostas | dict[Pergunta, int] | Mapeamento Pergunta -> Índice da resposta. | |
| | pontuacao_obtida | int | Pontuação final alcançada. | |
| | tempo_gasto | float | Tempo total gasto. | |
| | concluida | bool | Indica se a tentativa foi concluída. | |

### 3.2. Métodos Principais

| Classe | Método | Propósito | Destaque POO |
| :--- | :--- | :--- | :--- |
| **Pergunta** | `__init__` | Construtor. | |
| | `@property` / `.setter` | Validação de dados (alternativas, índice, dificuldade). | **Encapsulamento** |
| | `__str__` | Exibição amigável da pergunta. | **Método Especial** |
| | `__eq__` | Comparação por enunciado e tema (para evitar duplicidade). | **Método Especial** |
| **Quiz** | `adicionar_pergunta` | Adiciona pergunta e recalcula pontuação. | |
| | `calcular_pontuacao_maxima` | Calcula a pontuação com base nos pesos de dificuldade. | |
| | `__len__`, `__iter__` | Permite usar `len()` e iterar sobre as perguntas. | **Métodos Especiais** |
| **Usuario** | `registrar_tentativa` | Adiciona Tentativa ao histórico. | |
| | `pode_tentar` | Verifica se o limite de tentativas foi atingido. | **Regra de Negócio** |
| **Tentativa** | `registrar_resposta` | Registra a escolha do usuário. | |
| | `finalizar_tentativa` | Calcula a pontuação e marca como concluída. | **Lógica de Negócio** |

### 3.3. Relacionamentos

| Origem | Multiplicidade | Relação | Multiplicidade | Destino |
| :--- | :--- | :--- | :--- | :--- |
| Quiz | 1 | contém | 1..* | Pergunta |
| Usuario | 1 | possui | 0..* | Tentativa |
| Tentativa | * | é de | 1 | Quiz |
| Tentativa | * | é de | 1 | Usuario |

---
**Desenvolvido por:** David Josué Vital Santos
**Instituição:** Universidade Federal do Cariri (UFCA)
**Disciplina:** Programação Orientada a Objetos (POO)
**Status:** Modelagem Inicial Concluída (Entrega Semana 1)
