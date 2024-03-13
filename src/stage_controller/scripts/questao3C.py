#!/usr/bin/env python3

import rospy
from os import system
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import *
import numpy as np
import random
import math

#================================ Definições Globais ===================================

#TARGETs [X,Y]
target_0 = np.array([-4.14, -5.56]) #primeiro ponto intermediário
target_1 = np.array([-2.58, -1.53]) #segundo ponto intermediário
target_2 = np.array([3.30, 6.69]) 	#terceiro ponto intermediário
target_3 = np.array([6.29, 13.19])  #quarto ponto intermediário
target_4 = np.array([9.04, 13.94]) 	#Ponto final 

# Distância mínima para chegar ao alvo
min_distance = 0.5

#================================ Funções ===================================

odometry_msg = Odometry()
velocity = Twist()

def odometry_callback(data):
	global odometry_msg
	odometry_msg = data

#Primeiro movimento do robô em direção ao primeiro ponto intermediário
def move_frente1():
	velocity.linear.x = 1.0
	velocity.angular.z = 0.2
	pub.publish(velocity)

#Segundo movimento do robô em direção ao segundo ponto intermediário
def move_frente2():
	velocity.linear.x = 1.0
	velocity.angular.z = -1.5
	pub.publish(velocity)

#Terceiro movimento do robô em direção ao terceiro ponto intermediário
def move_frente3():
	velocity.linear.x = 0.5
	velocity.angular.z = -1.5
	pub.publish(velocity)

#Quarto movimento do robô em direção ao quarto ponto intermediário
def move_frente4():
	velocity.linear.x = 0.5
	velocity.angular.z = -2.0
	pub.publish(velocity)  

#Quinto movimento do robô em direção ao ponto final
def move_frente5():
	velocity.linear.x = 0.5
	velocity.angular.z = -1.1
	pub.publish(velocity)        

#Faz o robô parar
def para():
	velocity.linear.x = 0.0
	velocity.angular.z = 0.0
	pub.publish(velocity)  

#================================ Função Principal ===================================

if __name__ == "__main__": 
	# Node
	rospy.init_node("controle_stage_node", anonymous=False)  

	# Subscribers
	rospy.Subscriber("/base_pose_ground_truth", Odometry, odometry_callback)

	# Publishers
	pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
	pub_pos = rospy.Publisher("/base_pose_ground_truth", Odometry, queue_size=10)
  
	rate = rospy.Rate(10) #10hz
  
	while not rospy.is_shutdown(): #Executa enquanto o rospy não for encerrado.
      
		move_frente1()
		
		x = odometry_msg.pose.pose.position.x
		y = odometry_msg.pose.pose.position.y
		
		#Distancia do primeiro ponto intermediário
		distance1= math.sqrt((x-target_0[0])**2 + (y-target_0[1])**2)  
		rospy.loginfo("T: (%.2f, %.2f)" % (target_0[0], target_0[1]))
		rospy.loginfo("P: (%.2f, %.2f)" % (x, y)) 
		rospy.loginfo("D: %.2f" % distance1)

		#Distancia do segundo ponto intermediário
		distance2 = math.sqrt((x-target_1[0])**2 + (y-target_1[1])**2)  
		rospy.loginfo("T: (%.2f, %.2f)" % (target_1[0], target_1[1]))
		rospy.loginfo("P: (%.2f, %.2f)" % (x, y)) 
		rospy.loginfo("D: %.2f" % distance2)

		#Distancia do terceiro ponto intermediário
		distance3 = math.sqrt((x-target_2[0])**2 + (y-target_2[1])**2)  
		rospy.loginfo("T: (%.2f, %.2f)" % (target_2[0], target_2[1]))
		rospy.loginfo("P: (%.2f, %.2f)" % (x, y)) 
		rospy.loginfo("D: %.2f" % distance3)

		#Distancia do quarto ponto intermediário
		distance4 = math.sqrt((x-target_3[0])**2 + (y-target_3[1])**2)  
		rospy.loginfo("T: (%.2f, %.2f)" % (target_3[0], target_3[1]))
		rospy.loginfo("P: (%.2f, %.2f)" % (x, y)) 
		rospy.loginfo("D: %.2f" % distance4)

		#Distancia do ponto final
		distance5 = math.sqrt((x-target_4[0])**2 + (y-target_4[1])**2)  
		rospy.loginfo("T: (%.2f, %.2f)" % (target_4[0], target_4[1]))
		rospy.loginfo("P: (%.2f, %.2f)" % (x, y)) 
		rospy.loginfo("D: %.2f" % distance5)

		#Condições para o robô fazer os pequenos trejetos
		if( distance1 < 0.5 ):
			#para()
			move_frente2()
		elif ( distance2 < 0.5):
			#para()
			move_frente3()
		elif ( distance3 < 0.5):	
			#para()
			move_frente4()
		elif ( distance4 < 0.5):
			#para()
			move_frente5()
		elif(distance5 < 0.5):
			para()
	  
		rate.sleep()
