# Calculates the remaining amount of money each person is owed/
# in debt after subtracting the cost ('per_person') which is the same
# for each participant.

import sys

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
  print("Usage: weshare_dynamic.py person_1 [contribution in euros] person_2 ... \
    -p x% person_who_pays_less [contribution in euros]")
  print("Write name of person followed by the amount that person contributed to the \
    overall cost of the shared event. If a person made multiple payments, those can be \
    added as separate arguments. People who did not contribute to the costs must \
    have the number 0 as their payment.")
  print("Option '-p' precedes the info of the person who is seen to have to \
    contribute less than other people. '-p' option is followed by the percentage \
    of what that person has to pay compared to other people. This is followed by \
    the name of the person and the amount they contributed.")
  print("Example usage: \nAdam 350 Bertha 10 30 47 Cecilia 0 -p 50% David 0")
  exit()

def check_if_number(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n)

def save_person_who_pays_less(args, paying_less):
  for index, arg in enumerate(args):
    if arg == "-p":
      if index + 2 > len(args) - 1 or args[index + 1][-1] != '%':
        display_usage()
      paying_less.append(args[index + 2])
      # convert percentage into a float number
      percentage = float(args[index + 1][:-1]) / 100
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
        if not num:
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
  all_costs = sum(payments.values())
  print("\nSum of all payments is " + bcolors.OKBLUE + str(all_costs) + bcolors.ENDC + " euros.")
  num_of_people = len(payments) - 1 + paying_less[1] if option_p == True else len(payments)
  share_per_person = all_costs / num_of_people
  print("Share per person is " + bcolors.OKBLUE + str(round(share_per_person, 2)) + bcolors.ENDC + " euros.")

  if option_p:
    share_of_person_paying_less = share_per_person * paying_less[1]
    print("The share of " + bcolors.OKCYAN + paying_less[0] + bcolors.ENDC + " is " + \
      bcolors.OKBLUE + str(round(share_of_person_paying_less, 2)) + bcolors.ENDC + " euros.")

  for person, share in payments.items():
    if option_p and person == paying_less[0]:
      payments[person] -= share_of_person_paying_less
    else:
      payments[person] -= share_per_person

def print_final_payments(trio):
  print(bcolors.OKCYAN + trio[1] + bcolors.ENDC + " will pay " + bcolors.OKCYAN + trio[0] + \
    bcolors.ENDC + ' ' + bcolors.OKGREEN +  str(round(trio[2], 2)) + bcolors.ENDC + " euros")

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
      if (sorted_min[i][1] < 0):
        if sorted_max[i][0] == sorted_min[i][0]:
          break
        if sorted_max[i][1] + sorted_min[i][1] >= 0.0:
          del payments[sorted_min[i][0]]
          payments[sorted_max[i][0]] = sorted_max[i][1] + sorted_min[i][1]
          temp = [sorted_max[i][0], sorted_min[i][0], (sorted_min[i][1] * -1)]
          completed.append(temp)
        else:
          payments[sorted_min[i][0]] = round(sorted_min[i][1] + sorted_max[i][1], 2)
          del payments[sorted_max[i][0]]
          temp = [sorted_max[i][0], sorted_min[i][0], sorted_max[i][1]]
          completed.append(temp)
      i += 1

  # This extra check is to deal with floating point "inconsistency", because
  #  even though the sum of 2 floating points should be exactly 0.0 (and thus
  # should have fallen into the first if clause), it doesn't always register
  if payments:
    if payments.values()[0] == 0.0:
      payments.clear()
  print("\nPayments to be made:")
  for trio in completed:
    print_final_payments(trio)
  print("")

  if (payments):
    print(payments)
    print("Because of rounding, " + str(round(payments.values()[0], 2)) + " euros will be lost.\n")

if __name__ == "__main__":
  main()