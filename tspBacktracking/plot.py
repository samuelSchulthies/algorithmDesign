import matplotlib.pyplot as plt
import math as math

x = [5,10,15,20,25,30,35,40,45,50]
y = [.0,.0002,.0004,.0012,.0023,.0028,.0080,.0032,.0041,.0032]

theoretical = []
#time complexity is nlogn, take x and plug in for n
K = 0

for single in x:
    theoretical.append(single ** 3)
kk=[] #constant for each data point
for i,value in enumerate(theoretical):
    kk.append(y[i]/value)
    print(f" y/x {kk[i]}")


K = sum(kk)/len(kk) #average of constant of proportionality
scale_theoretical=[]
print(K)

for i,value in enumerate(theoretical):
    scale_theoretical.append(value*K)
    print(scale_theoretical[i])


plt.plot(x,y, label = "Actual")

plt.plot(x,scale_theoretical,label = "Theoretical O(n^3)", color = 'red', linestyle = '--')

plt.legend()
plt.xlabel('Size of N', fontsize=18)
plt.ylabel('Time', fontsize=18)



plt.savefig('baseline_plot.png')



plt.show()