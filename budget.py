

def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    names = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), names))
    names = list(map(lambda description: description.ljust(max_length), names))
    for x in zip(*names):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")



class Category:


  def __init__(self, name):
    self.name = name
    self.ledger = list()
    
  
  def __str__(self):
    title = f'{self.name:*^30}\n'
    items = ''
    total = 0
    for item in self.ledger:
      items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + '\n'
      total += item['amount']
    output = title + items + 'Total: ' + str(total)
    return output
        
    
  def deposit(self, amount, description=''):
    """
    A deposit method that accepts an amount and description. If no
    description is given, it should default to an empty string. The
    method should append an object to the ledger list in the form of
    {'amount': amount, 'description': description}.
    """
    self.ledger.append({'amount': amount, 'description': description})
    
    
  def withdraw(self, amount, description=''):
    """
    A withdraw method that is similar to the deposit method, but the 
    amount passed in should be stored in the ledger as a negative number. 
    If there are not enough funds, nothing should be added to the ledger. 
    This method should return True if the withdrawal took place, and False otherwise.
    """
    if self.check_funds(amount):
      self.ledger.append({'amount': -amount, 'description': description})
      return True
    return False
  
  
  def get_balance(self):
    """
    A get_balance method that returns the current balance of the budget 
    category based on the deposits and withdrawals that have occurred.
    """
    total_cash = 0
    for item in self.ledger:
      total_cash += item['amount']
    return total_cash
  
  
  def transfer(self, amount, category):
    """
    A transfer method that accepts an amount and another budget category 
    as arguments. The method should add a withdrawal with the amount and the 
    description "Transfer to [Destination Budget Category]". The method 
    should then add a deposit to the other budget category with the amount 
    and the description "Transfer from [Source Budget Category]". If there 
    are not enough funds, nothing should be added to either ledgers. This 
    method should return True if the transfer took place, and False otherwise.
    """
    if self.check_funds(amount):
      self.withdraw(amount, 'Transfer to ' + category.name)
      category.deposit(amount, 'Transfer from ' + self.name)
      return True
    return False
  
  
  def check_funds(self, amount):
    """
    A check_funds method that accepts an amount as an argument. It returns 
    False if the amount is greater than the balance of the budget category 
    and returns True otherwise. This method should be used by both the 
    withdraw method and transfer method.
    """
    if amount > self.get_balance():
      return False
    return True
  