# Simulations-of-the-Art-Fair
In  the  Art  Fair,  different  student  societies  gather,  promote  and  share  their  culture  with all  students.  The  Art  Fair  takes  place  at  the  University  Mall.  There  are  many  booths  set  up  in the  Mall,  and  each  society  stays  in  one  Mall.  The  Art  Fair  lasts  for  2  days,  operating  from  11 am to  6  pm

# Tasks completed
1.  Simulations of the Art Fair
2.  System Performance Comparison with Two-stage sampling 
3.  Comparison with system that support Group Promotion
4.  Regression Analysis 


# Conclustion
1.  Day 1 the preference remains the same. But in day2, the departure time of art fair is later than base case after reordering the preference, from [17,8] to [8,17]. Reordering the preference according to distance will reduce the travel time but not necessarily reduce the waiting time.
2.  Using 2-stage sampling at 5% significance level, we can conclude that the system 2 has a shorter tatal waiting time compare to system 1.
3.  In set_next function, while giving student promotion. It sends the serving list to the function find_com to find the most common shared booth in the serving list. If the booth is serving 6 student and 3 of them are having a same interested booth x in later, then the function will swap the booth x to the front of the preference list of those 3-student. Given that most likely students will change their mind and give top priority to the shared booth. The q set as 0.4 which if they find match student in group promotion then they will visit the common booth together with 0.3.
4.  We can conclude that the promotion time have highest weighting which shows it has a large significant effect on the traveling time. Increase the time on the promotion can reduce the time of traveling time of student. And the booth number is the second high weighting.

# Data and Simulations
<img src="data/Annotation%202022-06-15%20191226.jpg" class="center">
