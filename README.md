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
| **Relatórios** | `gerar_relatorio_alunos_por_turma` | Agrupa e lista usuários por turma. | **Funcionalidade de Gestão** |
| | `export_relatorio_alunos_por_turma_json` | Exporta o relatório de alunos por turma para JSON. | **Exportação de Dados** |
| | `gerar_relatorio_consolidado` | Gera ranking geral, desempenho por tema e taxa de acerto global. | **Análise de Desempenho** |
| | `export_relatorio_consolidado_json` | Exporta o relatório consolidado para JSON. | **Exportação de Dados** |
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


## 4. Como Executar

O projeto Quizito é uma aplicação de linha de comando (CLI) desenvolvida em Python.

### 4.1. Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado em seu sistema.

### 4.2. Instalação

Como o projeto utiliza apenas bibliotecas padrão do Python, não é necessário instalar dependências adicionais via `pip`.

1.  **Clone o repositório** (ou descompacte o arquivo do projeto):
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd Quizito
    ```

### 4.3. Execução

Execute o arquivo principal `main.py` diretamente:

```bash
python3 main.py
```

Isso iniciará o menu principal da aplicação, onde você poderá selecionar um usuário, executar quizzes, gerenciar perguntas e acessar os relatórios.


## 5. Exemplos de Uso (Interação CLI)

A aplicação é totalmente orientada por menus de texto. Abaixo estão exemplos de como interagir com as principais funcionalidades.

### 5.1. Menu Principal

Ao executar `python3 main.py`, o menu principal é exibido:

```
--- Quizito CLI ---
[1] Iniciar Quiz
[2] Selecionar/Cadastrar Usuário
[3] Gerenciar Quizzes
[4] Relatórios
[5] Sair
Escolha uma opção:
```

### 5.2. Executando um Quiz

1.  Selecione **[1] Iniciar Quiz**.
2.  Selecione o quiz desejado (ex: `[0] Quiz de Exemplo`).
3.  Selecione o usuário (ou cadastre um novo).
4.  O quiz será iniciado, e o tempo será cronometrado.

### 5.3. Gerenciando Quizzes (Criação de Pergunta)

1.  Selecione **[3] Gerenciar Quizzes** no menu principal.
2.  Selecione **[2] Adicionar Pergunta** ao quiz ativo.
3.  Escolha o tipo de pergunta (ex: `[1] Múltipla Escolha`).
4.  Siga as instruções para preencher o enunciado, tema, dificuldade, alternativas e índice correto.

### 5.4. Exportando Relatórios

1.  Selecione **[4] Relatórios** no menu principal.
2.  Para exportar o relatório consolidado, selecione **[4] Relatório Consolidado (Exportar JSON)**.
3.  Informe o caminho do arquivo (ex: `rel_consolidado.json`).

```
--- Relatórios ---
[1] Alunos por Turma (Imprimir)
[2] Alunos por Turma (Exportar JSON)
[3] Relatório Consolidado (Imprimir)
[4] Relatório Consolidado (Exportar JSON)
[5] Voltar
Escolha uma opção: 4
Caminho para salvar JSON (ex: rel_consolidado.json): relatorios/desempenho_geral.json
Relatório salvo em relatorios/desempenho_geral.json
```

---
**Desenvolvido por:** David Josué Vital Santos
**Instituição:** Universidade Federal do Cariri (UFCA)
**Disciplina:** Programação Orientada a Objetos (POO)
**Status:** Implementação completa da CLI com controle de tentativas, tempo limite, pontuação ponderada e relatórios consolidados de desempenho.
