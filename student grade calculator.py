subject = ["math","science","computer","english","sst"]
for subject in subject:
	marks=int(input(f"enter the  {subject} marks: "))
if marks > 0 or marks < 100:
    print("Error: Marks must be between 0 and 100")
if 91 <= marks <= 100:
	print("grade a1")
elif 81 <= marks <=90 :
    print("grade a2")
elif 71 <= marks <=80 :
	print("grade b1")
elif 61 <= marks <=70 :
    print("grade b2")
elif 51 <= marks <=60 :
    print("grade c1")
elif 41 <= marks <=50 :
    print("grade c2")
elif 33 <= marks <=40 :
    print("grade d")
else:
 	print("fail")
 	
 		
 	