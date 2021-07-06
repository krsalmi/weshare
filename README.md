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
 saved in a little list \[who gets paid, who pays, how much\] which is then added to 'completed', a list of lists. People, who have
 gotten to zero after a payment, are removed from the 'payments' dictionary. The loop will repeat until there are either no, or just one, person left in the 'payments' dictionary. When the program reaches its end, it prints the 'completed' list out in the form of
 who pays who and how much. If there is one person left in the 'payments' dict, (which can happen if we have an uneven number of 
 participants), the program states finally the amount of money that is 'lost' due to rounding etc.
   
   Final output  
 <img width="325" alt="Screen Shot 2021-07-06 at 21 30 26" src="https://user-images.githubusercontent.com/57495339/124649880-b902c700-dea1-11eb-99ef-5657ad556756.png">

 ### Things I learned
 I'm glad I wrote this program in Python, partly because I'm still trying to learn the language, and partly because I felt that it
 would fit this kind of problem well. I ended up using a lot of time understanding the data structures and how they might change. For
 example, it took me a while to understand that a sorted dict is actually a list of tuples, and because of that, the points of data are
 immutable. That's why I ended up updating the contributions of each person directly to the 'payments' dictionary, and not to the
 sorted lists.
 
