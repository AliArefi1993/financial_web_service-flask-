# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
from finance_functions import *
import grpc

import finance_pb2
import finance_pb2_grpc

class account_adder(finance_pb2_grpc.account_adderServicer):

    def add_account(self, request, context):
        try:
            current_user = request.user_ID
            bank_name = request.bank_name
            account_number = request.account_number
            shaba_number = request.shaba_number
        except:
            status = 2
            return finance_pb2.AddingAccountActionReply(status=status)
        try:
            add_new_account(current_user, bank_name, account_number, shaba_number)
            status = 1
            return finance_pb2.AddingAccountActionReply(status=status)
        except:
            status = 0
            return finance_pb2.AddingAccountActionReply(status=status)



class withdrawer(finance_pb2_grpc.withdrawerServicer):
    def withdrawal(self, request, context):
        try:
            user_ID = request.user_ID
            bank_name, account_number, cash = request.bank_name, request.account_number, request.cash
        except:
            #   invalid data
            status = 2
            return finance_pb2.WithdrawActionReply(status=status)
        try:
            if check_valid_cash(cash, user_ID):
                try:
                    withdrawal_action(bank_name, account_number, cash)
                except:
                    # gateway_error
                    status = 4
                    return finance_pb2.WithdrawActionReply(status=status)
                user_credit_update(cash, user_ID)
                # Cash deposit to your account was successful
                status = 1
                return finance_pb2.WithdrawActionReply(status=status)
            else:
                #This amount cannot be paid
                status = 3
                return finance_pb2.WithdrawActionReply(status=status)
        except:
            # error
            status = 0
        return finance_pb2.WithdrawActionReply(status=status)


class update_credit_income(finance_pb2_grpc.update_credit_incomeServicer):

    def credit_and_income(self, request, context):
        user_ID = request.user_ID
        income = this_month_user_incom(user_ID)
        credit = user_credit(user_ID)
        return finance_pb2.CreditAndIncomeResponse(income=income, credit=credit)

class show_accounts(finance_pb2_grpc.show_accountsServicer):

    def accounts(self, request, context):
        current_user = request.user_ID
        user_acc, owner = user_accounts(current_user)
        all_accounts = []
        for row in user_acc:
            user_data = finance_pb2.AccountMsg(owner=owner[0][0], bank=row[0], accountNumber=row[1], shaba=row[2])
            all_accounts.append(user_data)
        return finance_pb2.accountsResponse(account=all_accounts)

class transactions_ten_i(finance_pb2_grpc.transactions_ten_iServicer):

    def transactions(self, request, context):
        current_user = request.user_ID
        i = int(request.i)
        transactions = i_tenth_transaction(current_user, i)
        all_transactions = []
        for row in transactions:
            user_data = finance_pb2.Tenthitransactions(type=row[0], value=row[1], date=row[2], paycode=row[3])
            all_transactions.append(user_data)
        return finance_pb2.TenITransactionResponse(tenthitransactions=all_transactions)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    finance_pb2_grpc.add_withdrawerServicer_to_server(withdrawer(), server)
    finance_pb2_grpc.add_account_adderServicer_to_server(account_adder(), server)
    finance_pb2_grpc.add_update_credit_incomeServicer_to_server(update_credit_income(), server)
    finance_pb2_grpc.add_show_accountsServicer_to_server(show_accounts(), server)
    finance_pb2_grpc.add_transactions_ten_iServicer_to_server(transactions_ten_i(), server)



    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
