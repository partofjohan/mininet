# -*- coding: utf-8 -*-
import subprocess
import re
import math
c=1
avr_delay=0
avr_bitrate=0	#Valor medio de bitrate
array_bitrate=[]
de_bitrate=0	#Valor de desviación estándar
bitrate_list=[]

for i in range (3):
	print("Valor de c: ",c)
	for j in range (32):
		subprocess.call("./ITGSend -T UDP -a 10.0.0.18 -k {}  -l tx.log -x rx.log".format(10000*c),shell=True)
		subprocess.call("./ITGDec rx.log -v > rx.txt",shell=True)	#Se genera un archivo .txt
		print(j)
		f=open("rx.txt","r")
		lines=f.readlines()
		f.close()
		bitrate=re.findall("\d+.\d+",lines[15])	#Se extrae el valor de bitrate
		bitrate_float=float(bitrate[0])	#Se convierte a float el valor de la lista
		array_bitrate.append(bitrate_float)	#Se guarda el valor en un arreglo
	avr_bitrate=sum(array_bitrate)/32	#Se calcula el valor medio
	for k in range (0,31):	#Se cacula la desviación estándar
		de_bitrate=de_bitrate+(array_bitrate[k]-avr_bitrate)**2
	de_bitrate=math.sqrt(de_bitrate)/32
	c=c*10
	bitrate_list.append(de_bitrate)
print("Vector de bitrate: ",bitrate_list)
	
	
