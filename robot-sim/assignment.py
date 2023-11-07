from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 2.0
#float number, which is a threshold for the control of the orientation

d_th = 0.4
#float number which is a threshold for the control of the linear distance

def drive(speed, seconds):

    """
    function to set the speed of the wheels of the robot, in order to drive it straight;
    arguments: the desired speed (equal for both wheels) and the time for which it has to go before stopping.
    """

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
	
    """
    function to set the wheels' speed in order to turn;
    arguments: the desired speed of the wheel (one going forward and the other one backword, with equal and opposite speed) and the time for which it has to move before stopping.
    """
	
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(list_code):
	
	""" 
	function to find the closest token that has a different code with respect to the list, given as input;
 	argument: list of codes to discard;
	this function is useful in order to find the closest token, discarding the undesired ones, and returns its distance and angle (orientation) with respect to the robot;
	if no token is detected, no distance is returned.
	"""
	
    	dist=100
    	#high number set to the distance: if no token is close enough, i.e. under the threshold of 100, the distance is not recorded
    	for token in R.see():
    		if token.info.code not in list_code:
        		if token.dist < dist:
        	   		dist=token.dist
		    		rot_y=token.rot_y	
	if dist==100:
    		print("Too distant")
		return -1, -1
    	else:
 		return dist, rot_y
 	
def find_new_token(codice):
	"""  
	function to check if a token among the ones in the list "codice" is in the field of view of the robot;
 	in this case, its distance and angle are returned;
  	argument: list of codes to look for.
	"""
    	dist=100
	for token in R.see():
    		if token.info.code in codice:
   	   		if token.dist < dist:
         			dist=token.dist
			    	rot_y=token.rot_y
    	if dist==100:
    		print("Too distant")
		return -1, -1
    	else:
 		return dist, rot_y
 	
def reach_token(codice):
	"""
	function to reach the desired token, which has a code different from the ones in the list "codice", and to grab it once we're close enough to it.
 	argument: list of codes to be discarded.
	"""
	var=1
	while var:
    		dist, rot_y = find_token(codice)  #looking for markers which are not in the list given in input ("codice"). 
    		#To better understand its meaning, go to the definition of the function "find_token"
    		d_th=0.4 #we set a threshold of the minimum distance to grab the token
    		if dist==-1:
        		print("No token in my field of view, I have to turn a little bit")
			turn(+5,0.5)
			#if no markers are detected, the robot must turn in order to find one
    		elif dist<d_th: 
        		print("Token found")
        		R.grab() 
     		   	#if the robot is close to the token, it grabs it
        		print("Taken") 
        		var=0 #at the end of this condition, the program exits the loop, since the robot found the marker
        		list=[]
        		for i in  R.see():
        			list.append(i.centre.polar.length)  #the distances are recorded in the list called "list"
        		
        		minimum=min(list)  #we look for the minimum distance, which is the one of the grabbed token
        		index=list.index(minimum)  #we record the index of the token corresponding to the closest one
        		return R.see()[index].info.code  #we exploit this index to return its code
    		elif -a_th<= rot_y <= a_th: #if the robot is well aligned with the token, and not enough close to it, it goes forward
        		print("Going straight")
        		drive(20, 0.5)
    		elif rot_y < -a_th: #if the robot is not well aligned with the token, it moves on the left or on the right
        		print("Turn left")
        		turn(-2, 0.5)
    		elif rot_y > a_th:
        		print("Turn right")
        		turn(+2,0.5)

def explore():
	"""
	function used to create a list of the codes of all the tokens inside the arena
	"""
	tokens_list=[]  #create the empty list of tokens' codes
	drive(50,3)  #go straight forward in order to be at least inside the "circle" composed by the markers
	token_t0_angles=[]  
	token_t0_codes=[]
	for token in R.see():	#in that configuration, record the angles and codes of the tokens in the robot's field of view
		token_t0_angles.append(token.centre.polar.rot_y)
		token_t0_codes.append(token.info.code)
	ang0=token_t0_angles[0]  #choose the first token in the list, and use only its angle and code as reference
	code0=token_t0_codes[0]
	var=True
	while var:
		turn(+2,0.5) #at this point, the goal is to make a complete circle on itself (of the robot) and record all the markers in the arena, 
		#so we have to start by turning a little, and proceed like this up to when the the 360 deg rotation is approximately completed
		for token in R.see():
			if token.info.code not in tokens_list: 
				tokens_list.append(token.info.code)	#if the token is not yet in the list, append its code to i
		for token in R.see(): #now let's check if the robot made the whole rotation:
			if token.info.code==code0 and ang0-1.5<=token.centre.polar.rot_y<=ang0-0.5:  #if in the robot's field of view is present the token with code taken as reference,
			#check if its angle with respect to the robot is almost equal to the reference one: I chose a range of values right before the exact value of the complete rotation
				var=False #at this point we exit the loop
				return tokens_list #and return the list of the found tokens
	
				
def reach_goal(codice):
	"""
	this function is useful to go towards the goal position, which is represented by the
	position of the token with the chosen code, named "codice". It is okay even if it is a list, 
	because this will be the list of all the moved tokens, which are all in the same spot, the goal one
	"""
	d_th=0.6 #threshold to release the token, in order to avoid to go on and push the tokens already grouped
	var=1
	while var:
    		dist, rot_y = find_new_token(codice)  #go and look for the tokens which are in the position of the list called "codice", in order to go there
    		if dist==-1:
        		print("No token in my field of view, I have to turn a little bit")
			turn(+5,0.5)  
			#if no markers in the location of "codice" list are detected, the robot must turn in order to find at least one
    		elif dist<d_th: 
        		print("Token found")
     		   	# if the robot is close to the token's list "codice", it releases it
        		drive(0,0.1) # the robot has to stop once it reached the goal position, in order to avoid pushing the group
        		R.release()
        		print("Released")
        		var=0 #the program exits the loop
        		return 0
    		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, and not close enough to it, it goes forward
        		print("Going straight")
        		drive(20, 0.5)
    		elif rot_y < -a_th: # if the robot is not well aligned with the token, it moves on the left or on the right
        		print("Turn left")
        		turn(-2, 0.5)
    		elif rot_y > a_th:
        		print("Turn right")
        		turn(+2,0.5)
def main():
        list=[] #create an empty list to store there all the token's distances of the tokens in the robot's field of view
        for i in  R.see():
        	list.append(i.centre.polar.length) # fill the list previously created
	minimum=min(list) #find minimum distance
	ind_min=list.index(minimum) #find the corresponding index of that minimum distance
	discard_list=[] #create a list of token's codes which have to be discarded for any reason:
	#this could be either because that token has to stay where it it, because it is in the goal position
	#or because it has already been moved, so once it is done, it has to stay where it is again
	discard_list.append(R.see()[ind_min].info.code) #pushing the goal position,
	#which is the minimum distance token in the initial field of view of the robot, in the list of tokens to be left where they are
	print(discard_list) #let's check the token's code corresponing to the goal position
	lista=[] #create an empty list, it will be stuffed with all the tokens found during the exploration
	lista=explore()
	var=1
	while var:
		if len(discard_list)==len(lista): #as first thing, at each cycle, we check whether the number 
		#of all the tokens found matches with the number of total tokens in the arena
			var=0 
			print("End of the loop")
			print("End of the program")
			exit() #in this case, the program exits the loop
		codice=reach_token(discard_list) #record the code of the token grabbed with this function
		reach_goal(discard_list) #reach the goal position and release there the grabbed token
		discard_list.append(codice) #push the code of the previously moved token inside the list of 
		#tokens to be discarded
		print(discard_list)		
		print(lista)
	exit()		
		
        
main()

