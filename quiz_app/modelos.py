from enum import Enum

class Dificuldade(Enum):
    """Define os níveis de dificuldade válidos para as perguntas."""
    FACIL = "FÁCIL"
    MEDIO = "MÉDIO"
    DIFICIL = "DIFÍCIL"

class Pergunta:
    """
    Representa uma única pergunta de múltipla escolha no sistema.
    
    Responsável por armazenar o enunciado, alternativas, a resposta correta,
    o nível de dificuldade e o tema. Implementa validações via @property
    para garantir a integridade dos dados.
    """
    pass

class Quiz:
    """
    Representa um conjunto de perguntas (Composição).
    
    Responsável por agregar objetos Pergunta, calcular a pontuação máxima
    e gerenciar configurações como tempo limite e número máximo de tentativas.
    """
    pass

class Usuario:
    """
    Representa um usuário (participante) do sistema.
    
    Responsável por armazenar dados de identificação e manter o histórico
    de todas as Tentativas realizadas (Composição).
    """
    pass

class Tentativa:
    """
    Representa uma única sessão de resposta de um Quiz por um Usuário.
    
    Responsável por registrar as respostas, calcular a pontuação obtida,
    o tempo gasto e o status de conclusão da tentativa.
    """
    pass