from __future__ import print_function
import logging
import grpc
import finance_pb2
import finance_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = finance_pb2_grpc.withdrawerStub(channel)
        cash = 500000000
        user_ID = "sp001"
        response = stub.withdrawal(finance_pb2.CashRequest(cash=cash, user_ID=user_ID,
                                                           bank_name='صادرات', account_number="100324200001"))
        print("withdrw client received: ", response.status)

        stub = finance_pb2_grpc.account_adderStub(channel)
        user_ID = "sp001"
        bank_name = "رسالت"
        account_number = "45682159900"
        shaba_number = "IR005421845682100"
        response = stub.add_account(finance_pb2.AccountInfoRequest(user_ID=user_ID, bank_name=bank_name,
                                                                   account_number=account_number, shaba_number=shaba_number))
        print("adding new account client status: ", response.status)

        stub = finance_pb2_grpc.update_credit_incomeStub(channel)
        response = stub.credit_and_income(finance_pb2.CreditAndIncomeRequest(user_ID=user_ID))
        income = response.income
        credit = response.credit
        print("income=", income, "credit=", credit)

        stub = finance_pb2_grpc.show_accountsStub(channel)
        response = stub.accounts(finance_pb2.accountsRequest(user_ID=user_ID))
        account = response.account
        print("account=", account)

        stub = finance_pb2_grpc.transactions_ten_iStub(channel)
        response = stub.transactions(finance_pb2.TenITransactionRequest(user_ID=user_ID, i=1))
        trasactionsi10 = response.tenthitransactions
        print("transactions=", trasactionsi10)

if __name__ == '__main__':
    logging.basicConfig()
    run()
