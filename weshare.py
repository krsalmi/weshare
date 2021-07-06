# Calculates the remaining amount of money each person is owed/
# in debt after subtracting the cost ('per_person') which is the same
# for each participant.
def calc_remaining_costs_per_person(payments, per_person):
  for person in payments:
    ret = payments[person] - per_person
    payments[person] = ret

def print_final_payments(trio):
  print(trio[1] + " will pay " + trio[0] + ' ' + str(round(trio[2], 2)) + " euros")

def main():
  # Participant Lukas only stayed for one day, so his share was agreed to be 30 euros
  lukas = 30
  remaining = 359.54 - lukas
  per_person = remaining / 7

  # the payements each participant made during the weekend. It was agreed that
  # the Lukas would pay his share to Kris, who paid the most
  payments = {
    'Nate' : 0,
    'Kata' : 53,
    'Justas' : 6,
    'Samvel' : 90,
    'Miina' : 83,
    'Kris' : (45.39 + 30.15 + 52 - lukas),
    'Johannes' : 0
  }

  calc_remaining_costs_per_person(payments, per_person)

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
    sorted_max = sorted(payments.items(),  key=lambda item: item[1], reverse=True)
    i = 0
    while i < len(payments):
      if (sorted_min[i][1] < 0):
        if sorted_max[i][1] + sorted_min[i][1] >= 0:
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

  print('')
  for trio in completed:
    print_final_payments(trio)
  print("Plus Lukas will pay Kris 30 euros.\n")

  if (payments):
    print("Because of rounding, " + str(round(payments.values()[0], 2)) + " euros will be lost.\n")

if __name__ == "__main__":
  main()