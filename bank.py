class Person:
    def __init__(self, name, age, address, social_security):
        self.name = name
        if type(name) != str:
            raise TypeError("arguement \"name\" must be of type str")
        self.age = age
        if type(age) != int:
            raise TypeError("arguement \"age\" must be of type int")
        self.address = address
        if type(address) != str:
            raise TypeError("arguement \"address\" must be of type str")
        self.social_security = social_security
        if len(social_security) != 9:
            raise ValueError("arguement \"social_security\" must have 9 digits")


    def set_address(self, address):
        self.address = address

    def __str__(self):
        string = "-----------------------------\n"
        string += "Name:            " + self.name + "\n"
        string += "Age:             " + str(self.age) + "\n"
        string += "Address:         " + self.address + "\n"
        string += "Social Security: " + self.social_security + "\n"
        string += "----------------------------"
        return string
    __repr__ = __str__


class Employee(Person):
    def __init__(self, name, age, address, social_security, position):
        Person.__init__(self, name, age, address, social_security)
        if age < 16:
            raise ValueError("You must be 16 or older to work at the bank")
        self.position = position

    def __str__(self):
        string = "-----------------------------\n"
        string += "Employee:               " + self.name + "\n"
        string += "Position:               " + self.position + "\n"
        string += "Age:                    " + str(self.age) + "\n"
        string += "Address:                " + self.address + "\n"
        string += "Social Security Number: " + self.social_security + "\n"
        string += "-----------------------------"
        return string
    __repr__ = __str__


class Customer(Person):
    def __init__(self, name, age, address, social_security):
        Person.__init__(self, name, age, address, social_security)
        if age < 16:
            raise ValueError("You must be 16 or older to open an account")
        self.accounts = []

    def add_account(self, account, password):
        if not isinstance(account, Account) or password != "notthepassword":
            return False
        for acc in self.accounts:
            if acc.account_number == account.account_number:
                return False
        self.accounts.append(account)
        return True

    def delete_account(self, account_number, password):
        if password != "notthepassword":
            return False
        for i in range(len(self.accounts)):
            if self.accounts[i].account_number == account_number:
                self.accounts.pop(i)
                print("The " + str(account_number) + " has been sucessfully terminated")
                return True
        return False

    def get_account(self, account_number):
        for x in self.accounts:
            if x.account_number == account_number:
                return x
        return None

    def __str__(self):
        string = "-----------------------------\n"
        string += "Customer:               " + self.name + "\n"
        string += "Age:                    " + str(self.age) + "\n"
        string += "Address:                " + self.address + "\n"
        string += "Social Security Number: " + self.social_security + "\n"
        string += "-----------------------------"
        for account in self.accounts:
            string += str(account)
        return string
    __repr__ = __str__



class Account:
    def __init__(self, account_number, account_type, balance, interest_rate, pin, active = True):
        self.active = active
        self.account_number = account_number
        if type(account_number) != str:
            raise TypeError("\"account_number\" must be of type str")
        if len(account_number) != 5:
            raise ValueError("\"account number\" must have a length of 5")
        self.balance = balance
        if type(balance) != float:
            raise TypeError("\"balance\" is not of type float")
        if balance < 0:
            raise ValueError("The balance must be positive")
        self.account_type = account_type
        if type(account_type) != str:
            raise TypeError("\"account_type\" is not of type str")
        self.interest_rate = interest_rate * .01
        self.pin = pin
        if type(pin) != str:
            raise TypeError("\"pin\" must be of type str")
        if len(pin) != 4:
            raise ValueError("\"pin\" must contain 4 digits")

    def deposit(self, amount, password):
      	if (password == "notthepassword" or password == "letmein") and self.active:
            self.balance += amount
            return ("%.2f" % self.balance)
        else:
            return -1.0

    def withdraw(self, amount, password):
        if not(password == "notthepassword" or password == "letmein") or not self.active or amount > self.balance:
            return -1.0
        else:
            self.balance -= amount
            return ("%.2f" % self.balance)

    def transfer_money(self, amount, account, password):
        if password == "letmein" or password == "notthepassword":
      	    if isinstance(account, Account) and self.withdraw(amount, password) != -1 and account.deposit(amount, password):
                return True
        return False

    def access_ATM(self):
        x = int(input("How much cash would you like to recieve: "))
        pin = input("Enter your 4-digt pin to continue: ")
        if pin == self.pin and self.withdraw(x, "letmein") != -1:
			return True
        else:
            return False
    def check_balance(self):
      return self.balance

    def future_value(self, time):
      big_amount = int((1 + (self.interest_rate * float(time) / 12)) * self.balance * 100)
      return float(big_amount) / 100

    def __str__(self):
        string = "\n" + self.account_type + " Account\n"
        string += "-----------------------------\n"
        string += "Account Number: " + str(self.account_number) + "\n"
        string += "Balance:        " + str(self.balance) + "\n"
        string += "Interest Rate:  " + str(self.interest_rate * 100) + "\n"
        string += "-----------------------------\n"
        return string
    __repr__ = __str__


class Loan(Account):
    def __init__(self, account_number, loan_amount, time, interest_rate, credit_score):
        Account.__init__(self, account_number, "loan", loan_amount, interest_rate, "0000", active = True)
        self.time = time
        if type(time) != int:
            raise TypeError("\"time\" must be of type int")
        self.loan_amount = loan_amount
        if type(loan_amount) != int and type(loan_amount) != float:
            raise TypeError("\"loan_amount\" must be of type float or int")
        self.credit_score = credit_score
        if type(credit_score) != int:
            raise TypeError("\"credit_score\" must be of type int")
        if credit_score < 550:
            raise ValueError("Credit Score must be above 550 to take out a loan")

    def get_interest_rate(self):
        return self.interest_rate

    def monthly_payment(self):
        numer = (self.interest_rate / 12) * self.loan_amount
        denom = 1 - (1 + (self.interest_rate / 12))**(self.time * -1)
        total = int((numer / denom) * 100)
        return float(total) / 100

    def make_payment(self, amount):
        if amount < self.balance:
            self.balance -= amount
            return self.balance
        else:
            self.balance = 0
            return 0

    def __str__(self):
        string = "Loan\n"
        string += "-----------------------------\n"
        string += "Account Number:    " + self.account_number + "\n"
        string += "Remaining Balance: $" + str(self.balance) + "\n"
        string += "Monthly Payment:   " + str(self.monthly_payment()) + "\n"
        string += "Interest Rate:     " + str(self.interest_rate * 100) + "%\n"
        string += "Initial Balance:   $" + str(self.loan_amount) + "\n"
        string += "-----------------------------\n"
        return string


    def check_LOAN_comp_interest(self, comp_time):
        if self.time > 480:
            print("Can't be more than 40 years")
            return False

        rate = self.credit_score / 10000
        est_payment = self.loan_amount * (1 + (rate / comp_time)) ** (4 * self.time)
        return ("%.2f" % est_payment)

    def check_LOAN_simple_interest(self):
        if self.time > 240:
            print("Can't do more than 20 years, can't rip us off more!")
            return False
        rate = self.credit_score / 20000
        est_payment = self.loan_amount * rate * self.time
        return ("%.2f" % est_payment)


class Bank:
    def __init__(self):
        self.employees = []
        self.customers = []
        self.positions = ["Teller", "Manager"]


    def add_customer(self, customer, password):
        if password != "notthepassword":
            return False
        for cust in self.customers:
            if cust.social_security == customer.social_security:
                return False
        self.customers.append(customer)
        return True

    def delete_customer(self, customer):
        self.customers.remove(customer)

    def find_customer(self, social_security):
        for customer in self.customers:
            if customer.social_security == social_security:
                return customer
        return None

    def add_employee(self, employee, password):
        if password != "notthepassword":
            return False
        for emp in self.employees:
            if emp.social_security == employee.social_security:
                return False
        if not isinstance(employee, Employee):
            return False
        if employee.position in self.positions:
            self.employees.append(employee)
            return True
        else:
            return False

    def get_customers(self):
        return self.customers

    def delete_employee(self, employee_ss, password):
        if password != "notthepassword":
            return False
        for i in range(len(self.employees)):
            if self.employees[i].social_security == employee_ss:
                self.employees.pop(i)
                return True
        return False

    def find_employee(self, social_security):
        for employee in self.employees:
            if employee.social_security == social_security:
                return employee
        return None

    def get_employees(self):
        return self.employees

    def get_employees_by_position(self, position):
        emps = []
        for emp in self.employees:
            if emp.position == position:
                emps.append(emp)
        return emps

    def add_position(self, position):
        if type(position) != str:
            raise TypeError("position must be of type \"str\"")
        self.positions.append(position)

    def delete_position(self, position):
        self.positons.remove(position)

    def __str__(self):
        string = "\nEmployees\n"
        for employee in self.employees:
            string += str(employee)
        string += "\nCustomers\n"
        for customer in self.customers:
            string += str(customer)
        return string
    __repr__ = __str__

##########################################################
#--------------MAIN--------------------------------------#
##########################################################

#1
def create_employee(bank):
    name = input("Enter the employee name: ")
    age = int(input("Enter the employee age: "))
    address = input("Enter the employee address: ")
    social = input("Enter the employee Social Security number(9 digits): ")
    position = input("Enter Employee position: ")
    try:
        emp = Employee(name, age, address, social, position)
    except (TypeError, ValueError):
        return "Incorrect values entered for employee. Please try again"
    emp = Employee(name, age, address, social, position)
    passw = input("Please enter a manager password to continue: ")
    if bank.add_employee(emp, passw):
      	if emp.position == "Manager":
            return str(emp) + "\nThe Manager password is \"notthepassword\""
        else:
            return str(emp) + "\nThe employee password is \"letmein\""
    else:
        return "An error occured. Please try again"

#1.1
def employee_info(bank):
    ssn = input("Enter the social security number of the employee(9 digits): ")
    emp = bank.find_employee(ssn)
    if emp == None:
        return "This employee does not exist."
    return str(emp)

#1.2
def delete_employee(bank):
    emp_ss = input("Enter the social security number of the employee to delete: ")
    passw = input("Please enter a manager password to continue: ")
    if bank.delete_employee(emp_ss, passw):
        return "Employee successfully deleted"
    return "employee not deleted"

#2
def create_account(bank):
    SSN = input("Please enter your Social Security Number(9 digits): ")
    cust = bank.find_customer(SSN)
    if cust == None:
        y = input("Customer not found. Would you like to create a Customer?(Y or N) ")
        if y.lower() == "y":
            return create_customer(bank)
    else:
        number = input("Please create an Account Number (5 digits): ")
        pin = input("Please create a 4-digit pin number: ")
        account_type = input("Please enter Account Type (Checking or Savings): ")
        balance = float(input("Please enter Balance: "))
        interest_rate = float(input("Please enter your interest rate: "))
        accnt = None
        try:
            accnt = Account(number, account_type, balance, interest_rate, pin)
        except (TypeError, ValueError):
            return "Error: make sure all the values entered are correct"
        passw = input("Please enter a manager password to create an account: ")
        if cust.add_account(accnt, passw):
        	return str(accnt)
        else:
            return "An error occurred while creating an account"

#2.1
def withdraw(bank):
    cust_social = input("What is the customers Social Security Number(9 digits): ")
    cust = bank.find_customer(cust_social)
    if cust == None:
        return "This customer does not exist"
    print("Welcome " + cust.name)
    acct_num = input("What is the account number you would like to access: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    amount = float(input("Enter amount of money to withdraw: "))
    passw = input("Enter a Teller or Manager Password to continue: ")
    amt = acct.withdraw(amount, passw)
    if amt == -1.0:
        return "Error in withdraw.. Please try again"
    else:
        return str(amt)

#2.2
def deposit(bank):
    cust_social = input("What is the customers Social Security Number(9 digits): ")
    cust = bank.find_customer(cust_social)
    if cust == None:
        return "This customer does not exist"
    print("Welcome " + cust.name)
    acct_num = input("What is the account number you would like to access: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    amount = float(input("Enter amount of money to deposit: "))
    passw = input("Enter a Teller or Manager Password to continue: ")
    amt = acct.deposit(amount, passw)
    if amt == -1.0:
        return "Error in deposit. Please try again"
    else:
        return str(amt)
#2.3
def transfer_money(bank):
    cust1_social = input("Enter the Social Security of the customer to remove the money from: ")
    acct1_num = input("Enter the account number for this customer: ")
    cust2_social = input("Enter the Social Security of the customer to add the money to: ")
    acct2_num = input("Enter the account number for this customer: ")
    cust1 = bank.find_customer(cust1_social)
    cust2 = bank.find_customer(cust2_social)
    if cust1 == None or cust2 == None:
        return "One of the customers you entered was not valid"
    acct1 = cust1.get_account(acct1_num)
    acct2 = cust2.get_account(acct2_num)
    if acct1 == None or acct2 == None:
        return "One of the accounts you entered is not valid"
    ammt = float(input("Enter the amount of money to transfer: "))
    passw = input("Enter a manager or teller password to continue with transaction: ")
    if acct1.transfer_money(ammt, acct2, passw):
        return str(ammt) + " successfully transferred"
    else:
        return "An error occurred. Please try again"

#2.4
def ATM(bank):
    social = input("Enter the customer Social Security number(9 digits): ")
    cust = bank.find_customer(social)
    if cust == None:
        return "Not a valid customer"
    acct_num = input("Hello " + cust.name + ". Enter the account number: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    if acct.access_ATM():
        return str(acct.check_balance())
    else:
        return "An error occurred. Please try again"

#2.5
def check_future(bank):
    cust_social = input("Enter the customers social security number(9 digits): ")
    cust = bank.find_customer(cust_social)
    if cust == None:
        return "Not a valid customer"
    acct_num = input("Enter the account number: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account is not valid"
    time = input("How many months from now do you want to check the balance: ")
    return str(acct.future_value(time))

#2.6
def current_balance(bank):
    cust_social = input("Enter the customers social security number(9 digits): ")
    cust = bank.find_customer(cust_social)
    if cust == None:
        return "This customer does not exist"
    acct_num = input("Enter the account number: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account is not valid"
    return str(acct.check_balance())

#2.7
def account_info(bank):
    ssn = input("Enter the social security numnber of the customer(9 digits): ")
    cust = bank.find_customer(ssn)
    if cust == None:
        return "There is no customer with this social security numnber"
    acct_num = input("Hello " + cust.name + ". Please enter the account number: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    return str(acct)

#2.8
def delete_account(bank):
    cust_ss = input("Enter the customer social security number(9 digits): ")
    cust = bank.find_customer(cust_ss)
    account_number = input("Please enter the account number you would like to delete: ")
    acct = cust.get_account(account_number)
    passw = input("Please enter Manager Password to continue: ")
    if cust.delete_account(account_number, passw):
        return "Account successfuppy deleted"
    else:
        return "An error occurred. Please try again"

#3
def take_out_loan(bank):
    ssn = input("Please enter your Social Security Number: ")
    cust = bank.find_customer(ssn)
    if cust == None:
        y = input("Customer not found. Would you like to create a Customer?(Y or N) ")
        if y.lower() == "y":
            return create_customer(bank)
    else:
        acct_num = input("Please enter account number: ")
        amount = float(input("Please enter the loan amount: "))
        interest_rate = float(input("Please enter the interest rate: "))
        time = int(input("Please enter the amount of time (in months) to pay back the loan: "))
        c_score = int(input("Please enter your credit score (above 550): "))
        try:
            loan = Loan(acct_num, amount, time, interest_rate, c_score)
        except (TypeError, ValueError):
            return "One of the values entered was not correct"
        passw = input("Enter a manager password to continue: ")
        cust.add_account(loan, passw)
        return loan

#3.1
def check_interest():
    loan_amount = float(input("Please enter your desired loan amount: "))
    time = int(input("Please enter your time limit of your loan: "))
    interest_rate = float(input("Enter the interest_rate: "))
    credit_score = int(input("Please enter your credit score (above 550): "))
    comp_time = int(input("How many time would you like to have the loan compounded per year (for compound interest): "))
    loan = Loan("10001", loan_amount, time, interest_rate, credit_score)
    est_comp = loan.check_LOAN_comp_interest(comp_time)
    if est_comp != False:
        print("Your compound interest would be:", est_comp)
    else:
        print("Error 404: Please make sure your typed in your info correctly")
    est_simp = loan.check_LOAN_simple_interest()
    if est_simp != False:
        print("Your simple interest would be:", est_simp)
    else:
        print("Error 404: Please make sure your typed in your info correctly")

#3.2
def check_monthly(bank):
    ssn = input("Please enter your Social Security Number(9 digits): ")
    cust = bank.find_customer(ssn)
    if cust == None:
        return "This account does not exist"
    acct_num = input("Enter the account number of the loan: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    if not isinstance(acct, Loan):
        return "Account is not of type Loan"
    return str(acct.monthly_payment())

#3.3
def make_payment(bank):
    ssn = input("Please enter your Social Security Number(9 digits): ")
    cust = bank.find_customer(ssn)
    if cust == None:
        return "This customer does not exist"
    acct_num = input("Enter the account number of the loan: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    if not isinstance(acct, Loan):
        return "Account is not of type Loan"
    ammt = float(input("Enter the amount for payment: "))
    return str(acct.make_payment(ammt))

#3.4
def loan_info(bank):
    ssn = input("Please enter your Social Security Number(9 digits): ")
    cust = bank.find_customer(ssn)
    if cust == None:
        return "This customer does not exist"
    acct_num = input("Enter the account number of the loan: ")
    acct = cust.get_account(acct_num)
    if acct == None:
        return "This account does not exist"
    if not isinstance(acct, Loan):
        return "Account is not of type Loan"
    return str(acct)

#4
def create_customer(bank):
    name = input ("Please enter your name: ")
    age = int(input ("Please enter your age(Over 16): "))
    SSN = input ("Please enter your Social Security(9 digits): ")
    address = input ("Please enter your address: ")
    password = input("Please enter a manager password to continue: ")
    cust = None
    try:
        cust = Customer(name, age, address, SSN)
    except (TypeError, ValueError):
        return "The information entered is not correct"
    if bank.add_customer(cust, password):
        return str(cust)
    else:
        return "An error occured. Please try again"

#4.1
def customer_info(bank):
    ssn = input("Enter the social security number of the customer(9 digits): ")
    cust = bank.find_customer(ssn)
    if cust == None:
        return "This customer does not exist"
    return str(cust)

#5
def get_employees(bank):
    string = ""
    for employee in bank.get_employees():
      string += str(employee)
      string += "\n"
    return string

#6
def get_customers(bank):
    string = ""
    for customer in bank.get_customers():
        string += str(customer)
        string += "\n"
    return string

def main():
    bank = Bank()
    print("To start using the bank please create a manager.")
    no_mang = True
    while no_mang:
        name = input("Enter the manager name: ")
        age = int(input("Enter the manager age (above 16): "))
        address = input("Enter the manager address: ")
        social = input("Enter the manager Social Security number(9 digits): ")
        emp = None
        try:
            emp = Employee(name, age, address, social, "Manager")
        except (TypeError, ValueError):
            print("Please enter the correct values")
            continue
        if bank.add_employee(emp, "notthepassword"):
            print("Manager successfully added. The password is \"notthepassword\"")
            no_mang = False
        else:
            print("Failed to create manager. Please try again")

    while True:
        print("WELCOME TO THE BANK, please press...")
        print("------------------------------------")
        print(1, "  -- Create Employee")
        print(1.1, "-- Check Employee Information")
        print(1.2, "-- Delete Employee", "\n")

        print(2, "  -- Create Account")
        print(2.1, "-- Withdraw")
        print(2.2, "-- Deposit")
        print(2.3, "-- Transfer Money")
        print(2.4, "-- Access ATM")
        print(2.5, "-- Check Future Balance")
        print(2.6, "-- Check Current Balance")
        print(2.7, "-- Check Account Information")
        print(2.8, "-- Delete Account", "\n")

        print(3, "  -- Take out Loan")
        print(3.1, "-- Check Interest")
        print(3.2, "-- Check Monthly Payment")
        print(3.3, "-- Make Payment")
        print(3.4, "-- Check Loan Information", "\n")

        print(4, "  -- Create Customer")
        print(4.1, "-- Check Customer Information", "\n")

        print(5, "  -- Print Employee List")
        print(6, "  -- Print Customer List")
        print(7, "  -- Quit")
        print("------------------------------------")
        option = float(input("Option: "))
#---------------------------------------------------
        if option == 1:
            print(create_employee(bank))
        elif option == 1.1:
            print(employee_info(bank))
        elif option == 1.2:
            print(delete_employee(bank))
#---------------------------------------------------
        elif option == 2:
            print(create_account(bank))
        elif option == 2.1:
            print(withdraw(bank))
        elif option == 2.2:
            print(deposit(bank))
        elif option == 2.3:
            print(transfer_money(bank))
        elif option == 2.4:
            print(ATM(bank))
        elif option == 2.5:
            print(check_future(bank))
        elif option == 2.6:
            print(current_balance(bank))
        elif option == 2.7:
            print(account_info(bank))
        elif option == 2.8:
            print(delete_account(bank))
#---------------------------------------------------
        elif option == 3:
            print(take_out_loan(bank))
        elif option == 3.1:
            print(check_interest())
        elif option == 3.2:
            print(check_monthly(bank))
        elif option == 3.3:
            print(make_payment(bank))
        elif option == 3.4:
            print(loan_info(bank))
#---------------------------------------------------
        elif option == 4:
            print(create_customer(bank))
        elif option == 4.1:
            print(customer_info(bank))
#---------------------------------------------------
        elif option == 5:
            print(get_employees(bank))
        elif option == 6:
            print(get_customers(bank))
        elif option == 7:
          	print("Good doing business with you!")
            break
        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
