"""Gera relatorio/relatorio_big_data.pdf.

Cada print entra num "slot". Se o arquivo existir em relatorio/prints/, a imagem é inserida;
se não existir, sai um quadro tracejado com o nome do arquivo esperado.
Uso: python relatorio/gerar_pdf.py   (precisa de playwright + chromium)
"""
from __future__ import annotations

import base64
import html
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PRINTS = AQUI / "prints"
REPO = "https://github.com/GN0Ber/gs-citizentech-dados"

FALTANDO: list[str] = []


def slot(arquivo: str, legenda: str) -> str:
    p = PRINTS / arquivo
    if p.exists():
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        b64 = base64.b64encode(p.read_bytes()).decode()
        corpo = f'<img src="data:{mime};base64,{b64}">'
    else:
        FALTANDO.append(arquivo)
        corpo = f'<div class="vazio">PRINT<br><code>prints/{arquivo}</code></div>'
    return f'<figure>{corpo}<figcaption>{legenda}</figcaption></figure>'


def tabela(cab: list[str], linhas: list[list[str]], cls: str = "") -> str:
    th = "".join(f"<th>{c}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


DIAGRAMA = """
<svg viewBox="0 0 760 330" class="diag" xmlns="http://www.w3.org/2000/svg" font-family="Inter, Arial" font-size="11">
 <defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="#334"/></marker></defs>
 <g fill="#eef3fb" stroke="#4a6fa5">
  <rect x="10" y="10" width="190" height="34" rx="5"/><rect x="10" y="52" width="190" height="34" rx="5"/>
  <rect x="10" y="94" width="190" height="34" rx="5"/></g>
 <g fill="#fdf2e3" stroke="#c07a1a"><rect x="10" y="136" width="190" height="48" rx="5"/></g>
 <g fill="#1f2a44" font-weight="600">
  <text x="20" y="31">GeoSampa WFS · cadastro ILUME</text><text x="20" y="73">SP156 · CKAN (poste, fiação)</text>
  <text x="20" y="115">Open-Meteo · sol e chuva</text><text x="20" y="157">Robô LDR · app + visão · RPA</text>
  <text x="20" y="173" font-weight="400" fill="#7a4b0a">simulados até a integração</text></g>
 <rect x="250" y="40" width="160" height="110" rx="6" fill="#e8f5ec" stroke="#2e7d4f"/>
 <text x="262" y="62" font-weight="700" fill="#1d5135">Airflow 3</text>
 <text x="262" y="80">gs_coleta_iluminacao</text><text x="262" y="96">@daily · catchup</text>
 <text x="262" y="112">3 coletas em paralelo</text><text x="262" y="128">conferir_chegada + alerta</text>
 <rect x="460" y="70" width="140" height="50" rx="6" fill="#f4f4f6" stroke="#666"/>
 <text x="472" y="92" font-weight="700">chegada/&lt;fonte&gt;/</text><text x="472" y="108">1 arquivo por dia</text>
 <rect x="640" y="70" width="110" height="50" rx="6" fill="#f4f4f6" stroke="#666"/>
 <text x="650" y="92" font-weight="700">Volume</text><text x="650" y="108">upload em lotes</text>
 <g fill="#efe9fb" stroke="#6a4fb3">
  <rect x="40" y="230" width="150" height="70" rx="6"/><rect x="230" y="230" width="170" height="70" rx="6"/>
  <rect x="440" y="230" width="170" height="70" rx="6"/></g>
 <rect x="640" y="230" width="110" height="70" rx="6" fill="#e8f5ec" stroke="#2e7d4f"/>
 <g font-weight="700" fill="#3b2a73"><text x="52" y="252">Bronze</text><text x="242" y="252">Prata</text><text x="452" y="252">Ouro</text></g>
 <text x="652" y="252" font-weight="700" fill="#1d5135">MVP</text>
 <text x="52" y="270">Auto Loader</text><text x="52" y="286">checkpoint, só novo</text>
 <text x="242" y="270">tipos, 3+ regras, quarentena</text><text x="242" y="286">MERGE · hash LGPD</text>
 <text x="452" y="270">estrela: 3 fatos, 3 dims</text><text x="452" y="286">views vw_mvp_*</text>
 <text x="652" y="270">export JSON</text><text x="652" y="286">app, RPA, IA</text>
 <g stroke="#334" stroke-width="1.4" fill="none" marker-end="url(#s)">
  <path d="M200,27 L250,70"/><path d="M200,69 L250,85"/><path d="M200,111 L250,105"/><path d="M200,160 L250,130"/>
  <path d="M410,95 L460,95"/><path d="M600,95 L640,95"/><path d="M695,120 L695,180 L115,180 L115,230"/>
  <path d="M190,265 L230,265"/><path d="M400,265 L440,265"/><path d="M610,265 L640,265"/></g>
 <text x="300" y="196" fill="#555" font-style="italic">Databricks Free Edition · Unity Catalog workspace.gs</text>
</svg>"""


def montar() -> str:
    s = []
    s.append(f"""
<section class="capa">
 <p class="sup">FIAP · Engenharia de Software · Global Solution 2026.2 · CitizenTech</p>
 <h1>LuzViva</h1>
 <p class="sub">Big Data Architecture &amp; Data Integration<br>Pipeline de iluminação pública: Airflow 3 + Databricks (Bronze, Prata, Ouro)</p>
 <h2>01 · Integrantes</h2>
 {tabela(["Nome", "RM"], [["Caíque Walter Silva", "RM550693"], ["Guilherme Nobre Bernardo", "RM98604"],
    ["Guilherme Monteiro Espim", "RM99499"], ["João Paulo Fonseca Zamperlini", "RM99279"],
    ["Matheus José de Lima Costa", "RM551157"]], "estreita")}
 <p class="repo">Repositório público: <a href="{REPO}">{REPO}</a></p>
</section>""")

    s.append("""
<section><h2>02 · Produto e perguntas do MVP</h2>
<p class="destaque">Um robô mede a luz sob cada poste à noite, o cidadão manda foto pelo app e a visão
computacional classifica; o pipeline cruza tudo com o cadastro real da ILUME e entrega ao gestor quais
luminárias estão apagadas, onde e em que ordem atender, e ao RPA os chamados a abrir.</p>
<ol>
<li>Como está a iluminação de cada subprefeitura do piloto agora? <span class="q">(Q1)</span></li>
<li>Quais luminárias a equipe de campo deve atender primeiro? <span class="q">(Q2)</span></li>
<li>Quantas falhas o sistema achou antes de alguém reclamar? <span class="q">(Q3, impacto)</span></li>
<li>Quanto tempo a cidade leva hoje para resolver poste e fiação pelo SP156? <span class="q">(Q4, linha de base real)</span></li>
<li>Quando a visão diz "apagada", o robô confirma? <span class="q">(Q5, IA responsável)</span></li>
<li>Depois que o chamado é aberto, quanto tempo leva o reparo, e o robô confirma a luz de volta? <span class="q">(Q6, impacto)</span></li>
</ol>
<p>Piloto em três áreas: Sé, Pinheiros e Campo Limpo (47.736 pontos de iluminação do cadastro ILUME),
de 01 a 12/11/2026.</p>
<h2>03 · Diagrama do fluxo</h2>""" + DIAGRAMA + """
<p class="nota">O Databricks Free Edition não aceita conexão do Airflow; por isso a ponte é a pasta
<code>chegada/</code>, enviada ao Volume <code>workspace.gs.chegada</code> em lotes. Dependências do DAG:
<code>inicio &gt;&gt; [luminarias, sp156, clima]</code>; <code>luminarias &gt;&gt; [medicoes_robo, ocorrencias_app]</code>;
<code>medicoes_robo &gt;&gt; chamados_rpa</code>; todas <code>&gt;&gt; conferir_chegada</code>.</p>
</section>""")

    s.append("<section><h2>04 · Fontes de dados</h2>" + tabela(
        ["Fonte", "Origem", "Tipo", "Formato", "Frequência", "Volume no piloto"],
        [["luminarias", "GeoSampa WFS <code>geoportal:iluminacao_publica</code> (SMUL/ILUME)", "externa real", "GeoJSON paginado", "diária", "47.736 pontos"],
         ["sp156", "Portal de Dados Abertos SP, <code>dados-do-sp156</code> (CKAN)", "externa real", "CSV Latin-1 ;", "diária (arquivo trimestral, cache)", "1.113 pedidos de poste/fiação"],
         ["clima", "Open-Meteo <code>/v1/forecast</code>", "externa real", "JSON", "diária", "3 pontos"],
         ["medicoes_robo", "robô LDR (Maker Lab)", "própria, simulada", "JSON", "diária (rota noturna)", "150 a 260/noite"],
         ["ocorrencias_app", "app + visão computacional", "própria, simulada", "JSON", "diária", "8 a 18 fotos/dia"],
         ["chamados_rpa", "robô de RPA", "própria, simulada", "JSON", "diária", "322 chamados"]], "pequena") + """
<p><b>Por que simular.</b> Robô, visão e RPA ficam prontos na mesma janela de entrega. O simulador gera o
mesmo formato do contrato (<code>docs/contrato_mvp.md</code>), ancorado em postes reais do cadastro, com
~6% de sujeira proposital para as regras da Prata terem o que barrar. Quando o dado real chegar, ele cai na
mesma pasta e nada muda dali em diante.</p>
<p><b>Achados nas fontes reais.</b> (1) Lâmpada apagada quase não aparece no SP156 aberto: a cidade tem
663 mil pontos cadastrados e nenhum dado aberto de quais estão apagados, que é a lacuna do produto.
(2) O SP156 muda o formato da data entre arquivos (dd/MM no 2º trimestre, MM/dd no 3º); a Prata detecta
por arquivo. (3) O SP156 não tem protocolo: a chave é um hash dos campos estáveis. (4) Na zona do
piloto o poste vizinho fica a 12,7 m (mediana), menos que o erro do GPS de celular: o pipeline liga foto e
medição ao poste pela placa ILUME e usa o GPS só como reserva.</p>
</section>""")

    reqs = [
        ("01", "Fontes (≥ 2, ≥ 1 externa real)", "Três fontes externas reais (GeoSampa, SP156, Open-Meteo) e três próprias. Configuração em <code>dags/coletores/temas.py</code>; descrição em <code>docs/fontes.md</code>.",
         "r01_volume.png", "Volume <code>workspace.gs.chegada</code>: as 6 fontes, um arquivo por dia (lotes 1 e 2)."),
        ("02", "DAG agendado gravando em chegada/", "<code>gs_coleta_iluminacao</code>, <code>@daily</code>, <code>catchup=True</code> desde 01/11, grava <code>chegada/&lt;fonte&gt;/&lt;fonte&gt;_AAAA-MM-DD</code>, com 2 retries e alerta de falha.",
         None, "Prints na seção 06 (Grid com 12 execuções diárias, 0 falhas)."),
        ("03", "Paralelismo, verificação e Variables", "As três fontes externas rodam em paralelo; <code>conferir_chegada</code> valida que todo arquivo chegou; caminho e webhook ficam nas Variables <code>gs_chegada</code> e <code>gs_webhook_url</code>, fora do código.",
         None, "Print na seção 06 (visão Graph)."),
        ("04", "Dois ou mais lotes ao Volume", "Três lotes de dias diferentes: 01–03 e 04–05 (05/11) e 06–12 (12/11).",
         None, "Print na seção 07 (contagens por lote)."),
        ("05", "Bronze incremental sem duplicar", "Auto Loader com checkpoint por fonte: só arquivo novo entra; arquivo reenviado é ignorado. Contagens em <code>gs.controle_cargas</code>.",
         None, "Prints na seção 07."),
        ("06", "Prata: tipos, MERGE e regras com contagem", "JSON do envelope aberto com schema do contrato, tipos convertidos, regras de qualidade por tabela (21 no total) com linhas barradas indo para <code>prata_quarentena</code>, e MERGE pela chave de negócio.",
         "r06_prata_contagens.png", "Prata: antes, depois e novas por tabela após o MERGE."),
        ("06b", "", "", "r06_prata_qualidade.png", "<code>gs.controle_qualidade</code>: regras e linhas barradas (parte 1)."),
        ("06c", "", "", "r06_prata_qualidade2.png", "<code>gs.controle_qualidade</code>: regras e linhas barradas (parte 2)."),
        ("07", "Ouro (fato e dimensões) e 5 SQL", "Modelo estrela: <code>fato_inspecao</code>, <code>fato_ocorrencia</code>, <code>fato_chamado</code> com <code>dim_luminaria</code>, <code>dim_regiao</code>, <code>dim_tempo</code>. Seis consultas interpretadas na seção 08.",
         "r07_ouro_catalogo.png", "Catálogo <code>workspace.gs</code> com as tabelas Bronze, Prata e Ouro e as views do MVP."),
        ("08", "LGPD na Ouro e uso pelo MVP", "Nome, e-mail e telefone do cidadão viram <code>cidadao_hash</code> (SHA-256 com sal guardado fora do repositório); coordenada generalizada para ~110 m; as views <code>vw_mvp_*</code> não expõem nem o pseudônimo. O notebook 05 exporta as views em JSON para a API do app.",
         "r08_export_mvp.png", "Export das views do MVP: mapa (47.736), fila de manutenção (239) e painel (3)."),
        ("08b", "", "", "r08_app_mvp.png", "Tela do app LuzViva exibindo os dados exportados."),
        ("09", "README e organização", "README com integrantes, arquitetura, passo a passo e mapa dos requisitos; pastas <code>dags/</code>, <code>databricks/</code>, <code>docs/</code>, <code>amostras/</code>, <code>tests/</code> (28 testes automatizados).",
         "r09_github.png", "Repositório público no GitHub."),
    ]
    blocos = []
    for num, titulo, texto, arq, leg in reqs:
        cab = f'<h3>Requisito {num} · {titulo}</h3><p>{texto}</p>' if titulo else ""
        fig = slot(arq, leg) if arq else f'<p class="nota">{leg}</p>'
        blocos.append(f'<div class="req">{cab}{fig}</div>')
    s.append('<section><h2>05 · Requisitos 01 a 09</h2>' + "".join(blocos) + "</section>")

    s.append("<section><h2>06 · Airflow</h2>" +
             slot("s06_grid.png", "Visão Grid: execuções diárias de 01 a 12/11/2026, todas concluídas.") +
             slot("s06_graph.png", "Visão Graph: <code>inicio</code> dispara as três fontes externas em paralelo; as simuladas esperam o cadastro de luminárias; <code>conferir_chegada</code> fecha o dia.") +
             "</section>")

    s.append("<section><h2>07 · Contagens da Bronze</h2>" + tabela(
        ["Rodada", "Arquivos por fonte", "JSON (cada fonte)", "sp156 (linhas)", "Leitura"],
        [["1º lote (01–03)", "3", "0 → 3", "0 → 3.339", "carga inicial"],
         ["2º lote (04–05)", "5", "3 → 5 (+2)", "3.339 → 5.565 (+2.226)", "só os arquivos novos entram"],
         ["reexecução sem lote novo", "5", "5 → 5 (0)", "5.565 → 5.565 (0)", "não duplica"]], "pequena") +
        slot("s07_volume_lote2.png", "Volume com o 2º lote: 5 arquivos por pasta.") +
        slot("s07_bronze_lote2.png", "Bronze após o 2º lote: só as linhas novas entraram.") +
        slot("s07_bronze_reexecucao.png", "Bronze executada de novo sem arquivo novo: <code>novas = 0</code> em todas as fontes; histórico em <code>gs.controle_cargas</code>.") +
        """<p><b>Bronze × Prata.</b> A Bronze do SP156 guarda o recorte trimestral uma vez por dia de coleta, como
chegou; a Prata fica com 1.113 pedidos únicos, porque o MERGE pela chave hash descarta a repetição. Os arquivos
de luminárias 01 a 03 foram reenviados por engano e não entraram de novo: o checkpoint do Auto Loader reconhece
arquivo já lido.</p></section>""")

    q = [
        ("Q1 · Situação por subprefeitura", "q1.png",
         "13,9% a 14,1% das luminárias inspecionadas estão com falha nas três áreas (1.485 inspecionadas: 78 apagadas e 131 insuficientes). Uma em cada sete luminárias inspecionadas não ilumina o mínimo, e a proporção é parecida no centro (Sé) e na periferia (Campo Limpo)."),
        ("Q2 · Fila de manutenção", "q2.png",
         "A prioridade soma evidências: apagada vale 60, cada relato de cidadão +10 (máx. 30) e a visão com confiança ≥ 0,8 +10. O topo (100, Praça Doutor João Mendes, placa IP0195078) tem robô, três relatos e visão concordando. A placa vai pronta para a equipe da ILUME."),
        ("Q3 · Falhas achadas antes da reclamação (impacto)", "q3.png",
         "73,7% a 83,3% das falhas encontradas pelo robô não tinham nenhum relato de cidadão. Somadas, as luminárias apagadas representam 850 horas de rua no escuro por noite. Ressalva: o volume de fotos é simulado; o número real depende da adesão ao app."),
        ("Q4 · Linha de base real no SP156", "q4.png",
         "Dado real: pedidos de poste em mau estado e fiação solta levam de 8 a 45 dias (mediana) conforme a subprefeitura, e em várias mais de 80% seguem em aberto (Penha 98,4%, Santo Amaro 96,7%). Hoje a cidade leva semanas; o robô detecta em até três noites. Atenção: \"finalizada\" no SP156 pode significar encaminhada à concessionária."),
        ("Q5 · A visão confirma? (IA responsável)", "q5.png",
         "A precisão da visão sobe com a confiança: 0% abaixo de 0,60 (1 caso), 70,4% entre 0,60 e 0,79 (27), 85,7% entre 0,80 e 0,89 (14) e 90,9% acima de 0,90 (11). Por isso a prioridade só soma pontos com confiança ≥ 0,8, e abaixo disso a foto não abre chamado sozinha: o robô confirma antes."),
        ("Q6 · Tempo até o reparo (impacto)", "q6.png",
         "322 chamados abertos pelo RPA; mediana de 3,4 a 4,4 dias até o reparo (p90 de 7,4 a 9,4) e 27% a 32% dos reparos já confirmados em campo pelo robô. Os chamados abertos esperam há 3,4 a 5,4 dias (mediana), então a mediana dos concluídos não esconde uma fila parada. Comparado com a Q4: semanas no canal atual contra dias com o ciclo robô → RPA → equipe."),
    ]
    s.append("<section><h2>08 · Consultas SQL e interpretação</h2><p>Seis consultas em <code>databricks/04_consultas.sql</code> sobre a Ouro, 12 dias de dado (01 a 12/11/2026).</p>" +
             "".join(f'<div class="req"><h3>{t}</h3>{slot(a, t)}<p class="interp">{i}</p></div>' for t, a, i in q) + "</section>")

    s.append(f"""<section><h2>09 · Conclusão</h2>
<p><b>O que funcionou.</b> Coleta diária automática de três fontes públicas reais e três próprias, com
reprocessamento seguro (Bronze não duplica, Prata faz MERGE), 21 regras de qualidade com quarentena, modelo
estrela na Ouro e entrega ao app por views sem dado pessoal. As consultas sustentam o argumento do produto:
a maior parte das falhas não é reclamada (Q3) e o canal atual leva semanas (Q4), enquanto o ciclo do LuzViva
fecha em dias e é conferido em campo (Q6), com a IA usada só onde é confiável (Q5).</p>
<p><b>Limites.</b> Robô, fotos e chamados são simulados até a integração com os componentes do grupo; o
SP156 aberto quase não registra lâmpada apagada, então a linha de base usa poste e fiação; o Free Edition
exige upload manual dos lotes.</p>
<p><b>Próximo passo.</b> Trocar as fontes simuladas pelos dados reais do robô, do app e do RPA (mesmo
contrato), pedir à ILUME o histórico de chamados de lâmpada apagada e agendar os notebooks num Job.</p>
<p class="repo">Repositório: <a href="{REPO}">{REPO}</a></p></section>""")
    return "\n".join(s)


CSS = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm;}
body { font-family: Inter, 'Segoe UI', Arial, sans-serif; color: #1f2430; font-size: 10.5pt; line-height: 1.45; }
h1 { font-size: 40pt; margin: 6mm 0 2mm; color: #1f2a44; letter-spacing: -1px; }
h2 { font-size: 15pt; color: #1f2a44; border-bottom: 2px solid #f0b429; padding-bottom: 2px; margin: 8mm 0 3mm; }
h3 { font-size: 11pt; margin: 4mm 0 1mm; color: #2c3a5c; }
section { page-break-before: always; } section.capa { page-break-before: auto; }
.sup { color: #666; font-size: 9.5pt; margin-top: 20mm; } .sub { font-size: 12pt; color: #444; }
.repo { margin-top: 5mm; } a { color: #1f5fbf; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 9.5pt; }
table.estreita { width: 70%; } table.pequena { font-size: 8.5pt; }
th { background: #1f2a44; color: #fff; text-align: left; padding: 4px 6px; }
td { border-bottom: 1px solid #dde; padding: 4px 6px; vertical-align: top; }
code { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 8.8pt; background: #f1f2f6; padding: 0 3px; border-radius: 3px; }
.destaque { background: #fff8e6; border-left: 4px solid #f0b429; padding: 3mm 4mm; }
.q { color: #6a7287; font-size: 9pt; } .nota { color: #555; font-size: 9.5pt; }
.req { page-break-inside: avoid; margin-bottom: 4mm; }
figure { margin: 2mm 0 3mm; page-break-inside: avoid; }
figure img { width: 100%; border: 1px solid #ccd; }
figcaption { font-size: 9pt; color: #555; margin-top: 1mm; font-style: italic; }
.vazio { border: 2px dashed #b9bfcf; height: 55mm; display: flex; flex-direction: column; align-items: center;
  justify-content: center; color: #8a90a3; font-weight: 700; background: #fafbfd; text-align: center; }
.interp { background: #f4f7fc; border-left: 4px solid #4a6fa5; padding: 2mm 4mm; }
.diag { width: 100%; margin: 2mm 0; }
"""


def main() -> None:
    corpo = montar()
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{corpo}</body></html>'
    (AQUI / "relatorio.html").write_text(doc, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content(doc, wait_until="load")
        pg.pdf(path=str(AQUI / "relatorio_big_data.pdf"), format="A4", print_background=True,
               display_header_footer=True, header_template="<span></span>",
               footer_template='<div style="font-size:8px;width:100%;text-align:right;padding-right:15mm;color:#888">LuzViva · Big Data · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
               margin={"top": "16mm", "bottom": "16mm", "left": "15mm", "right": "15mm"})
        b.close()
    print("prints faltando:", len(FALTANDO))
    for f in FALTANDO:
        print("  ", f)


if __name__ == "__main__":
    main()
