from enum import Enum
from typing import List, Optional, Dict, Tuple, Any
import time
from abc import ABC, abstractmethod 

class Dificuldade(Enum):
    """Define os níveis de dificuldade válidos para as perguntas."""
    FACIL = "FÁCIL"
    MEDIO = "MÉDIO"
    DIFICIL = "DIFÍCIL"

class Pergunta(ABC): 
    """
    Classe base abstrata para todos os tipos de perguntas.
    """
    def __init__(self, enunciado: str, dificuldade: Dificuldade, tema: str):
        self._enunciado = enunciado
        self._dificuldade = dificuldade
        self._tema = tema

    @property
    def enunciado(self) -> str:
        return self._enunciado

    @property
    def dificuldade(self) -> Dificuldade:
        return self._dificuldade

    @property
    def tema(self) -> str:
        return self._tema

    @abstractmethod
    def verificar_resposta(self, resposta: Any) -> bool:
        """Verifica se a resposta fornecida está correta."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Representação em string da pergunta (com gabarito)."""
        pass

    @abstractmethod
    def exibir_para_quiz(self) -> str:
        """Exibe a pergunta para o quiz (SEM mostrar a resposta correta)."""
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Pergunta):
            return NotImplemented
        
        return (self._enunciado == other._enunciado and 
                self._tema == other._tema)

class PerguntaVerdadeiroFalso(Pergunta): 
    """
    Representa uma pergunta de Verdadeiro ou Falso.
    """
    def __init__(self, enunciado: str, resposta_correta: bool, 
                 dificuldade: Dificuldade, tema: str):
        super().__init__(enunciado, dificuldade, tema)
        self._resposta_correta = resposta_correta

    @property
    def resposta_correta(self) -> bool:
        return self._resposta_correta

    def verificar_resposta(self, resposta: bool) -> bool:
        """Verifica se a resposta fornecida (True/False) está correta."""
        return resposta == self._resposta_correta

    def __str__(self) -> str:
        """Exibição com gabarito (mostra resposta correta)."""
        status = "VERDADEIRO" if self._resposta_correta else "FALSO"
        return (f"[{self.tema}] ({self.dificuldade.value})\n"
                f"{self.enunciado}\n"
                f"[V] Verdadeiro | [F] Falso (CORRETA: {status})")

    def exibir_para_quiz(self) -> str:
        """Exibição para o quiz (SEM mostrar resposta correta)."""
        return (f"[{self.tema}] ({self.dificuldade.value})\n"
                f"{self.enunciado}\n"
                f"[V] Verdadeiro | [F] Falso")

class PerguntaMultiplaEscolha(Pergunta): 
    """
    Representa uma pergunta de múltipla escolha.
    Valida integridade dos dados (3-5 alternativas, índice válido).
    """
    def __init__(self, enunciado: str, alternativas: List[str], indice_correto: int, 
                 dificuldade: Dificuldade, tema: str):
        super().__init__(enunciado, dificuldade, tema) 
        
        self._alternativas: List[str] = []
        self._indice_correto: int = -1 
        self.alternativas = alternativas
        self.indice_correto = indice_correto

    @property
    def alternativas(self) -> Tuple[str, ...]:
        """Retorna uma tupla para impedir modificação direta da lista."""
        return tuple(self._alternativas)

    @alternativas.setter
    def alternativas(self, novas_alternativas: List[str]):
        if not (3 <= len(novas_alternativas) <= 5):
            raise ValueError("Uma pergunta deve ter entre 3 e 5 alternativas.")
        self._alternativas = list(novas_alternativas) 
        
        
        if not (0 <= self._indice_correto < len(self._alternativas)):
             self._indice_correto = -1 

    @property
    def indice_correto(self) -> int:
        return self._indice_correto

    @indice_correto.setter
    def indice_correto(self, novo_indice: int):
        if not self._alternativas:
             
             if novo_indice == -1: 
                 self._indice_correto = -1
                 return
             raise ValueError("Defina as alternativas antes do índice correto.")

        if not (0 <= novo_indice < len(self._alternativas)):
            raise ValueError(f"Índice {novo_indice} inválido para {len(self._alternativas)} alternativas.")
        self._indice_correto = novo_indice

    def verificar_resposta(self, indice_resposta: int) -> bool:
        """Implementação do método abstrato."""
        return indice_resposta == self._indice_correto

    def __str__(self) -> str:
        """Exibição com gabarito (mostra resposta correta)."""
        alternativas_str = "\n".join([f"[{i}] {alt}{' (CORRETA)' if i == self._indice_correto else ''}" 
                                      for i, alt in enumerate(self._alternativas)])
        return (f"[{self.tema}] ({self.dificuldade.value})\n"
                f"{self.enunciado}\n{alternativas_str}")

    def exibir_para_quiz(self) -> str:
        """Exibição para o quiz (SEM mostrar resposta correta)."""
        alternativas_str = "\n".join([f"[{i}] {alt}" 
                                      for i, alt in enumerate(self._alternativas)])
        return (f"[{self.tema}] ({self.dificuldade.value})\n"
                f"{self.enunciado}\n{alternativas_str}")

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
    Participante do sistema. Mantém histórico de tentativas.
    """
    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email
        self._tentativas: List['Tentativa'] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    @property
    def tentativas(self) -> Tuple['Tentativa', ...]:
        """Retorna histórico imutável."""
        return tuple(self._tentativas)

    def adicionar_tentativa(self, tentativa: 'Tentativa'):
        if not tentativa.concluida:
             raise ValueError("Apenas tentativas concluídas devem ir para o histórico.")
        self._tentativas.append(tentativa)

    def __str__(self) -> str:
        return f"{self._nome} ({self._email}) | Histórico: {len(self._tentativas)} quizzes"

    
    def pode_tentar(self, quiz: Quiz) -> bool:
        """Verifica se o usuário pode realizar o quiz com base no limite de tentativas."""
        if quiz.max_tentativas is None:
            return True # Sem limite
        tentativas_concluidas = 0
        for tentativa in self._tentativas:
            # Compara o quiz pelo título para simplificar, mas o ideal seria por um ID único
            if tentativa.quiz.titulo == quiz.titulo and tentativa.concluida:
                tentativas_concluidas += 1
        return tentativas_concluidas < quiz.max_tentativas

    def gerar_relatorio_usuario(self, pesos: Dict[str, int]) -> Dict[str, Any]:
        """Gera um relatório consolidado de todas as tentativas do usuário."""
        relatorio = {
            "nome": self.nome,
            "matricula_id": self.matricula_id,
            "total_tentativas": len(self._tentativas),
            "resumos_tentativas": []
        }
        
        for tentativa in self._tentativas:
            relatorio["resumos_tentativas"].append(tentativa.gerar_resumo_tentativa(pesos))
            
        return relatorio

class Tentativa:
    """
    Sessão de resolução de um Quiz.
    """
    def __init__(self, quiz: Quiz, usuario: Usuario):
        self._quiz = quiz
        self._usuario = usuario
        self._respostas: Dict[int, Any] = {} 
        self._pontuacao_obtida = 0
        self._tempo_gasto_seg = 0
        self._concluida = False

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def concluida(self) -> bool:
        return self._concluida

    @property
    def pontuacao_obtida(self) -> int:
        return self._pontuacao_obtida

    def registrar_resposta(self, indice_pergunta: int, resposta: Any):
        if self._concluida:
            raise RuntimeError("Tentativa já finalizada. Não é possível alterar respostas.")
        
        
        perguntas = self._quiz.perguntas 
        if not (0 <= indice_pergunta < len(perguntas)):
            raise IndexError("Índice da pergunta inválido.")
        
        pergunta_atual = perguntas[indice_pergunta]
        
        
        if isinstance(pergunta_atual, PerguntaMultiplaEscolha):
            if not isinstance(resposta, int) or not (0 <= resposta < len(pergunta_atual.alternativas)):
                raise ValueError("Resposta inválida para PerguntaMultiplaEscolha (deve ser um índice válido).")
        
        
        elif isinstance(pergunta_atual, PerguntaVerdadeiroFalso):
            if not isinstance(resposta, bool):
                raise ValueError("Resposta inválida para PerguntaVerdadeiroFalso (deve ser True ou False).")
        
        
        
        self._respostas[indice_pergunta] = resposta

    def finalizar_tentativa(self, tempo_gasto_seg: int, pesos: Dict[str, int]):
        if self._concluida:
            return 

        self._tempo_gasto_seg = tempo_gasto_seg
        self._pontuacao_obtida = self._calcular_pontuacao(pesos)
        self._concluida = True

    def _calcular_pontuacao(self, pesos: Dict[str, int]) -> int:
        pontuacao = 0
        perguntas = self._quiz.perguntas
        for i, pergunta in enumerate(perguntas):
            resp_user = self._respostas.get(i)
            if resp_user is not None and pergunta.verificar_resposta(resp_user):
                pontuacao += pesos.get(pergunta.dificuldade.value, 0)
        return pontuacao

    def obter_gabarito(self) -> List[Dict[str, Any]]:
        gabarito = []
        perguntas = self._quiz.perguntas
        for i, pergunta in enumerate(perguntas):
            resp_user = self._respostas.get(i)
            acertou = (resp_user is not None and pergunta.verificar_resposta(resp_user))
            
            sua_resposta_str = None
            correta_str = "N/A"

            if isinstance(pergunta, PerguntaMultiplaEscolha):
                if resp_user is not None:
                    sua_resposta_str = pergunta.alternativas[resp_user]
                correta_str = pergunta.alternativas[pergunta.indice_correto]
            elif isinstance(pergunta, PerguntaVerdadeiroFalso):
                if resp_user is not None:
                    sua_resposta_str = "VERDADEIRO" if resp_user else "FALSO"
                correta_str = "VERDADEIRO" if pergunta.resposta_correta else "FALSO"

            gabarito.append({
                "enunciado": pergunta.enunciado,
                "sua_resposta": sua_resposta_str,
                "correta": correta_str,
                "acertou": acertou
            })
        return gabarito

    def gerar_resumo_tentativa(self, pesos: Dict[str, int]) -> Dict[str, Any]:
        """Gera um resumo estatístico da tentativa."""
        max_pontuacao = self._quiz.calcular_pontuacao_maxima(pesos)
        
        acertos = 0
        erros = 0
        
        for item in self.obter_gabarito():
            if item['acertou']:
                acertos += 1
            else:
                erros += 1
                
        return {
            "quiz_titulo": self._quiz.titulo,
            "pontuacao_obtida": self._pontuacao_obtida,
            "pontuacao_maxima": max_pontuacao,
            "percentual_acerto": (acertos / len(self._quiz.perguntas)) * 100 if len(self._quiz.perguntas) > 0 else 0,
            "tempo_gasto_seg": self._tempo_gasto_seg,
            "acertos": acertos,
            "erros": erros,
            "concluida": self._concluida
        }

class Cronometro:
    """
    Classe utilitária para medir o tempo decorrido.
    """
    def __init__(self):
        self._inicio = time.time()

    @property
    def tempo_decorrido_seg(self) -> int:
        """Retorna o tempo decorrido em segundos (arredondado para baixo)."""
        return int(time.time() - self._inicio)

    @property
    def tempo_decorrido_min(self) -> float:
        """Retorna o tempo decorrido em minutos."""
        return self.tempo_decorrido_seg / 60.0