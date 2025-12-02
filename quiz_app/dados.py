import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from quiz_app.modelos import Pergunta, PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso, Quiz, Usuario, Tentativa, Dificuldade

# --- Funções Auxiliares de Serialização/Desserialização ---

def serializar_objeto(obj: Any) -> Dict[str, Any]:
    """Converte um objeto do modelo em um dicionário serializável para JSON."""
    if isinstance(obj, Dificuldade):
        return {"__enum__": "Dificuldade", "value": obj.value}
    
    if isinstance(obj, PerguntaMultiplaEscolha):
        return {
            "__class__": "PerguntaMultiplaEscolha",
            "enunciado": obj.enunciado,
            "dificuldade": serializar_objeto(obj.dificuldade),
            "tema": obj.tema,
            "alternativas": list(obj.alternativas),
            "indice_correto": obj.indice_correto
        }
    
    if isinstance(obj, PerguntaVerdadeiroFalso):
        return {
            "__class__": "PerguntaVerdadeiroFalso",
            "enunciado": obj.enunciado,
            "dificuldade": serializar_objeto(obj.dificuldade),
            "tema": obj.tema,
            "resposta_correta": obj.resposta_correta
        }
    
    if isinstance(obj, Quiz):
        return {
            "__class__": "Quiz",
            "titulo": obj.titulo,
            "perguntas": [serializar_objeto(p) for p in obj.perguntas],
            "max_tentativas": obj.max_tentativas,
            "tempo_limite_min": obj._tempo_limite_min 
        }

    if isinstance(obj, Usuario):
      
        return {
            "__class__": "Usuario",
            "nome": obj.nome,
            "email": obj.email,
            "matricula_id": obj.matricula_id,
            # O histórico de tentativas será carregado separadamente
        }

    if isinstance(obj, Tentativa):
        return {
            "__class__": "Tentativa",
            "quiz_titulo": obj.quiz.titulo,
            "usuario_id": obj.usuario.matricula_id,
            "respostas": obj._respostas, 
            "pontuacao_obtida": obj.pontuacao_obtida,
            "tempo_gasto_seg": obj._tempo_gasto_seg,
            "concluida": obj.concluida
        }

    raise TypeError(f"Objeto do tipo {type(obj)} não serializável.")

def desserializar_objeto(data: Dict[str, Any]) -> Any:
    """Converte um dicionário de volta para um objeto do modelo."""
    if "__enum__" in data:
        if data["__enum__"] == "Dificuldade":
            return Dificuldade(data["value"])
    
    if "__class__" in data:
        class_name = data["__class__"]
        
        if class_name == "PerguntaMultiplaEscolha":
            return PerguntaMultiplaEscolha(
                enunciado=data["enunciado"],
                dificuldade=desserializar_objeto(data["dificuldade"]),
                tema=data["tema"],
                alternativas=data["alternativas"],
                indice_correto=data["indice_correto"]
            )
        
        if class_name == "PerguntaVerdadeiroFalso":
            return PerguntaVerdadeiroFalso(
                enunciado=data["enunciado"],
                dificuldade=desserializar_objeto(data["dificuldade"]),
                tema=data["tema"],
                resposta_correta=data["resposta_correta"]
            )
        
        if class_name == "Quiz":
            # As perguntas são desserializadas recursivamente
            perguntas = [desserializar_objeto(p) for p in data["perguntas"]]
            quiz = Quiz(
                titulo=data["titulo"],
                perguntas=perguntas,
                max_tentativas=data["max_tentativas"],
                tempo_limite_min=data["tempo_limite_min"]
            )
            return quiz

        if class_name == "Usuario":
            # Cria o usuário sem as tentativas (serão carregadas separadamente)
            return Usuario(
                nome=data["nome"],
                email=data["email"],
                matricula_id=data["matricula_id"]
            )
        if class_name == "Tentativa":
            return data # Retorna o dicionário para ser tratado pela função de carregamento de histórico

    return data

# --- Funções de I/O ---

def salvar_dados(caminho: Path, dados: Any):
    """Salva dados serializáveis em um arquivo JSON."""
    caminho.parent.mkdir(parents=True, exist_ok=True)

    dados_serializaveis = serializar_objeto(dados) if not isinstance(dados, (list, dict)) else dados
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados_serializaveis, f, ensure_ascii=False, indent=4)

def carregar_dados(caminho: Path) -> Any:
    """Carrega dados de um arquivo JSON e tenta desserializar para objetos do modelo."""
    if not caminho.exists():
        return None
    
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    if isinstance(dados, list):
        return dados
    elif isinstance(dados, dict):
        return desserializar_objeto(dados)
    return dados

# --- Funções Específicas de Persistência ---

def salvar_quiz(quiz: Quiz, caminho: Path):
    """Salva um único objeto Quiz."""
    salvar_dados(caminho, quiz)

def carregar_quiz(caminho: Path) -> Optional[Quiz]:
    """Carrega um único objeto Quiz."""
    return carregar_dados(caminho)

def salvar_usuarios(usuarios: List[Usuario], caminho: Path):
    """Salva uma lista de objetos Usuario."""
    usuarios_serializaveis = [serializar_objeto(u) for u in usuarios]
    salvar_dados(caminho, usuarios_serializaveis)

def carregar_usuarios(caminho: Path) -> List[Usuario]:
    """Carrega uma lista de objetos Usuario."""
    dados = carregar_dados(caminho)
    if dados is None:
        return []
    return [desserializar_objeto(d) for d in dados if isinstance(d, dict)]
