import streamlit as st
import json
from datetime import datetime

class ContaAPagar:
    def __init__(self, identificacao, descricao, codigo_fornecedor, descricao_fornecedor, valor_pago, data_pagamento):
        self.identificacao = identificacao
        self.descricao = descricao
        self.codigo_fornecedor = codigo_fornecedor
        self.descricao_fornecedor = descricao_fornecedor
        self.valor_pago = valor_pago
        self.data_pagamento = data_pagamento

class CafeteriaContas:
    def __init__(self):
        self.contas_a_pagar = []

    def adicionar_conta_a_pagar(self, conta):
        self.contas_a_pagar.append(conta)
        self.gerar_json('contas.json')  # Salvar todas as contas no arquivo JSON após adição

    def listar_contas_a_pagar(self):
        return self.contas_a_pagar

    def gerar_json(self, nome_arquivo):
        # Ler contas existentes no arquivo (se existirem)
        try:
            with open(nome_arquivo, 'r') as arquivo_leitura:
                contas_json = json.load(arquivo_leitura)
        except FileNotFoundError:
            contas_json = []

        # Adicionar novas contas
        for conta in self.contas_a_pagar:
            contas_json.append({
                "identificacao": conta.identificacao,
                "descricao": conta.descricao,
                "codigo_fornecedor": conta.codigo_fornecedor,
                "descricao_fornecedor": conta.descricao_fornecedor,
                "valor_pago": conta.valor_pago,
                "data_pagamento": conta.data_pagamento.isoformat() if isinstance(conta.data_pagamento, datetime) else None
            })

        # Gravar todas as contas no arquivo JSON
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(contas_json, arquivo, indent=2, default=str)

    def ler_json(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as arquivo:
                contas_json = json.load(arquivo)

            self.contas_a_pagar = []
            for conta_json in contas_json:
                data_pagamento = datetime.fromisoformat(conta_json["data_pagamento"]) if conta_json["data_pagamento"] else None
                conta = ContaAPagar(
                    conta_json["identificacao"],
                    conta_json["descricao"],
                    conta_json["codigo_fornecedor"],
                    conta_json["descricao_fornecedor"],
                    conta_json["valor_pago"],
                    data_pagamento
                )
                self.contas_a_pagar.append(conta)
        except FileNotFoundError:
            # Se o arquivo não existir, não há contas a serem lidas
            pass

# Criar instância da classe CafeteriaContas
cafeteria_contas = CafeteriaContas()

# Interface Streamlit
st.title('Gestão de Contas a Pagar - Cafeteria')

# Restante do código permanece inalterado
# ...



# Botões para ler e gerar JSON
if st.button('Ler Dados de JSON'):
    st.write(cafeteria_contas.ler_json('contas.json'))
    st.success('Dados lidos com sucesso!')

if st.button('Gerar JSON'):
    cafeteria_contas.gerar_json('contas.json')
    st.success('JSON gerado com sucesso!')

# Formulário para adicionar nova conta
st.header('Adicionar Nova Conta a Pagar')
identificacao = st.number_input('Identificação', min_value=1, value=1, step=1)
descricao = st.text_input('Descrição')
codigo_fornecedor = st.text_input('Código do Fornecedor')
descricao_fornecedor = st.text_input('Descrição do Fornecedor')
valor_pago = st.number_input('Valor Pago', min_value=0.0, value=0.0, step=1.0)
data_pagamento = st.date_input('Data de Pagamento', value="today", format="DD/MM/YYYY", disabled=False, label_visibility="visible")

if st.button('Adicionar Conta'):
    nova_conta = ContaAPagar(identificacao, descricao, codigo_fornecedor, descricao_fornecedor, valor_pago, data_pagamento)
    cafeteria_contas.adicionar_conta_a_pagar(nova_conta)
    st.success('Conta adicionada com sucesso!')

# Listar contas existentes
st.header('Contas a Pagar Atuais')
contas_atuais = cafeteria_contas.listar_contas_a_pagar()
for conta in contas_atuais:
    st.write(f'**Identificação:** {conta.identificacao}')
    st.write(f'**Descrição:** {conta.descricao}')
    st.write(f'**Código do Fornecedor:** {conta.codigo_fornecedor}')
    st.write(f'**Descrição do Fornecedor:** {conta.descricao_fornecedor}')
    st.write(f'**Valor Pago:** {conta.valor_pago}')
    st.write(f'**Data de Pagamento:** {conta.data_pagamento}')
    st.write('---')
