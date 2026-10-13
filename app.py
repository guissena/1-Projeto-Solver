from flask import Flask, request, render_template_string
from graphviz import Digraph
from datetime import datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simulador de Cartão de Crédito</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; color: #333; padding: 20px; }
  .container { max-width: 900px; margin: 0 auto; }
  h1 { text-align: center; margin-bottom: 24px; color: #1a1a2e; }
  .card { background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 24px; }
  label { display: block; font-weight: 600; margin-bottom: 6px; color: #444; }
  input, button { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; margin-bottom: 16px; }
  input:focus { outline: none; border-color: #4a6cf7; box-shadow: 0 0 0 3px rgba(74,108,247,0.15); }
  button { background: #4a6cf7; color: #fff; border: none; cursor: pointer; font-weight: 600; font-size: 16px; padding: 12px; transition: background .2s; }
  button:hover { background: #3a5ce5; }
  .hint { font-size: 13px; color: #888; margin-top: -10px; margin-bottom: 16px; }
  .results { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
  .result-box { background: #f8f9ff; border-radius: 8px; padding: 16px; text-align: center; }
  .result-box .label { font-size: 13px; color: #888; margin-bottom: 4px; }
  .result-box .value { font-size: 22px; font-weight: 700; color: #1a1a2e; }
  .result-box.highlight .value { color: #e74c3c; }
  .result-box.ok .value { color: #27ae60; }
  .flowchart { text-align: center; margin-top: 20px; }
  .flowchart svg { max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 8px; }
  .status-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: 600; margin-bottom: 16px; }
  .status-badge.ok { background: #e8f8ee; color: #27ae60; }
  .status-badge.late { background: #fdeaea; color: #e74c3c; }
  .error { color: #e74c3c; background: #fdeaea; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; }
</style>
</head>
<body>
<div class="container">
  <h1>💳 Simulador de Cartão de Crédito</h1>

  <div class="card">
    <h2 style="margin-bottom:16px;">Dados da Fatura</h2>
    <form method="POST" action="/">
      <label for="compras">Compras (valores separados por vírgula)</label>
      <input type="text" id="compras" name="compras" placeholder="Ex: 150.00, 89.90, 250.00" required>
      <div class="hint">Digite os valores das compras separados por vírgula</div>

      <label for="fechamento">Data de Fechamento da Fatura</label>
      <input type="date" id="fechamento" name="fechamento" required>

      <label for="pagamento">Data de Pagamento</label>
      <input type="date" id="pagamento" name="pagamento" required>

      <button type="submit">Calcular e Gerar Fluxograma</button>
    </form>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
  </div>

  {% if resultado %}
  <div class="card">
    <span class="status-badge {{ 'ok' if not resultado.tem_juros else 'late' }}">
      {{ 'Pagamento sem juros' if not resultado.tem_juros else 'Cálculo de juros aplicado' }}
    </span>
    <div class="results">
      <div class="result-box">
        <div class="label">Total de Compras</div>
        <div class="value">R$ {{ resultado.total_compras }}</div>
      </div>
      <div class="result-box {{ 'highlight' if resultado.tem_juros else 'ok' }}">
        <div class="label">Juros</div>
        <div class="value">R$ {{ resultado.juros }}</div>
      </div>
      <div class="result-box">
        <div class="label">Fechamento</div>
        <div class="value">{{ resultado.fechamento }}</div>
      </div>
      <div class="result-box highlight">
        <div class="label">Total a Pagar</div>
        <div class="value">R$ {{ resultado.total_pagar }}</div>
      </div>
    </div>
    <div class="flowchart">
      {{ resultado.svg | safe }}
    </div>
  </div>
  {% endif %}
</div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    error = None

    if request.method == 'POST':
        try:
            compras_raw = request.form['compras']
            compras = [float(v.strip()) for v in compras_raw.split(',') if v.strip()]
            if not compras:
                error = "Digite pelo menos um valor de compra."
            else:
                data_fechamento = datetime.strptime(request.form['fechamento'], '%Y-%m-%d')
                data_pagamento = datetime.strptime(request.form['pagamento'], '%Y-%m-%d')

                total_compras = sum(compras)

                if data_pagamento.day <= 25:
                    juros = 0.0
                else:
                    dias_atraso = data_pagamento.day - 25
                    juros = total_compras * (0.03 + dias_atraso * 0.01)

                total_pagar = total_compras + juros

                dot = Digraph()
                dot.attr(rankdir='TB')
                dot.node('A', f'Registro das compras\\nTotal: R$ {total_compras:.2f}')
                dot.node('B', f'Fechamento da fatura\\n{data_fechamento.strftime("%d/%m/%Y")}')
                dot.node('C', 'Emissão da fatura')
                dot.node('D', f'Data de pagamento\\n{data_pagamento.strftime("%d/%m/%Y")}')
                dot.node('E', f'Pagamento sem juros\\nTotal: R$ {total_compras:.2f}')
                dot.node('F', f'Cálculo de juros\\nJuros: R$ {juros:.2f}\\nTotal: R$ {total_pagar:.2f}')
                dot.edges(['AB', 'BC', 'CD'])
                dot.edge('D', 'E', label='Até dia 25')
                dot.edge('D', 'F', label='Após dia 25')

                svg = dot.pipe(format='svg').decode('utf-8')

                resultado = {
                    'total_compras': f'{total_compras:.2f}',
                    'juros': f'{juros:.2f}',
                    'total_pagar': f'{total_pagar:.2f}',
                    'fechamento': data_fechamento.strftime('%d/%m/%Y'),
                    'svg': svg,
                    'tem_juros': juros > 0,
                }
        except ValueError as e:
            error = f"Erro nos dados informados: {e}"

    return render_template_string(HTML, resultado=resultado, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
