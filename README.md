# Menu-program-
#hello

import time<br>
import os

def prime (a):
	fac = 0 
	for i in range(1, a +1):
		 if (a%i == 0): 		
		 	fac+=1

	if (fac == 2): 
		print ("number is prime ")

	else:
		print ("number is not prime")

	return "thank you"

def armstrong (a):

	x = a

	b = 0 
	d = 0 
	while (a != 0):
		 d = a%10 
		 b=b+d **3 
		 a = a//10

	if (x == b):

		print("number is armstrong")

	else:

		print ("number is not armstrong")

	return "thank you"

def leap_year (a):

	if (a % 4 == 0): 
		print(a,"is a leap year")
	else:
		print(a, "is not a leap year")

	return "thank you"

def odd_even (a):

	if (a%2==0):
		print (a,"is even")
	else:
		print (a, " is odd ")

	return "thank you"

n = 0

while (n != 5):

	print ("------------------------")

	print (" programe list ")

	print ("------------------------")

	print ("1.prime number ")

	print ("2.armstrong number ")

	print ("3.leap year")

	print ("4.odd even ")

	print ("5.exit")

	print ()

	n = int (input ("enter your choice:"))

	if (n==1):

		p= int (input ("enter your number: "))

		print (prime(p))

		print ()


	if (n==2):

		p=int (input ("enter your number: "))

		print (armstrong(p))

		print ()

	if (n==3):

		p=int (input ("enter your year: "))

		print (leap_year(p))

		print ()

	if (n==4):

		p = int (input ("enter your number: "))

		print (odd_even(p))

		print ()

	if(n>5):

		print ("please enter a valid index")

		print ()

	time.sleep(2)
	os.system('clear')
	
if (n==5):
	print('thank you')


