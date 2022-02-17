from datetime import datetime
import converter
import pymssql

    # check if the requested cash is affordable
def check_valid_cash(cash, current_user):
    credit = user_credit(current_user)
    if cash < (credit - 500000):
        return True
    else:
        return False
    # bank process
def withdrawal_action(bank_name, account_number, cash):
    # bank process
    pass
    #update credit after withdrawal
def user_credit_update(cash, current_user):
    now = datetime.now()
    y, m, d = int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d"))
    now_jalili = converter.gregorian_to_jalali(y, m, d)
    jalili_date = "{:n}{:02d}{:02d}{}{}{}".format(now_jalili[0], now_jalili[1], now_jalili[2],
                                    now.strftime("%H"), now.strftime("%M"),
                                    now.strftime("%S"))
    int_jalili_date = int(jalili_date)
    conn = connectToDatabase()
    cursor = conn.cursor()
    payCode = jalili_date[-8:-1]
    status = 'ok'
    cursor.execute("""INSERT INTO dbo.Payments (ragDateTime, amount, status,\
     serviceProvider, type, payCode) VALUES ('{}', '{}', '{}' , '{}', '{}', '{}')""" \
                   .format(int_jalili_date, cash, status, current_user, 'withdraw', payCode))
    conn.commit()
    cursor.close()
    conn.close()
    # read from database and calculate user credit
def user_credit(current_user):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("""SELECT amount FROM Payments WHERE serviceProvider = '{}'\
        AND type = 'paid' """.format(current_user))
    rows = cursor.fetchall()
    totalIncome = 0
    for row in rows:
        totalIncome = row[0] + totalIncome
    cursor.execute("""SELECT amount FROM Payments WHERE serviceProvider = '{}'\
            AND type = 'withdraw' """.format(current_user))
    rows = cursor.fetchall()
    totalWithdrawal = 0
    for row in rows:
        totalWithdrawal = row[0] + totalWithdrawal
    return totalIncome - totalWithdrawal
    # read from database and calculate this month user income
def this_month_user_incom(current_user):
    now = datetime.now()
    y, m, d = int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d"))
    now_jalili = converter.gregorian_to_jalali(y, m, d)
    start_current_month = int("{:n}{:02d}01000000".format(now_jalili[0], now_jalili[1]))
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("""SELECT amount FROM Payments WHERE serviceProvider = '{}'\
    AND type = 'paid' AND ragDateTime > '{}'""".format(current_user, start_current_month))
    rows = cursor.fetchall()
    income = 0
    for row in rows:
        income = row[0] + income
    return income
    # read current user bank accounts from database
def user_accounts(current_user):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("""SELECT fullname from dbo.ServiceProviders WHERE username='{}'"""\
                   .format(current_user))
    owner = cursor.fetchall()
    cursor.execute("""SELECT Bank,AccountNumber,ShabaNumber FROM dbo.Account\
         WHERE serviceProvider='{}'""".format(current_user))
    rows = cursor.fetchall()
    return rows, owner
    # read 10 ith recent transaction from database
def i_tenth_transaction(current_user, i):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("""SELECT type,amount,ragDateTime,payCode FROM dbo.Payments\
     WHERE serviceProvider='{}' ORDER BY id OFFSET {} ROWS FETCH NEXT 10 ROWS ONLY"""\
                   .format(current_user, (i-1)*10))
    rows = cursor.fetchall()
    return rows
    #addin new bank account to database
def add_new_account(current_user, bank_name, account_number, shabaNumber):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO dbo.Account (serviceProvider, Bank, AccountNumber, ShabaNumber)\
    VALUES ('{}', '{}', '{}' , '{}')"""\
                   .format(current_user, bank_name, account_number, shabaNumber))
    conn.commit()
    cursor.close()
    conn.close()
    #make a connection to database
def connectToDatabase():
    conn = pymssql.connect(host='185.128.82.62:11433', user='arefi', password="UUHtBe8nD5vMEREN",
                           database='Limoo_Trial')
    return conn
