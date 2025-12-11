import os
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quiz_app.modelos import Quiz, Usuario, Tentativa, Dificuldade, PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso, Cronometro
from quiz_app.dados import carregar_quizes, salvar_quizes, carregar_usuarios, salvar_usuarios, carregar_configuracoes, carregar_tentativas, salvar_tentativas


QUIZ_PATH = Path("quiz.json")
USUARIOS_PATH = Path("usuarios.json")
TENTATIVAS_PATH = Path("tentativas.json")
SETTINGS_PATH = Path("settings.json")


CONFIGURACOES: Dict[str, Any] = {}
QUIZES: List[Quiz] = []
USUARIOS: List[Usuario] = []
TENTATIVAS: List[Tentativa] = []



def limpar_tela():

    os.system('cls' if os.name == 'nt' else 'clear')

def obter_entrada(prompt: str, tipo: type = str, validacao: Optional[Any] = None, default: Optional[Any] = None) -> Any:

    while True:
        try:
            entrada = input(prompt).strip()
            if not entrada and default is not None:
                return default
            if not entrada:
                raise ValueError("A entrada não pode ser vazia.")
            
            
            if tipo == int:
                valor = int(entrada)
            elif tipo == bool:
                if entrada.upper() in ('V', 'VERDADEIRO'):
                    valor = True
                elif entrada.upper() in ('F', 'FALSO'):
                    valor = False
                else:
                    raise ValueError("Entrada deve ser 'V' ou 'F'.")
            else:
                valor = entrada
            
            if validacao and not validacao(valor):
                raise ValueError("Entrada inválida. Tente novamente.")
                
            return valor
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception:
            print("Erro de entrada. Tente novamente.")



def carregar_dados_iniciais():
    global CONFIGURACOES, QUIZES, USUARIOS, TENTATIVAS
    
    CONFIGURACOES = carregar_configuracoes(SETTINGS_PATH)
    
    QUIZES = carregar_quizes(QUIZ_PATH)
    if not QUIZES:
        print("Aviso: Arquivo de quizzes não encontrado. Criando um quiz de exemplo.")
        p1 = PerguntaMultiplaEscolha("Qual a capital da França?", ["Paris", "Londres", "Roma"], 0, Dificuldade.FACIL, "Geografia")
        p2 = PerguntaVerdadeiroFalso("Python é uma linguagem compilada.", False, Dificuldade.MEDIO, "Programação")
        QUIZES.append(Quiz("Quiz de Exemplo", [p1, p2], 
                      max_tentativas=CONFIGURACOES.get("MAX_TENTATIVAS_PADRAO", 3), 
                      tempo_limite_min=CONFIGURACOES.get("DURACAO_PADRAO_QUIZ_MIN", 10)))
        
    USUARIOS = carregar_usuarios(USUARIOS_PATH)
    if not USUARIOS:
        print("Aviso: Arquivo de usuários não encontrado. Criando um usuário de exemplo.")
        USUARIOS.append(Usuario("Visitante", "visitante@quizito.com"))
        
    TENTATIVAS = carregar_tentativas(TENTATIVAS_PATH, QUIZES, USUARIOS)

def salvar_dados_atuais():
    salvar_quizes(QUIZES, QUIZ_PATH)
    salvar_usuarios(USUARIOS, USUARIOS_PATH)
    salvar_tentativas(TENTATIVAS, TENTATIVAS_PATH)

def selecionar_usuario(usuarios: List[Usuario]) -> Usuario:
    print("\n--- Seleção de Usuário ---")
    for i, u in enumerate(usuarios):
        print(f"[{i}] {u.nome} ({u.email}) | Tentativas: {len(u.tentativas)}")
        
    print("[N] Novo Usuário")
    
    while True:
        escolha = input("Selecione o número do usuário ou 'N' para novo: ").strip().upper()
        
        if escolha == 'N':
            print("\n--- Cadastro de Novo Usuário ---")
            nome = obter_entrada("Nome: ")
            email = obter_entrada("Email: ", validacao=lambda e: '@' in e)
            novo_usuario = Usuario(nome, email)
            usuarios.append(novo_usuario)
            salvar_dados_atuais()
            print(f"Usuário {nome} cadastrado e selecionado.")
            return novo_usuario
        
        try:
            indice = int(escolha)
            if 0 <= indice < len(usuarios):
                return usuarios[indice]
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida. Digite o número ou 'N'.")

def executar_quiz(quiz: Quiz, usuario: Usuario):
    limpar_tela()
    print(f"--- Iniciando Quiz: {quiz.titulo} ---")
    print(f"Usuário: {usuario.nome}")
    
    if not usuario.pode_tentar(quiz):
        print(f"\nVocê já atingiu o limite de {quiz.max_tentativas} tentativas para este quiz.")
        input("Pressione Enter para voltar ao menu.")
        return

    tempo_limite_min = quiz._tempo_limite_min if quiz._tempo_limite_min is not None else CONFIGURACOES.get("DURACAO_PADRAO_QUIZ_MIN")
    
    print(f"Tempo Limite: {tempo_limite_min} minutos (0 para sem limite)")
    input("Pressione Enter para começar...")
    
    tentativa = Tentativa(quiz=quiz, usuario=usuario)
    cronometro = Cronometro()
    
    tempo_limite_seg = tempo_limite_min * 60 if tempo_limite_min else None
    
    for i, pergunta in enumerate(quiz.perguntas):
        limpar_tela()
        tempo_decorrido = cronometro.tempo_decorrido_seg
        
        if tempo_limite_seg is not None:
            tempo_restante = tempo_limite_seg - tempo_decorrido
            if tempo_restante <= 0:
                print("\n--- TEMPO ESGOTADO! ---")
                break
            
            minutos = int(tempo_restante // 60)
            segundos = int(tempo_restante % 60)
            tempo_str = f"Tempo Restante: {minutos:02d}:{segundos:02d}"
        else:
            tempo_str = f"Tempo Decorrido: {tempo_decorrido}s"
            
        print(f"Pergunta {i+1} de {len(quiz)} | Tema: {pergunta.tema} | Dificuldade: {pergunta.dificuldade.value}")
        print(tempo_str)
        
        print("-" * 30)
        print(pergunta.exibir_para_quiz())
        print("-" * 30)
        
        
        if isinstance(pergunta, PerguntaMultiplaEscolha):
            validacao = lambda r: isinstance(r, int) and 0 <= r < len(pergunta.alternativas)
            resposta = obter_entrada("Sua resposta (índice): ", tipo=int, validacao=validacao)
        elif isinstance(pergunta, PerguntaVerdadeiroFalso):
            validacao = lambda r: isinstance(r, bool)
            resposta = obter_entrada("Sua resposta (V/F): ", tipo=bool, validacao=validacao)
        else:
            print("Tipo de pergunta desconhecido. Pulando.")
            continue
            
        tentativa.registrar_resposta(indice_pergunta=i, resposta=resposta)

    
    tempo_final = cronometro.tempo_decorrido_seg
    
    if tempo_limite_seg is not None and tempo_final > tempo_limite_seg:
        tempo_final = tempo_limite_seg
        
    tentativa.finalizar_tentativa(tempo_final, CONFIGURACOES.get("PESOS_DIFICULDADE", {}))
    
    TENTATIVAS.append(tentativa)
    if tentativa.concluida:
        usuario.adicionar_tentativa(tentativa)
        
    salvar_dados_atuais() 

    limpar_tela()
    print("--- Quiz Finalizado ---")
    pontuacao_max = quiz.calcular_pontuacao_maxima(CONFIGURACOES.get('PESOS_DIFICULDADE', {}))
    print(f"Pontuação Obtida: {tentativa.pontuacao_obtida} de {pontuacao_max}")

    gabarito = tentativa.obter_gabarito()
    acertos_q = sum(1 for it in gabarito if it.get('acertou'))
    total_q = len(gabarito)
    print(f"Acertos: {acertos_q} de {total_q} perguntas")

    print(f"Tempo Gasto: {tempo_final} segundos")
    
    print("\n--- Gabarito ---")
    for item in tentativa.obter_gabarito():
        status = "ACERTO" if item['acertou'] else "ERRO"
        print(f"[{status}] {item['enunciado']}")
        print(f"  Sua Resposta: {item['sua_resposta']}")
        print(f"  Correta: {item['correta']}")
        
    input("\nPressione Enter para voltar ao menu.")

def criar_pergunta_verdadeiro_falso(quiz_ativo: Quiz) -> Optional[PerguntaVerdadeiroFalso]:
    print("\n--- Criar Pergunta de Verdadeiro ou Falso ---")
    enunciado = obter_entrada("Enunciado da Pergunta: ")
    tema = obter_entrada("Tema da Pergunta: ")
    
    if any(p.enunciado == enunciado and p.tema == tema for p in quiz_ativo.perguntas):
        print("Erro: Já existe uma pergunta com este enunciado e tema no quiz atual.")
        return None
        
    dificuldades = {str(i+1): d for i, d in enumerate(Dificuldade)}
    print("Nível de Dificuldade:")
    for k, v in dificuldades.items():
        print(f"[{k}] {v.value}")
    
    while True:
        escolha_dificuldade = obter_entrada("Escolha o número da dificuldade: ", tipo=str)
        if escolha_dificuldade in dificuldades:
            dificuldade = dificuldades[escolha_dificuldade]
            break
        print("Opção inválida.")
        
    resposta_correta = obter_entrada("Resposta Correta (V/F): ", tipo=bool)
    
    try:
        pergunta = PerguntaVerdadeiroFalso(enunciado, resposta_correta, dificuldade, tema)
        return pergunta
    except ValueError as e:
        print(f"Erro ao criar pergunta: {e}")
        return None


def criar_pergunta_multipla_escolha(quiz_ativo: Quiz) -> Optional[PerguntaMultiplaEscolha]:
    print("\n--- Criar Pergunta de Múltipla Escolha ---")
    enunciado = obter_entrada("Enunciado da Pergunta: ")
    tema = obter_entrada("Tema da Pergunta: ")
    
    if any(p.enunciado == enunciado and p.tema == tema for p in quiz_ativo.perguntas):
        print("Erro: Já existe uma pergunta com este enunciado e tema no quiz atual.")
        return None
        
    dificuldades = {str(i+1): d for i, d in enumerate(Dificuldade)}
    print("Nível de Dificuldade:")
    for k, v in dificuldades.items():
        print(f"[{k}] {v.value}")
    
    while True:
        escolha_dificuldade = obter_entrada("Escolha o número da dificuldade: ", tipo=str)
        if escolha_dificuldade in dificuldades:
            dificuldade = dificuldades[escolha_dificuldade]
            break
        print("Opção inválida.")
        
    alternativas = []
    print("Digite as alternativas (mínimo 3, máximo 5). Digite 'FIM' para terminar.")
    while len(alternativas) < 5:
        alt = obter_entrada(f"Alternativa {len(alternativas) + 1}: ")
        if alt.upper() == 'FIM':
            if len(alternativas) < 3:
                print("Erro: Mínimo de 3 alternativas.")
                continue
            break
        alternativas.append(alt)
        
    print("\nÍndices das Alternativas:")
    for i, alt in enumerate(alternativas):
        print(f"[{i}] {alt}")
        
    validacao_indice = lambda i: 0 <= i < len(alternativas)
    indice_correto = obter_entrada("Índice da resposta correta: ", tipo=int, validacao=validacao_indice)
    
    try:
        pergunta = PerguntaMultiplaEscolha(enunciado, alternativas, indice_correto, dificuldade, tema)
        return pergunta
    except ValueError as e:
        print(f"Erro ao criar pergunta: {e}")
        return None

def criar_novo_quiz():
    global QUIZES
    
    print("\n--- Criar Novo Quiz ---")
    titulo = obter_entrada("Título do Novo Quiz: ")
    
    # Validação de unicidade do título
    if any(q.titulo == titulo for q in QUIZES):
        print(f"Erro: Já existe um quiz com o título '{titulo}'.")
        input("Pressione Enter para continuar.")
        return
        
    # Obter configurações
    max_tentativas_padrao = CONFIGURACOES.get("MAX_TENTATIVAS_PADRAO", 3)
    duracao_padrao_min = CONFIGURACOES.get("DURACAO_PADRAO_QUIZ_MIN", 10)
    
    max_tentativas = obter_entrada(f"Máximo de Tentativas (Padrão: {max_tentativas_padrao}): ", tipo=int, validacao=lambda x: x >= 1, default=max_tentativas_padrao)
    tempo_limite_min = obter_entrada(f"Tempo Limite em Minutos (0 para sem limite) (Padrão: {duracao_padrao_min}): ", tipo=int, validacao=lambda x: x >= 0, default=duracao_padrao_min)
    
    # Cria o novo quiz (sem perguntas inicialmente)
    novo_quiz = Quiz(titulo, perguntas=[], max_tentativas=max_tentativas, tempo_limite_min=tempo_limite_min)
    
    # Adiciona à lista global e salva
    QUIZES.append(novo_quiz)
    salvar_dados_atuais()
    
    print(f"\nQuiz '{titulo}' criado com sucesso! Adicione perguntas a ele.")
    input("Pressione Enter para continuar.")
    
    
def menu_gerenciar_quiz():
    global QUIZES
    
    while True:
        limpar_tela()
        print("--- Gerenciar Quizzes ---")
        print(f"Quizzes Carregados: {len(QUIZES)}")
        print("-" * 30)
        print("[1] Criar Novo Quiz")
        print("[2] Editar Quiz Existente")
        print("[3] Voltar ao Menu Principal")
        print("-" * 30)
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '1':
            criar_novo_quiz()
            
        elif escolha == '2':
            if not QUIZES:
                print("Nenhum quiz para editar. Crie um novo primeiro.")
                input("Pressione Enter para continuar.")
                continue
                
            quiz_selecionado = selecionar_quiz(QUIZES)
            if quiz_selecionado is not None:
                menu_editar_quiz(quiz_selecionado)
            else:
                print("Nenhum quiz foi selecionado.")
                input("Pressione Enter para continuar.")
            
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar.")

def menu_editar_quiz(quiz: Quiz):
    while True:
        limpar_tela()
        print(f"--- Editando Quiz: {quiz.titulo} ({len(quiz.perguntas)} perguntas) ---")
        print("-" * 30)
        print("[1] Adicionar Pergunta de Múltipla Escolha")
        print("[2] Adicionar Pergunta de Verdadeiro/Falso")
        print("[3] Visualizar Perguntas")
        print("[4] Voltar ao Menu de Gerenciamento")
        print("-" * 30)
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '1':
            pergunta = criar_pergunta_multipla_escolha(quiz)
            if pergunta:
                try:
                    quiz.adicionar_pergunta(pergunta)
                    salvar_quizes(QUIZES, QUIZ_PATH)
                    print("\nPergunta adicionada e quizzes salvos com sucesso!")
                except ValueError as e:
                    print(f"Erro: {e}")
            input("Pressione Enter para continuar.")
            
        elif escolha == '2':
            pergunta = criar_pergunta_verdadeiro_falso(quiz)
            if pergunta:
                try:
                    quiz.adicionar_pergunta(pergunta)
                    salvar_quizes(QUIZES, QUIZ_PATH)
                    print("\nPergunta adicionada e quizzes salvos com sucesso!")
                except ValueError as e:
                    print(f"Erro: {e}")
            input("Pressione Enter para continuar.")
            
        elif escolha == '3':
            limpar_tela()
            print(f"--- Perguntas do Quiz: {quiz.titulo} ---\n")
            if not quiz.perguntas:
                print("Este quiz ainda não tem perguntas.")
            else:
                for i, pergunta in enumerate(quiz.perguntas, 1):
                    print(f"{i}. {pergunta}\n")
            input("Pressione Enter para continuar.")
            
        elif escolha == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar.")


def selecionar_quiz(quizes: List[Quiz]) -> Optional[Quiz]:
    print("\n--- Seleção de Quiz ---")
    if not quizes:
        print("Nenhum quiz disponível.")
        return None
        
    for i, q in enumerate(quizes):
        print(f"[{i}] {q.titulo} ({len(q.perguntas)} perguntas)")
        
    print("[C] Cancelar")
        
    while True:
        escolha = input("Selecione o número do quiz ou 'C' para cancelar: ").strip()
        
        # Verifica se é cancelamento
        if escolha.upper() == 'C':
            return None
            
        # Tenta converter para inteiro
        try:
            indice = int(escolha)
            if 0 <= indice < len(quizes):
                return quizes[indice]
            else:
                print(f"Erro: Índice {indice} inválido. Escolha entre 0 e {len(quizes) - 1}.")
        except ValueError:
            print("Erro: Entrada inválida. Digite um número ou 'C' para cancelar.")

def menu_principal():
    carregar_dados_iniciais()
    
    if not QUIZES:
        print("Aviso: Nenhum quiz carregado. Crie um novo quiz no menu de gerenciamento.")

    while True:
        limpar_tela()
        print("--- Quizito: Sistema de Quiz Educacional ---")
        print(f"Quizzes Carregados: {len(QUIZES)}")
        print(f"Usuários Carregados: {len(USUARIOS)}")
        print("-" * 30)
        print("[1] Iniciar Quiz")
        print("[2] Selecionar/Cadastrar Usuário")
        print("[3] Gerenciar Quizzes")
        print("[4] Sair")
        print("-" * 30)
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '1':
            if not QUIZES:
                print("Erro: Nenhum quiz disponível para iniciar.")
                input("Pressione Enter para continuar.")
                continue
            
            quiz_selecionado = selecionar_quiz(QUIZES)
            if quiz_selecionado:
                usuario_selecionado = selecionar_usuario(USUARIOS)
                executar_quiz(quiz_selecionado, usuario_selecionado)
        elif escolha == '2':
            selecionar_usuario(USUARIOS)
        elif escolha == '3':
            menu_gerenciar_quiz()
        elif escolha == '4':
            print("Obrigado por usar o Quizito. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar.")

if __name__ == "__main__":
    menu_principal()