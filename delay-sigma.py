# -*- coding: utf-8 -*-
import subprocess
import re
import math
c=1
d=250000

avr_delay=0	#Valor medio de delay
avr_bitrate=0	#Valor medio de bitrate
avr_loss=0	#Valor medio de pérdida de paquetes

array_delay=[]
array_bitrate=[]
array_loss=[]

de_delay=0	#Desviación estándar del delay
de_bitrate=0	#Desviación estándar del bitrate
de_loss=0	#Desviación estándar de las pérdidas de paquetes

delay_list=[]
bitrate_list=[]
loss_list=[]

delay_average=[]
bitrate_average=[]
loss_average=[]

for i in range (3):
	print("Valor de c: ",c)
	print("Valor de d: ",d)
	for j in range (32):
		subprocess.call("./ITGSend -T UDP -a 10.0.0.18 -c 218 -C {} -k {}  -l tx.log -x rx.log".format(d,10000*c),shell=True)
		subprocess.call("./ITGDec rx.log -v > rx.txt",shell=True)	#Se genera un archivo .txt
		print(j)
		f=open("rx.txt","r")
		lines=f.readlines()
		f.close()
		
		delay=re.findall("\d+.\d+",lines[11])	#Se extrae el valor del delay
		delay_float=float(delay[0])	#Se convierte a float el valor de la lista
		array_delay.append(delay_float)	#Se guarda el valor en un arreglo
		
		bitrate=re.findall("\d+.\d+",lines[15])	#Se extrae el valor de bitrate
		bitrate_float=float(bitrate[0])	#Se convierte a float el valor de la lista
		array_bitrate.append(bitrate_float)	#Se guarda el valor en un arreglo
		
		loss=re.findall("\d+.\d+",lines[17])
		loss_float=float(loss[0])
		array_loss.append(loss_float)
		
	avr_delay=sum(array_delay)/32		#Se calcula el valor medio de delay
	avr_bitrate=sum(array_bitrate)/32	#Se calcula el valor medio de bitrate
	avr_loss=sum(array_loss)/32		#Se calcula el valor medio de pérdida de paquetes
	
	delay_average.append(avr_delay)
	bitrate_average.append(avr_bitrate)
	loss_average.append(avr_loss)	

	for k in range (32):	#Se cacula la desviación estándar
		de_delay=de_delay+(array_delay[k]-avr_delay)**2
		de_bitrate=de_bitrate+(array_bitrate[k]-avr_bitrate)**2
		de_loss=de_loss+(array_loss[k]-avr_loss)**2
	de_delay=math.sqrt(de_delay)/32
	de_bitrate=math.sqrt(de_bitrate)/32
	de_loss=math.sqrt(de_loss)/32
	c=c*10
	d=d+50000

	delay_list.append(de_delay)
	bitrate_list.append(de_bitrate)
	loss_list.append(de_loss)	

file=open("bitrate.dat","w+")
file.write("# X Y ")
file.write("{} {}".format(10,bitrate_list[0]))
file.write("{} {}".format(100,bitrate_list[1]))
file.write("{} {}".format(1000,bitrate_list[2]))
file.close()

file=open("delay.dat","w+")
file.write("# X Y")
file.write("{} {}".format(10,delay_list[0]))
file.write("{} {}".format(100,delay_list[1]))
file.write("{} {}".format(1000,delay_list[2]))
file.close()

file=open("loss.dat","w+")
file.write("# X Y")
file.write("{} {}".format(10,loss_list[0]))
file.write("{} {}".format(100,loss_list[1]))
file.write("{} {}".format(1000,loss_list[2]))
file.close()
