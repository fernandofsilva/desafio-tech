# Import flask
from flask import Flask, render_template, request

# Import Calculation custom class
from Calculation import *


# Initiate App
app = Flask(__name__, template_folder='templates')


@app.route('/')
def main():
    return render_template(
        'base.html',
        title='Desafio Tech'
    )


@app.route('/', methods=['POST'])
def process_calculation():

    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Call Calculation class
    calc = Calculation(
        fund_file='data/zarathustra.csv',
        cdi_file='data/cdi.csv',
        start_date=start_date,
        end_date=end_date
    )

    # Valid the start and end dates
    if calc.check_date():
        return render_template('error.html')

    # Cumulative return
    cum_ret_value = f'{calc.calculate_cumulative_returns_value():.4f}'

    # Calculate relative return
    rel_ret = f'{calc.calculate_relative_return():.4f}'

    # Calculate minimum and maximum returns
    min_value, min_date, max_value, max_date = calc.calculate_min_max_returns()

    minimum = {'value': f'{min_value:.4f}',
              'date': min_date}

    maximum = {'value': f'{max_value:.4f}',
               'date': max_date}

    # Calculate Net Equity
    net_equity = f'{calc.calculate_net_equity():.2f}'

    # # Cumulative return
    cum_ret_table = calc.calculate_cumulative_returns_table()

    return render_template(
        'output.html',
        title='Desafio Tech',
        start_date=start_date,
        end_date=end_date,
        cum_ret_value=cum_ret_value,
        rel_ret=rel_ret,
        minimum=minimum,
        maximum=maximum,
        net_equity=net_equity,
        cum_ret_table=cum_ret_table.to_html(
            index=False, classes="thead-dark", justify='center')
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
