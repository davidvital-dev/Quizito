from typing import List, Dict, Any
from quiz_app.modelos import Usuario


def gerar_relatorio_alunos_por_turma(usuarios: List[Usuario]) -> Dict[str, List[Dict[str, Any]]]:
	"""Agrupa usuários por turma e retorna um dicionário.

	Cada entrada tem a forma:
		turma -> [ { 'nome': ..., 'email': ..., 'matricula': ... }, ... ]
	Usuários sem turma são agrupados em 'Sem Turma'.
	"""
	relatorio: Dict[str, List[Dict[str, Any]]] = {}
	for u in usuarios:
		turma = u._turma if getattr(u, '_turma', None) else 'Sem Turma'
		relatorio.setdefault(turma, []).append({
			'nome': u.nome,
			'email': u.email,
			'matricula': getattr(u, '_matricula', None)
		})
	return relatorio


def imprimir_relatorio_alunos_por_turma(usuarios: List[Usuario]):
	rel = gerar_relatorio_alunos_por_turma(usuarios)
	print('--- Relatório: Alunos por Turma ---')
	for turma, lista in rel.items():
		print(f"\nTurma: {turma} | Total: {len(lista)}")
		for s in lista:
			print(f"  - {s['nome']} (Matrícula: {s['matricula']}) - {s['email']}")
	print('\n--- Fim do Relatório ---')


def export_relatorio_alunos_por_turma_json(usuarios: List[Usuario], caminho: str):
	"""Exporta o relatório 'alunos por turma' para um arquivo JSON no caminho informado."""
	import json
	rel = gerar_relatorio_alunos_por_turma(usuarios)
	with open(caminho, 'w', encoding='utf-8') as f:
		json.dump(rel, f, ensure_ascii=False, indent=2)


def gerar_relatorio_consolidado(usuarios: List[Usuario], pesos: Dict[str, int]) -> Dict[str, Any]:
	"""Gera um relatório consolidado com:
	- ranking (por percentual de acerto e pontuação)
	- desempenho por tema
	- taxa de acerto global

	Retorna um dicionário com os dados agregados.
	"""
	ranking = []
	desempenho_tema: Dict[str, Dict[str, int]] = {}
	global_acertos = 0
	global_total = 0

	for u in usuarios:
		total_pont = 0
		total_max = 0
		acertos = 0
		total_qs = 0

		for tentativa in u.tentativas:
			if not tentativa.concluida:
				continue
			total_pont += tentativa.pontuacao_obtida
			total_max += tentativa._quiz.calcular_pontuacao_maxima(pesos)

			for i, pergunta in enumerate(tentativa._quiz.perguntas):
				total_qs += 1
				resp = tentativa._respostas.get(i)
				acertou = (resp is not None and pergunta.verificar_resposta(resp))

				tema = pergunta.tema
				if tema not in desempenho_tema:
					desempenho_tema[tema] = {"acertos": 0, "erros": 0, "total": 0}

				if acertou:
					desempenho_tema[tema]["acertos"] += 1
					acertos += 1
					global_acertos += 1
				else:
					desempenho_tema[tema]["erros"] += 1

				desempenho_tema[tema]["total"] += 1
				global_total += 1

		percentual = (acertos / total_qs * 100) if total_qs > 0 else 0
		ranking.append({
			"nome": u.nome,
			"matricula": getattr(u, "_matricula", None),
			"email": u.email,
			"total_pontuacao": total_pont,
			"total_pontuacao_max": total_max,
			"percentual_acerto": percentual,
			"total_questoes": total_qs
		})

	# Ordena ranking por percentual de acerto (desc), depois por pontuação total
	ranking.sort(key=lambda x: (x["percentual_acerto"], x["total_pontuacao"]), reverse=True)

	# Enriquecer desempenho por tema com percentual
	desempenho_por_tema = {}
	for tema, stats in desempenho_tema.items():
		total = stats["total"]
		ac = stats["acertos"]
		desempenho_por_tema[tema] = {
			"acertos": ac,
			"erros": stats["erros"],
			"total": total,
			"percentual_acerto": (ac / total * 100) if total > 0 else 0
		}

	taxa_acerto_global = (global_acertos / global_total * 100) if global_total > 0 else 0

	return {
		"ranking": ranking,
		"desempenho_por_tema": desempenho_por_tema,
		"taxa_acerto_global": taxa_acerto_global,
	}


def imprimir_relatorio_consolidado(usuarios: List[Usuario], pesos: Dict[str, int]):
	rel = gerar_relatorio_consolidado(usuarios, pesos)
	print('--- Relatório ---')
	print(f"Taxa de Acerto Global: {rel['taxa_acerto_global']:.2f}%")

	print('\n** Ranking de Usuários **')
	for i, u in enumerate(rel['ranking'], 1):
		print(f"{i}. {u['nome']} (Matrícula: {u['matricula']}) — {u['percentual_acerto']:.2f}% ({u['total_pontuacao']}/{u['total_pontuacao_max']})")

	print('\n** Desempenho por Tema **')
	for tema, stats in rel['desempenho_por_tema'].items():
		print(f"- {tema}: {stats['acertos']} acertos, {stats['erros']} erros, {stats['percentual_acerto']:.2f}%")

	print('\n--- Fim do Relatório ---')






def export_relatorio_consolidado_json(usuarios: List[Usuario], pesos: Dict[str, int], caminho: str):
	"""Exporta o relatório consolidado para um arquivo JSON no caminho informado."""
	import json
	rel = gerar_relatorio_consolidado(usuarios, pesos)
	with open(caminho, 'w', encoding='utf-8') as f:
		json.dump(rel, f, ensure_ascii=False, indent=2)
