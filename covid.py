from tkinter import *
import tkinter.font as tkFont
from selenium import webdriver 
from time import sleep ,time
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import numpy as np

CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
#driver = webdriver.Chrome() // To open chrome
name=[]

def graph(need,l1,l2):
	print("Results successfully recorded\n")
	print("Plotting on Graph\n")
	x = np.arange(len(l1))  # the label locations
	width = 0.35  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width/2, l2 , width)
	ax.set_ylabel('Number of cases')
	ax.set_title('Covid-19 Cases in Andhra Pradesh\n'+str(need))
	ax.set_xticks(x)
	ax.set_xticklabels(l1)
	plt.xlabel('District Names')
	plt.xticks(rotation = 90)
	for rect in rects1:
		height = rect.get_height()
		ax.annotate('{}'.format(height),xy=(rect.get_x() + rect.get_width() / 2, height),xytext=(0, 3),
textcoords="offset points",ha='center', va='bottom')

	fig.tight_layout()
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	plt.show()
def ok():
	need = var.get()
	name.append(need)
	if need == "Confirmed Cases":
		driver.find_element_by_css_selector('div.clickable:nth-child(2)').click()
	elif need == "Active Cases":
		driver.find_element_by_css_selector('div.clickable:nth-child(3)').click()
	elif need == "Recovered Cases":
		driver.find_element_by_css_selector('div.clickable:nth-child(4)').click()
	elif need == "Deceased Cases":
		driver.find_element_by_css_selector('div.clickable:nth-child(5)').click()

def result():
	l=[]
	l1=[]
	sleep(3)
	content1 = driver.find_element_by_css_selector('button.button')
	if content1.text == 'View all':
		content1.click()
	print("Fetching the",name[-1]," from web\nPlease Wait......\n")
	for i in range(1,15):
		sleep(1)
		content2 = driver.find_element_by_css_selector('div.district:nth-child('+str(i)+') > h2:nth-child(1)')
		sleep(1)
		content3 = driver.find_element_by_css_selector('div.district:nth-child('+str(i)+') > h5:nth-child(2)')
		text = content2.text
		text1 = content3.text
		l.append(int(text))
		l1.append(text1)
	
	sleep(3)
	graph(name[-1],l1,l)

master = Tk(className="Covid 19 Live Updates")

master.geometry('500x300')
master.configure(bg='green') 

fontStyle = tkFont.Font(family="Lucida Grande", size=20)


l = Label(master,text = "Covid-19 Live Updates AP ",bg='green',fg='red',bd=5,font = fontStyle)
l.pack()
text=Text(master,bg='green',fg='yellow')
text.pack(padx=0, pady=0)
print("connecting to web\n")
driver.get('https://www.covid19india.org/state/AP')

sleep(5)
text.delete("1.0","end")
text.insert(INSERT,"\t\tConnected, Now you can proceed\n")



var = StringVar(master)
var.set("Select option") # initial value

option = OptionMenu(master, var, "Confirmed Cases", "Active Cases", "Recovered Cases", "Deceased Cases")
option.config(bg='red',fg='green')
option.place(relx=0.5, rely=0.37, anchor=CENTER)

button = Button(master, text="Get Results", command=lambda:[ok(),result()])
button.configure(bg='yellow',fg='red',bd=5)
button.place(relx=0.5, rely=0.5, anchor=CENTER)

button = Button(master, text="Quit", command=master.destroy)
button.configure(bg='violet',fg='red',bd=5)
button.place(relx=0.5, rely=0.64, anchor=CENTER)

mainloop()


