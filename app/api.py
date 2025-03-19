from flask import Flask, request, jsonify
from app.AccountsRegistry import AccountsRegistry
from app.Account import Account

app = Flask(__name__)

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()

    if (AccountsRegistry.find_account_by_pesel(data["pesel"])):
        return jsonify({"message": "Account on that pesel has already been created"}), 409

    print(f"Create account request: {data}")
    konto = Account(data["name"], data["surname"], data["pesel"])
    AccountsRegistry.add_account(konto)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts/count", methods=['GET'])
def get_accounts_ammount():
    ammount = AccountsRegistry.get_account_ammount()
    return jsonify({"count": ammount}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = AccountsRegistry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"name": account.name, "surname": account.surname, "pesel": account.pesel}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = AccountsRegistry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    if "name" in data:
        account.name = data["name"]
    if "surname" in data:
        account.surname = data["surname"]
    if "pesel" in data:
        account.pesel = data["pesel"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = AccountsRegistry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    AccountsRegistry._accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_money(pesel):
    account = AccountsRegistry.find_account_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    if "amount" not in data or "type" not in data:
        return jsonify({"error": "Bad request, missing fields."}), 400

    amount = data["amount"]
    transfer_type = data["type"]

    if transfer_type == "incoming":
        account.incomingTransfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    elif transfer_type == "outgoing":
        previous_saldo = account.saldo
        account.outgoingTransfer(amount)
        if account.saldo == previous_saldo:
            return jsonify({"error": "Insufficient funds for outgoing transfer"}), 422
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    elif transfer_type == "express":
        previous_saldo = account.saldo
        if account.saldo < (amount + account.fee):
            return jsonify({"error": "Express transfer failed due to insufficient funds"}), 422
        account.expressTransfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    else:
        return jsonify({"error": "Unsupported transfer type"}), 400

@app.route("/api/test/reset", methods=['POST'])
def reset_accounts():
    from app.AccountsRegistry import AccountsRegistry
    AccountsRegistry._accounts = []
    return jsonify({"message": "Registry reset"}), 200
