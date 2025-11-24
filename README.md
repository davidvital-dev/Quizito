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
│   ├── modelos.py          # Classes de POO (Pergunta, Quiz, Usuario, Tentativa, Dificuldade)
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

### 3.1. Classes e Atributos (Implementação da Semana 2)

As classes base foram implementadas com foco em **encapsulamento** e **imutabilidade** para garantir a integridade dos dados.

| Classe | Atributo | Tipo | Descrição | Destaque POO |
| :--- | :--- | :--- | :--- | :--- |
| **Dificuldade** | FACIL, MEDIO, DIFICIL | Enum | Níveis de dificuldade válidos. | Encapsulamento de valores fixos. |
| **Pergunta** | enunciado | str | O texto da pergunta. | |
| | alternativas | tuple[str] | Tupla de 3 a 5 opções de resposta. | **Encapsulamento Defensivo (Tupla)** |
| | indice_correto | int | Índice da alternativa correta (0 a N-1). | **Validação via @property** |
| | dificuldade | Dificuldade | Nível de dificuldade da pergunta. | |
| | tema | str | Tema ao qual a pergunta pertence. | |
| **Quiz** | titulo | str | Título do quiz. | |
| | perguntas | tuple[Pergunta] | Tupla de objetos Pergunta. | **Composição e Imutabilidade (Tupla)** |
| | max_tentativas | int | Número máximo de tentativas permitidas. | |
| | tempo_limite_min | int (opcional) | Tempo máximo em minutos. | |
| **Usuario** | nome, email, matricula_id | str | Dados de identificação. | **Getters via @property** |
| | tentativas | tuple[Tentativa] | Histórico de tentativas. | **Composição e Imutabilidade (Tupla)** |
| **Tentativa** | quiz, usuario | Quiz, Usuario | Referências aos objetos relacionados. | **Getters via @property** |
| | respostas | dict[int, int] | Mapeamento Índice Pergunta -> Índice da resposta. | |
| | pontuacao_obtida | int | Pontuação final alcançada. | |
| | tempo_gasto_seg | int | Tempo total gasto em segundos. | |
| | concluida | bool | Indica se a tentativa foi concluída. | |

### 3.2. Métodos Principais (Implementação da Semana 2)

| Classe | Método | Propósito | Destaque POO |
| :--- | :--- | :--- | :--- |
| **Pergunta** | `__init__` | Construtor que utiliza os *setters* para validação inicial. | |
| | `@property` / `.setter` | Validação de dados (alternativas, índice correto). | **Encapsulamento** |
| | `__str__` | Exibição amigável da pergunta, incluindo a resposta correta (para debug). | **Método Especial** |
| | `__eq__` | Comparação por enunciado e tema (para evitar duplicidade no Quiz). | **Método Especial** |
| **Quiz** | `adicionar_pergunta` | Adiciona pergunta, garantindo a unicidade. | |
| | `calcular_pontuacao_maxima` | Calcula a pontuação com base nos pesos de dificuldade. | |
| | `__len__`, `__iter__` | Permite usar `len()` e iterar sobre as perguntas. | **Métodos Especiais** |
| **Usuario** | `adicionar_tentativa` | Adiciona Tentativa ao histórico, validando se está concluída. | **Regra de Negócio** |
| **Tentativa** | `registrar_resposta` | Registra a escolha do usuário, validando índices. | |
| | `finalizar_tentativa` | Calcula a pontuação e marca como concluída. **(Baixo Acoplamento)** | **Lógica de Negócio** |
| | `obter_gabarito` | Retorna um resumo detalhado das respostas e acertos. | |

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
**Status:** Classes Base Implementadas e Validadas (Entrega Semana 2)
