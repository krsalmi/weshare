# Almost WeShare
## My own modified version of a cost sharing program
I was at a cabin with my friends for Midsummer and by the end of the weekend, we each had paid different amounts of money for food, 
drinks, napkins, what-have-you, meant for the whole group. Originally we had thought about using a cost-sharing app, like WeShare, but
finally decided against it, because one friend, Lukas, only stayed for one evening.  
I wrote a cost-sharing program suitable for our exact situation, and I wanted to do it in Python, because I'm still getting familiar with
the language.

### How the program works
Because I was writing a program for our specific situation, this program does not take arguments, it works as is. All participants 
(except for Lukas, who we decided would pay 30 euros) and their contributions are saved in a dict called 'payments'. After subtracting
 Lukas' 30 euros, the sum is divided in 7 to get the general amount each of the 7 participants must pay (in our case, a little over 
 47 euros). The 'payments' dict is updated subtracting the general amount from each persons contributions.  
 After, in a larger while loop, the dict is sorted into two lists of tuples, one in ascending order by contributions and one in reverse.
 In the loop, the person who is the most in debt will pay the person who made the biggest contribution and so on. The transactions are
 saved in a little list [who 
 
