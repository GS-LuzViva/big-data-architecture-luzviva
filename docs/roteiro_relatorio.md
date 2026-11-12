# Roteiro do relatório em PDF (na ordem exigida pelo professor)

Fora da ordem tira até 1 ponto; print sem legenda também. Todo print com legenda curta.

| # | Seção | O que colocar | De onde tirar |
|---|---|---|---|
| 01 | Integrantes | Caíque Walter Silva (RM550693), Guilherme Nobre Bernardo (RM98604), Guilherme Monteiro Espim (RM99499), João Paulo Fonseca Zamperlini (RM99279), Matheus José de Lima Costa (RM551157) | README |
| 02 | Produto e perguntas | 1 frase do produto + as 5 perguntas do README | README |
| 03 | Diagrama do fluxo | fonte → Airflow → chegada → Volume → Bronze → Prata → Ouro → MVP | diagrama do README redesenhado |
| 04 | Tabela de fontes | origem, formato, frequência | `docs/fontes.md` |
| 05 | Requisitos 01 a 09 | um print + 2 linhas por requisito | mapa no README |
| 06 | Airflow | prints das visões **Graph** e **Grid** com execuções concluídas (e uma falha com retry, se tiver) | UI do Airflow |
| 07 | Contagens da Bronze | antes/depois do 2º lote e da 2ª execução sem lote novo (`linhas_novas = 0`) | `SELECT * FROM gs.controle_cargas` |
| 08 | 5 consultas SQL | resultado + interpretação de 2 a 3 linhas cada | `04_consultas.sql` |
| 09 | Conclusão e link | o que funcionou, limites (dados próprios simulados até a integração), próximo passo | |

## Rodadas executadas

| Data | O quê |
|---|---|
| 05/11 | Lote 1 (01–03) e lote 2 (04–05); prints de Volume, Bronze (incremental e `novas = 0`) e Prata |
| 10/11 | Airflow recuperou 06–10 pelo catchup; prints do Grid e do Graph |
| 12/11 | Lote 3 (06–12), rodada final 01 → 05; prints das 6 consultas e do export do MVP |

## Interpretação das consultas (resultado final, 12 dias: 01 a 12/11/2026)

* **Q1**: 13,9% a 14,1% das luminárias inspecionadas estão com falha nas três áreas
  (1.485 inspecionadas; 78 apagadas e 131 insuficientes). "Uma em cada sete luminárias
  inspecionadas não ilumina o mínimo."
* **Q2**: a fila soma evidências: apagada vale 60, cada relato de cidadão +10 (máx. 30) e a visão
  com confiança ≥ 0,8 +10. O topo (prioridade 100, Praça Doutor João Mendes, IP0195078) tem as três
  evidências; a placa vai pronta para a equipe da ILUME.
* **Q3 (impacto)**: 73,7% a 83,3% das falhas achadas pelo robô não tinham nenhum relato de
  cidadão (Pinheiros 83,3%). Juntas, as luminárias apagadas somam 850 horas de rua no escuro por
  noite. Ressalva: o volume de fotos é simulado; o número real depende da adesão ao app.
* **Q4 (dado real, o mais forte do trabalho)**: no SP156, pedidos de poste em mau estado e fiação
  solta levam de 8 a 45 dias (mediana) conforme a subprefeitura, e em várias mais de 80% seguem em
  aberto (Penha 98,4%, Santo Amaro 96,7%). "Hoje a cidade leva semanas; o robô detecta em até 3
  noites." Atenção: "finalizada" no SP156 pode significar encaminhada à concessionária.
* **Q5 (IA responsável)**: a precisão da visão sobe com a confiança: 0% abaixo de 0,60 (1 caso),
  70,4% em 0,60–0,79 (27), 85,7% em 0,80–0,89 (14) e 90,9% acima de 0,90 (11). Por isso a
  prioridade só soma pontos com confiança ≥ 0,8, e abaixo disso a foto não abre chamado sozinha:
  o robô confirma antes.
* **Q6**: 322 chamados; mediana de 3,4 a 4,4 dias até o reparo (p90 de 7,4 a 9,4) e 27% a 32% dos
  reparos já confirmados em campo pelo robô na ronda seguinte. Os abertos esperam há 3,4 a 5,4 dias
  (mediana), então a mediana dos concluídos não está escondendo uma fila parada. Comparar com a
  Q4: semanas no canal atual contra dias com o ciclo robô → RPA → equipe.
* **Bronze × Prata (item 07)**: a Bronze do SP156 guarda uma cópia do recorte trimestral por dia
  de coleta; a Prata tem 1.113 pedidos únicos. O MERGE pela chave hash garante que reprocessar não
  duplica. Arquivos reenviados (luminárias 01–03) não entraram de novo: o checkpoint do Auto Loader
  reconhece arquivo já lido.
* **Qualidade (Prata, rodada de 05/11)**: das 1.077 medições, as regras barraram 28 fora do horário
  noturno, 26 com lux negativo, 14 sem GPS e 14 longe de luminária; ocorrências: 3 sem categoria,
  3 com confiança fora de 0..1, 2 fora do município. Vão para a quarentena, não somem.
* **Entrega ao MVP (item 08)**: o export gerou `vw_mvp_mapa_luminarias` (47.736 pontos),
  `vw_mvp_fila_manutencao` (239) e `vw_mvp_painel_subprefeitura` (3). Cópia em `amostras/mvp/`.
