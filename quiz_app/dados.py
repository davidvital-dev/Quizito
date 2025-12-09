import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from quiz_app.modelos import Pergunta, PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso, Quiz, Usuario, Tentativa, Dificuldade, Cronometro



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
        }

    if isinstance(obj, Tentativa):
        return {
            "__class__": "Tentativa",
            "quiz_titulo": obj.quiz.titulo,
            "usuario_email": obj.usuario.email,
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
            perguntas = [desserializar_objeto(p) for p in data["perguntas"]]
            quiz = Quiz(
                titulo=data["titulo"],
                perguntas=perguntas,
                max_tentativas=data["max_tentativas"],
                tempo_limite_min=data["tempo_limite_min"]
            )
            return quiz

        if class_name == "Usuario":
            return Usuario(
                nome=data["nome"],
                email=data["email"]
            )
        if class_name == "Tentativa":
            return data

    return data



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
        return [desserializar_objeto(d) if isinstance(d, dict) and '__class__' in d else d for d in dados]
    elif isinstance(dados, dict):
        return desserializar_objeto(dados)
    return dados

def carregar_configuracoes(caminho: Path) -> Dict[str, Any]:
    """Carrega as configurações do settings.json."""
    if not caminho.exists():
        print(f"Aviso: Arquivo de configurações não encontrado em {caminho}. Usando valores padrão.")
        return {
            "DURACAO_PADRAO_QUIZ_MIN": 10,
            "MAX_TENTATIVAS_PADRAO": 3,
            "PESOS_DIFICULDADE": {
                "FÁCIL": 1,
                "MÉDIO": 2,
                "DIFÍCIL": 3
            }
        }
    
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)



def salvar_quizes(quizes: List[Quiz], caminho: Path):
    """Salva uma lista de objetos Quiz."""
    quizes_serializaveis = [serializar_objeto(q) for q in quizes]
    salvar_dados(caminho, quizes_serializaveis)

def carregar_quizes(caminho: Path) -> List[Quiz]:
    """Carrega uma lista de objetos Quiz."""
    dados = carregar_dados(caminho)
    if dados is None:
        return []
    
    return [q for q in dados if isinstance(q, Quiz)]

def salvar_usuarios(usuarios: List[Usuario], caminho: Path):
    """Salva uma lista de objetos Usuario."""
    usuarios_serializaveis = [serializar_objeto(u) for u in usuarios]
    salvar_dados(caminho, usuarios_serializaveis)

def carregar_usuarios(caminho: Path) -> List[Usuario]:
    """Carrega uma lista de objetos Usuario."""
    dados = carregar_dados(caminho)
    if dados is None:
        return []

    return [u for u in dados if isinstance(u, Usuario)]

def salvar_tentativas(tentativas: List[Tentativa], caminho: Path):
    """Salva uma lista de objetos Tentativa."""
    tentativas_serializaveis = [serializar_objeto(t) for t in tentativas]
    salvar_dados(caminho, tentativas_serializaveis)

def carregar_tentativas(caminho: Path, quizzes: List[Quiz], usuarios: List[Usuario]) -> List[Tentativa]:
    """Carrega tentativas e as associa aos respectivos Quiz e Usuario."""
    dados = carregar_dados(caminho)
    if dados is None:
        return []
    
    tentativas_carregadas = []
    
    quizzes_map = {q.titulo: q for q in quizzes}
    usuarios_map = {u.email: u for u in usuarios}
    
    for d in dados:
        if isinstance(d, dict) and d.get('__class__') == 'Tentativa':
            quiz_titulo = d.get('quiz_titulo')
            usuario_email = d.get('usuario_email')
            
            quiz = quizzes_map.get(quiz_titulo)
            usuario = usuarios_map.get(usuario_email)
            
            if quiz and usuario:
                tentativa = Tentativa(quiz=quiz, usuario=usuario)
                tentativa._respostas = d.get('respostas', {})
                tentativa._pontuacao_obtida = d.get('pontuacao_obtida', 0)
                tentativa._tempo_gasto_seg = d.get('tempo_gasto_seg', 0)
                tentativa._concluida = d.get('concluida', False)
                
                if tentativa.concluida:
                    usuario._tentativas.append(tentativa)
                
                tentativas_carregadas.append(tentativa)
                
    return tentativas_carregadas