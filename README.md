# Quizito - Sistema de Quiz Educacional Orientado a Objetos

## 1. Descrição do Projeto e Objetivo

Este projeto consiste no desenvolvimento de um **Sistema de Quiz Educacional** robusto, implementado como uma aplicação de **Linha de Comando (CLI)**, com foco estrito na aplicação de conceitos avançados de **Programação Orientada a Objetos (POO)**.

O objetivo principal é criar uma solução que permita:
1.  **Gerenciar** a criação de perguntas e a montagem de quizzes de múltipla escolha e verdadeiro/falso.
2.  **Executar** quizzes, registrando as respostas e calculando a pontuação.
3.  **Analisar** o desempenho dos usuários através de relatórios e estatísticas.
4.  **Demonstrar** o domínio de conceitos de POO, como herança (incluindo múltipla), encapsulamento (@property), métodos especiais e composição, conforme exigido pela disciplina de Programação Orientada a Objetos da UFCA.

A persistência de dados é implementada utilizando **JSON**.

## 2. Estrutura de Arquivos

O projeto segue uma estrutura modular para facilitar a manutenção e os testes:

```
Quizito/
├── quiz_app/
│   ├── modelos.py          # Classes de POO (Pergunta, Quiz, Usuario, Tentativa, Dificuldade)
│   ├── dados.py            # Funções de persistência (salvar/carregar JSON, incluindo tentativas)
│   ├── relatorios.py       # Módulo para geração de relatórios
│   └── cli.py              # Interface de linha de comando (criação e execução de quizzes)
├── tests/
│   ├── test_modelos.py     # Testes unitários para as classes e regras de negócio
│   └── test_dados.py       # Testes para a persistência
├── settings.json           # Arquivo de configurações (pesos de pontuação, limites)
├── main.py                 # Ponto de entrada da aplicação
└── README.md               # Documentação do projeto
```

## 3. Modelagem Orientada a Objetos

### 3.1. Classes e Atributos

As classes foram implementadas com foco em **encapsulamento** e **imutabilidade** para garantir a integridade dos dados.

| Classe | Atributo | Tipo | Descrição | Destaque POO |
| :--- | :--- | :--- | :--- | :--- |
| **Dificuldade** | FACIL, MEDIO, DIFÍCIL | Enum | Níveis de dificuldade válidos. | Encapsulamento de valores fixos. |
| **Pergunta** | enunciado | str | O texto da pergunta. | **Classe Base Abstrata** |
| | dificuldade | Dificuldade | Nível de dificuldade da pergunta. | |
| | tema | str | Tema ao qual a pergunta pertence. | |
| **PerguntaMultiplaEscolha** | alternativas | tuple[str] | Tupla de 3 a 5 opções de resposta. | **Herança de Pergunta** |
| | indice_correto | int | Índice da alternativa correta (0 a N-1). | **Validação via @property** |
| **PerguntaVerdadeiroFalso** | resposta_correta | bool | Resposta correta (True para Verdadeiro, False para Falso). | **Herança de Pergunta** |
| **Quiz** | titulo | str | Título do quiz. | |
| | perguntas | tuple[Pergunta] | Tupla de objetos Pergunta. | **Composição e Imutabilidade (Tupla)** |
| | max_tentativas | int | Número máximo de tentativas permitidas. | |
| | tempo_limite_min | int (opcional) | Tempo máximo em minutos. | |
| **Usuario** | nome, email | str | Dados de identificação. | **Getters via @property** |
| | tentativas | tuple[Tentativa] | Histórico de tentativas. | **Composição e Imutabilidade (Tupla)** |
| **Tentativa** | quiz, usuario | Quiz, Usuario | Referências aos objetos relacionados. | **Getters via @property** |
| | respostas | dict[int, Union[int, bool]] | Mapeamento Índice Pergunta -> Resposta (índice para ME, bool para VF). | **Suporte a Múltiplos Tipos** |
| | pontuacao_obtida | int | Pontuação final alcançada. | |
| | tempo_gasto_seg | int | Tempo total gasto em segundos. | |
| | concluida | bool | Indica se a tentativa foi concluída. | |
| **Cronometro** | _inicio | float | Timestamp do início da contagem. | **Classe Utilitária** |

### 3.2. Métodos Principais

| Classe | Método | Propósito | Destaque POO |
| :--- | :--- | :--- | :--- |
| **Pergunta** | `verificar_resposta` | Método abstrato para verificar a resposta. | **Método Abstrato** |
| | `__str__` | Exibição da pergunta COM gabarito (para revisão). | **Método Especial** |
| | `exibir_para_quiz` | Exibição da pergunta SEM resposta correta (durante quiz). | **Método Especial** |
| | `__eq__` | Comparação por enunciado e tema. | **Método Especial** |
| **PerguntaMultiplaEscolha** | `__init__` | Construtor que utiliza os *setters* para validação inicial. | **Herança** |
| | `@property` / `.setter` | Validação de dados (alternativas, índice correto). | **Encapsulamento** |
| | `__str__` | Exibição com a resposta marcada como (CORRETA). | **Método Especial** |
| | `exibir_para_quiz` | Exibição sem indicar qual alternativa é correta. | **Método Especial** |
| **PerguntaVerdadeiroFalso** | `__init__` | Construtor que utiliza o *setter* para validação. | **Herança** |
| | `@property` / `.setter` | Validação de dados (resposta_correta). | **Encapsulamento** |
| | `__str__` | Exibição com indicação (CORRETA: VERDADEIRO/FALSO). | **Método Especial** |
| | `exibir_para_quiz` | Exibição sem indicar se é verdadeiro ou falso. | **Método Especial** |
| **Usuario** | `pode_tentar` | Verifica se o limite de tentativas foi atingido. | **Regra de Negócio** |
| | `adicionar_tentativa` | Adiciona Tentativa ao histórico, validando se está concluída. | **Regra de Negócio** |
| | `gerar_relatorio_usuario` | Gera relatório consolidado de todas as tentativas. | **Relatório** |
| **Quiz** | `adicionar_pergunta` | Adiciona pergunta, garantindo a unicidade. | |
| | `calcular_pontuacao_maxima` | Calcula a pontuação com base nos pesos de dificuldade. | **Regra de Negócio** |
| | `__len__`, `__iter__` | Permite usar `len()` e iterar sobre as perguntas. | **Métodos Especiais** |
| **Persistência** | `carregar_configuracoes` | Carrega pesos e limites do `settings.json`. | |
| | `salvar_quiz`, `carregar_quiz` | Salva e carrega objetos Quiz em JSON. | **Persistência Básica** |
| | `salvar_usuarios`, `carregar_usuarios` | Salva e carrega objetos Usuario em JSON. | **Persistência Básica** |
| | `salvar_tentativas`, `carregar_tentativas` | Salva e carrega o histórico de Tentativas, associando-as aos objetos Quiz e Usuário. | **Persistência de Histórico** |
| | `serializar_objeto`, `desserializar_objeto` | Conversão de objetos para/de dicionários JSON com flags `__class__` e `__enum__`. | **Serialização Customizada** |
| **Tentativa** | `registrar_resposta` | Registra a escolha do usuário, validando o tipo de resposta. | |
| | `finalizar_tentativa` | Calcula a pontuação e marca como concluída. | **Lógica de Negócio** |
| | `obter_gabarito` | Retorna um resumo detalhado das respostas e acertos. | |
| | `gerar_resumo_tentativa` | Gera estatísticas da tentativa (percentual, tempo, etc). | **Relatório** |
| **Cronometro** | `tempo_decorrido_seg` | Retorna o tempo decorrido em segundos. | **Encapsulamento (@property)** |
| | `tempo_decorrido_min` | Retorna o tempo decorrido em minutos. | **Encapsulamento (@property)** |

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
**Status:** Controle de tentativas, tempo limite e pontuação ponderada. CLI mínima funcional. (Semana 4)
