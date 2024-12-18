from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/processar', methods=['POST'])
def processar_dados():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        # Tenta obter o JSON do corpo da requisição
        dados = request.get_json()

        if not dados:
            return jsonify({"error": "Nenhum dado foi enviado ou o corpo está vazio."}), 400

        # Lê os campos do JSON
        codigo_de_barras = dados.get('codigo_de_barras')
        categoria = dados.get('categoria')
        qtd_estoque = int(dados.get('qtd_estoque'))
        data_validade = dados.get('data_validade')
        preco_original = float(dados.get('preco_original'))

        # Calcula os dias para vencer e define o preço promocional
        hoje = datetime.now()
        validade = datetime.strptime(data_validade, '%Y-%m-%d')
        dias_para_vencer = (validade - hoje).days
        preco_promocional = round(preco_original * 0.8, 2) if dias_para_vencer < 7 else preco_original

        # Retorna os resultados
        return jsonify({
            'nome': f"Produto {codigo_de_barras[-4:]}",
            'descricao': f"Categoria: {categoria}, Estoque: {qtd_estoque}",
            'preco_promocional': preco_promocional,
            'dias_para_vencer': dias_para_vencer
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Erro de valor: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
