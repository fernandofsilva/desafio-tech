# Import flask
from flask import Flask, render_template

# Import Calculation custom class
from Calculation import *


# Initiate App
app = Flask(__name__, template_folder='templates')

# Class
class Data:
    def __init__(self, descricao, ean, sku, url, image):
        self.descricao = descricao
        self.ean = ean
        self.sku = sku
        self.url = url
        self.image = image

calc = Calculation(
    fund_file='data/zarathustra.csv',
    cdi_file='data/cdi.csv',
    start_date = '2019-01-02',
    end_date = '2019-01-31'
)

prod = Data('ADORNO LHAMA BR FULLFIT',
            '7893220244896',
            '14998079',
            'https://www.pontofrio.com.br/decoracao/objetosdecorativos/adorno-vela-llama-em-porcelana-l15xp135cm-24745-14998079.html',
            'https://www.pontofrio-imagens.com.br/decoracao/ObjetosDecorativos/14998079/1097088051/adorno-vela-llama-em-porcelana-l15xp135cm-24745-14998079.jpg')




@app.route("/")
def main():
    return render_template(
        "input.html",
        title='Desafio Tech'
    )


# @app.route('/calculation_table', methods=['POST'])
# def calculation_table():
#
#     POST = request.json
#
#     return render_template(
#         "input.html",
#         title='Desafio Tech',
#         produtos=prod,
#         calculation=calc
#     )
#
# @app.route('/generate_chart', methods=['POST'])
# def generate_chart():
#
#     POST = request.json
#
#     return render_template(
#         "dados.html",
#         title='Desafio Tech',
#         produtos=prod,
#         calculation=calc
#     )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
