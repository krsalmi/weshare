# Calculates the remaining amount of money each person is owed/
# in debt after subtracting the cost ('per_person') which is the same
# for each participant.

import sys
from decimal import *

option_p = False

# Color class from Blender build scripts:
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def display_usage():
  print("\nUsage: weshare_dynamic.py person_1 [contribution in euros] person_2 ...\
  -p x% person_who_pays_less [contribution in euros]\n")
  print("Write name of person followed by the amount that person contributed to the\
  overall cost of the shared event. If a person made multiple payments, those can be\
  added as separate arguments. People who did not contribute to the costs must\
  have the number 0 as their payment.")
  print("\nOption '-p' precedes the info of the person who is seen to have to\
  contribute less than other people. '-p' option is followed by the percentage\
  of what that person has to pay compared to other people. This is followed by\
  the name of the person and the amount they contributed.")
  print("\nExample usage: \npythn weshare_dynamic.py Adam 350 Bertha 10 30 47 Cecilia 0 -p 50% David 0")
  exit()

def check_if_number(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return Decimal(n)

def save_person_who_pays_less(args, paying_less):
  for index, arg in enumerate(args):
    if arg == "-p":
      if index + 2 > len(args) - 1 or args[index + 1][-1] != '%':
        display_usage()
      paying_less.append(args[index + 2])
      # convert percentage into a float number
      percentage = Decimal(args[index + 1][:-1]) / 100
      paying_less.append(percentage)
      args.pop(index + 1)
      args.pop(index)
      global option_p
      option_p = True
  return(args)


def handle_command_line_args(args):
  len_arg = len(args) - 1
  if (len_arg <= 1):
    display_usage()

  payments = {}
  i = 1
  j = i + 1
  amount = 0
  while (i <= len_arg):
    if not check_if_number(args[i]):
      name = args[i]
      while (j <= len_arg):
        num = check_if_number(args[j])
        if num is False:
          if (j == i + 1):
            print("Error, all names must be followed by a number")
            exit()
          else:
            break
        else:
          amount += num
        j += 1
    else:
      print("Error, amount of money must be preceded by a name")
      exit()
    payments[name] = amount
    i = j
    j = i + 1
    amount = 0
  return (payments)


def calc_remaining_costs_per_person(payments, paying_less):
  all_costs = (sum(payments.values())).quantize(Decimal("1.00"))

  print("\nSum of all payments is " + bcolors.OKBLUE + str(all_costs) + bcolors.ENDC + " euros.")
  num_of_people = len(payments) - 1 + paying_less[1] if option_p == True else len(payments)
  share_per_person = all_costs / num_of_people
  share_per_person = share_per_person.quantize(Decimal("1.00"))
  print("Share per person is " + bcolors.OKBLUE + str(share_per_person) + bcolors.ENDC + " euros.")

  if option_p:
    share_of_person_paying_less = (share_per_person * Decimal(paying_less[1])).quantize(Decimal("1.00"))
    print("The share of " + bcolors.OKCYAN + paying_less[0] + bcolors.ENDC + " is " + \
      bcolors.OKBLUE + str(share_of_person_paying_less) + bcolors.ENDC + " euros.")

  for person in payments:
    if option_p and person == paying_less[0]:
      payments[person] -= share_of_person_paying_less
    else:
      payments[person] -= share_per_person

def print_final_payments(completed):

  print("\nPayments to be made:")
  for trio in completed:
    print(bcolors.OKCYAN + trio[1] + bcolors.ENDC + " will pay " + bcolors.OKCYAN + trio[0] + \
    bcolors.ENDC + ' ' + bcolors.OKGREEN +  str(trio[2].quantize(Decimal("1.00"))) + bcolors.ENDC + " euros")

def print_remaining(payments):
  print("\nBecause of rounding, costs can not be shared 100% equally:")
  for person, costs in payments.items():
    print(bcolors.OKCYAN + person + bcolors.ENDC + " will end up paying ", end = " ")
    if costs < 0:
      print(bcolors.WARNING + str(costs * -1) + bcolors.ENDC + " euros too little.")
    else:
      print(bcolors.WARNING + str(costs) + bcolors.ENDC + " euros too much.")
  print("")

def main():
  paying_less = []
  payments = {}
  args = save_person_who_pays_less(sys.argv, paying_less)
  payments = handle_command_line_args(args)
  calc_remaining_costs_per_person(payments, paying_less)

  temp = [] # a list that will include [who gets paid, who pays, how much]
  completed = [] # will be a list of smaller 'temp' lists

  # the while loop starts with defining two lists of tuples. 'sorted_min' will
  # have the participants and their owed money in an ascending list, the 'sorted_max'
  # will have the same list in reverse order.
  # The person who owes the most will end up paying the person who paid the most, etc.
  # The person who gets paid, the person who pays, and the amount, will first saved as a
  # temp list and then added to the 'completed' list of lists'. People, whose payments get
  # to 0 will be deleted from the 'payments' dictionary and until there is 1 or none
  # participants in the dictionary, the loop will start over again.
  while bool(payments) and len(payments) != 1:
    sorted_min = sorted(payments.items(),  key=lambda item: item[1])
    # reverse sorted_min list
    sorted_max = sorted_min[::-1]

    i = 0
    while i < len(payments):
      if (sorted_min[i][1] < 0 and sorted_max[i][1] > 0):
        if sorted_max[i][1] + sorted_min[i][1] >= 0.0:
          del payments[sorted_min[i][0]]
          if sorted_max[i][1] + sorted_min[i][1] == 0.0:
            del payments[sorted_max[i][0]]
          else:
            payments[sorted_max[i][0]] = sorted_max[i][1] + sorted_min[i][1]
          temp = [sorted_max[i][0], sorted_min[i][0], (sorted_min[i][1] * -1)]
          completed.append(temp)
        else:
          payments[sorted_min[i][0]] = sorted_min[i][1] + sorted_max[i][1]
          del payments[sorted_max[i][0]]
          temp = [sorted_max[i][0], sorted_min[i][0], sorted_max[i][1]]
          completed.append(temp)
      i += 1

  print_final_payments(completed)

  if (payments):
    print_remaining(payments)


    # print(payments)
    # payment_values = payments.values()
    # lost_money = list(payment_values)[0]
    # print("Because of rounding, " + str(lost_money.quantize(Decimal('1.00'))) + " euros will be lost.\n")

if __name__ == "__main__":
  main()
