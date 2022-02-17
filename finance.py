from flask import Flask, request
from flask import jsonify
import sentry_sdk
from utils.finance_functions import *

sentry_sdk.init(
    "https://38ebd5aa73104a1d8b19b323c9fcdf67@sentry.daily-do.ir/4",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)

# get financial data(this month income and current credit)


@app.route('/financial-tab-basic-info', methods=['GET'])
def credit_and_income():
    current_user = "sp001"

    status = 1
    try:
        if status == 1:
            credit = user_credit(current_user)
            income = this_month_user_incom(current_user)
            return jsonify({'credit': credit, 'income': income, 'status': 1})
        else:
            return jsonify({{'status': 2}})
    except:
        return jsonify({'status': 0})

    # getting an array of {i}th 10 transaction


@app.route('/financial-tab-transactions-table', methods=['GET'])
def transactions():
    current_user = "sp001"
    i = int(request.args.get('id'))
    transactions = i_tenth_transaction(current_user, i)
    result = []
    for row in transactions:
        user_data = {}
        user_data['type'] = row[0]
        user_data['value'] = row[1]
        user_data['date'] = row[2]
        user_data['paycode'] = row[3]
        result.append(user_data)
    return jsonify(result)

    # getting an array of all the bank accounts information


@app.route('/financial-tab-bank-account-table', methods=['GET'])
def accounts():
    current_user = "sp001"
    user_acc, owner = user_accounts(current_user)
    result = []
    for row in user_acc:
        user_data = {}
        user_data['owner'] = owner[0][0]
        user_data['bank'] = row[0]
        user_data['accountNumber'] = row[1]
        user_data['shaba'] = row[2]
        result.append(user_data)
    return jsonify(result)

    # add a new bank account


@app.route('/addaccount', methods=['POST'])
def addaccount():
    current_user = "sp001"
    try:
        data = request.get_json()
        bank_name, account_number, shabaNumber = data['bank'], data['accountNumber'], data['shaba']
    except:
        status = 2
        return jsonify({'status': status})
    try:
        add_new_account(current_user, bank_name, account_number, shabaNumber)
        status = 1
        return jsonify({'status': status})
    except:
        status = 0
        return jsonify({'status': status})

#   withdraw cash from credit


@app.route("/withdrawal", methods=["POST"])
def withdrawal():
    current_user = "sp001"
    try:
        data = request.get_json()
        bank_name, account_number, cash = data['bank'], data['accountNumber'], data['cash']
    except:
        #   invalid data
        return jsonify({'status': 2})
    try:
        if check_valid_cash(cash, current_user):
            try:
                withdrawal_action(bank_name, account_number, cash)
            except:
                # gateway_error
                return jsonify({'status': 4})
            user_credit_update(cash, current_user)
            # Cash deposit to your account was successful
            return jsonify({'status': 1})
        else:
            # This amount cannot be paid
            return jsonify({'status': 3})
    except:
        # error
        return jsonify({'status': 0})

    # run app
if __name__ == "__main__":
    app.run()
