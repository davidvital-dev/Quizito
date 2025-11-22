from enum import Enum
from typing import List, Optional, Dict, Tuple, Any

class Dificuldade(Enum):
    """Define os níveis de dificuldade válidos para as perguntas."""
    FACIL = "FÁCIL"
    MEDIO = "MÉDIO"
    DIFICIL = "DIFÍCIL"

class Pergunta:
    """
    Representa uma pergunta de múltipla escolha.
    Valida integridade dos dados (3-5 alternativas, índice válido).
    """
    def __init__(self, enunciado: str, alternativas: List[str], indice_correto: int, 
                 dificuldade: Dificuldade, tema: str):
        self._enunciado = enunciado
        self._dificuldade = dificuldade
        self._tema = tema
        
        # Inicializa variáveis internas antes da validação
        self._alternativas: List[str] = []
        self._indice_correto: int = -1 
        
        # Usa os setters para validação inicial
        self.alternativas = alternativas
        self.indice_correto = indice_correto

    @property
    def enunciado(self) -> str:
        return self._enunciado

    @property
    def alternativas(self) -> Tuple[str, ...]:
        """Retorna uma tupla para impedir modificação direta da lista."""
        return tuple(self._alternativas)

    @alternativas.setter
    def alternativas(self, novas_alternativas: List[str]):
        if not (3 <= len(novas_alternativas) <= 5):
            raise ValueError("Uma pergunta deve ter entre 3 e 5 alternativas.")
        self._alternativas = list(novas_alternativas) # Cria cópia defensiva
        
        # Se o índice atual estiver fora dos novos limites, invalida-o
        if not (0 <= self._indice_correto < len(self._alternativas)):
             self._indice_correto = -1 

    @property
    def indice_correto(self) -> int:
        return self._indice_correto

    @indice_correto.setter
    def indice_correto(self, novo_indice: int):
        if not self._alternativas:
             # Permite setar -1 se não houver alternativas, mas bloqueia outros índices
             if novo_indice == -1: 
                 self._indice_correto = -1
                 return
             raise ValueError("Defina as alternativas antes do índice correto.")

        if not (0 <= novo_indice < len(self._alternativas)):
            raise ValueError(f"Índice {novo_indice} inválido para {len(self._alternativas)} alternativas.")
        self._indice_correto = novo_indice

    @property
    def dificuldade(self) -> Dificuldade:
        return self._dificuldade

    @property
    def tema(self) -> str:
        return self._tema

    def verificar_resposta(self, indice_resposta: int) -> bool:
        return indice_resposta == self._indice_correto

    def __str__(self) -> str:
        alternativas_str = "\n".join([f"[{i}] {alt}{' (CORRETA)' if i == self._indice_correto else ''}" 
                                      for i, alt in enumerate(self._alternativas)])
        return (f"[{self._tema}] ({self._dificuldade.value})\n"
                f"{self._enunciado}\n{alternativas_str}")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Pergunta):
            return NotImplemented
        return (self._enunciado == other._enunciado and 
                self._tema == other._tema)

class Quiz:
    """
    Agregador de perguntas.
    Garante unicidade de perguntas e configurações do teste.
    """
    def __init__(self, titulo: str, perguntas: Optional[List[Pergunta]] = None, 
                 max_tentativas: int = 1, tempo_limite_min: Optional[int] = None):
        self._titulo = titulo
        self._perguntas: List[Pergunta] = []
        self._max_tentativas = max_tentativas
        self._tempo_limite_min = tempo_limite_min
        
        if perguntas:
            for p in perguntas:
                self.adicionar_pergunta(p)

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def perguntas(self) -> Tuple[Pergunta, ...]:
        """Retorna tupla (imutável) para evitar append externo sem validação."""
        return tuple(self._perguntas)

    @property
    def max_tentativas(self) -> int:
        return self._max_tentativas

    def adicionar_pergunta(self, pergunta: Pergunta):
        if pergunta in self._perguntas:
            raise ValueError(f"Pergunta duplicada no quiz '{self._titulo}': {pergunta.enunciado}")
        self._perguntas.append(pergunta)

    def calcular_pontuacao_maxima(self, pesos: Dict[str, int]) -> int:
        return sum(pesos.get(p.dificuldade.value, 0) for p in self._perguntas)

    def __len__(self) -> int:
        return len(self._perguntas)

    def __iter__(self):
        return iter(self._perguntas)

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