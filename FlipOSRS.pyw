from tkinter import Frame,Button,Text,Entry,Tk,StringVar,Label,END,Scrollbar
from GrandExchange import GrandExchange
import numpy as np


master = Tk()

sorttoggle = False
lastsort = 0

def showResults(sort=0):
	global sorttoggle, lastsort
	label3['text']='\nResults:\n'
	exchange = GrandExchange.Exchange()
	allitems = exchange.retrieve()
	try:
		var1 = int(boxvar.get())
	except:
		var1 = 1000000000000
	try:
		var2 = float(boxvar2.get())
	except:
		var2 = -1000000000000
	items = []
	for item in allitems:
		if allitems[item]['buy_average'] <= var1 and allitems[item]['sell_average'] > allitems[item]['buy_average'] and allitems[item]['buy_average'] > 0 and boxvar3.get().lower() in allitems[item]['name'].lower():
			if ((allitems[item]['sell_average']-allitems[item]['buy_average'])/allitems[item]['buy_average']*100 if allitems[item]['buy_quantity'] != 0 else 0) > var2:
				items.append([allitems[item][name] for name in allitems[item]])
	for i, row in enumerate(items):
		items[i].append(round(row[7]/row[5],2) if row[5] != 0 else 0)
		items[i].append(row[6]-row[4])
		items[i].append(round(((row[6]-row[4])/row[6])*100,2) if row[6] != 0 else 0)
	if items:
		items = np.array(items, dtype='O')
		if sort:
			if str(type(items[0][sort])) == "<class 'int'>":
				sitems = items[items[:, sort].astype(np.int).argsort()].T
			if str(type(items[0][sort])) == "<class 'float'>":
				sitems = items[items[:, sort].astype(np.float).argsort()].T
			if str(type(items[0][sort])) == "<class 'str'>":
				sitems = items[items[:, sort].argsort()].T
			if str(type(items[0][sort])) == "<class 'bool'>":
				sitems = items[items[:, sort].argsort()].T
			if lastsort:
				if lastsort == sort and sorttoggle == False:
					sitems = np.flip(sitems,axis=1)
					sorttoggle = True
				else:
					sorttoggle = False
			lastsort = sort
		else: sitems = items.T
		txt.delete('1.0', END)
		txt.insert('1.0', '\n'.join(sitems[1].astype(np.str)))
		txt2.delete('1.0', END)
		txt2.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[4]))
		txt3.delete('1.0', END)
		txt3.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[6]))
		txt4.delete('1.0', END)
		txt4.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[-2]))
		txt5.delete('1.0', END)
		txt5.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[3]))
		txt6.delete('1.0', END)
		txt6.insert('1.0', '\n'.join(sitems[-3].astype(np.str)))
		txt7.delete('1.0', END)
		txt7.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[-4]))
		txt8.delete('1.0', END)
		txt8.insert('1.0', '\n'.join(sitems[2].astype(np.str)))
		txt9.delete('1.0', END)
		txt9.insert('1.0', '\n'.join(f"{num:,}" for num in sitems[-1]))
	else:
		label3['text']='\nYour search returned no results!\n'

def OnVsb(*args):
	txt.yview(*args)
	txt2.yview(*args)
	txt3.yview(*args)
	txt4.yview(*args)
	txt5.yview(*args)
	txt6.yview(*args)
	txt7.yview(*args)
	txt8.yview(*args)
	txt9.yview(*args)

def OnMouseWheel(event):
	txt.yview("scroll", -event.delta,'pixels')
	txt2.yview("scroll",-event.delta,'pixels')
	txt3.yview("scroll", -event.delta,'pixels')
	txt4.yview("scroll",-event.delta,'pixels')
	txt5.yview("scroll", -event.delta,'pixels')
	txt6.yview("scroll",-event.delta,'pixels')
	txt7.yview("scroll", -event.delta,'pixels')
	txt8.yview("scroll",-event.delta,'pixels')
	txt9.yview("scroll",-event.delta,'pixels')
	# this prevents default bindings from firing, which
	# would end up scrolling the widget twice
	return "break"

#INPUT MENU
inputmenu = Frame(master)
label = Label(inputmenu, text="Max Item Price")
label2 = Label(inputmenu, text="Minimum Profit per Item (%)")
label12 = Label(inputmenu, text="Item Search")
boxvar = StringVar()
boxvar2 = StringVar()
boxvar3 = StringVar()
box = Entry(inputmenu, textvariable= boxvar)
box2 = Entry(inputmenu, textvariable= boxvar2)
box3 = Entry(inputmenu, textvariable= boxvar3)
btn = Button(inputmenu, text = "Get Results", command=showResults)
label.grid(row=0,column=0)
label2.grid(row=1,column=0)
label12.grid(row=2,column=0)
box.grid(row=0,column=1)
box2.grid(row=1,column=1)
box3.grid(row=2,column=1)
btn.grid(row=0,rowspan=3,column=2,columnspan=6,sticky='NESW')

#TEXT OUTPUT
textoutput = Frame(master)
label4 = Button(textoutput, text="Name", borderwidth=2, relief="groove", width=45, command= lambda: showResults(1))
label5 = Button(textoutput, text="Avg Buy Price (GP)", borderwidth=2, relief="groove", width=17, command= lambda: showResults(4))
label6 = Button(textoutput, text="Avg Sell Price (GP)", borderwidth=2, relief="groove", width=17, command= lambda: showResults(6))
label7 = Button(textoutput, text="Profit per Item (GP)", borderwidth=2, relief="groove", width=18, command= lambda: showResults(-2))
label8 = Button(textoutput, text="Store Price (GP)", borderwidth=2, relief="groove", width=17, command= lambda: showResults(3))
label11 = Button(textoutput, text="Members", borderwidth=2, relief="groove", width=10, command= lambda: showResults(2))
label9 = Button(textoutput, text="Supply/Demand", borderwidth=2, relief="groove", width=17, command= lambda: showResults(-3))
label10 = Button(textoutput, text="Overall Quantity", borderwidth=2, relief="groove", width=17, command= lambda: showResults(-4))
label13 = Button(textoutput, text="Margin (%)", borderwidth=2, relief="groove", width=10, command= lambda: showResults(-1))
scrollb = Scrollbar(textoutput, command=OnVsb)

txt = Text(textoutput, font=('Consolas',12), width=35, yscrollcommand = scrollb.set)
txt2 = Text(textoutput, font=('Consolas',12), width=12, yscrollcommand = scrollb.set)
txt3 = Text(textoutput, font=('Consolas',12), width=12, yscrollcommand = scrollb.set)
txt4 = Text(textoutput, font=('Consolas',12), width=13, yscrollcommand = scrollb.set)
txt5 = Text(textoutput, font=('Consolas',12), width=12, yscrollcommand = scrollb.set)
txt6 = Text(textoutput, font=('Consolas',12), width=12, yscrollcommand = scrollb.set)
txt7 = Text(textoutput, font=('Consolas',12), width=12, yscrollcommand = scrollb.set)
txt8 = Text(textoutput, font=('Consolas',12), width=5, yscrollcommand = scrollb.set)
txt9 = Text(textoutput, font=('Consolas',12), width=5, yscrollcommand = scrollb.set)
txt.bind("<MouseWheel>", OnMouseWheel)
txt2.bind("<MouseWheel>", OnMouseWheel)
txt3.bind("<MouseWheel>", OnMouseWheel)
txt4.bind("<MouseWheel>", OnMouseWheel)
txt5.bind("<MouseWheel>", OnMouseWheel)
txt6.bind("<MouseWheel>", OnMouseWheel)
txt7.bind("<MouseWheel>", OnMouseWheel)
txt8.bind("<MouseWheel>", OnMouseWheel)
txt9.bind("<MouseWheel>", OnMouseWheel)
label4.grid(row=0,column=0)
label5.grid(row=0,column=1)
label6.grid(row=0,column=2)
label7.grid(row=0,column=3)
label8.grid(row=0,column=5)
label9.grid(row=0,column=6)
label10.grid(row=0,column=7)
label11.grid(row=0,column=8)
label13.grid(row=0,column=4)

txt.grid(row=1,column=0,sticky='NESW')
txt2.grid(row=1,column=1,sticky='NESW')
txt3.grid(row=1,column=2,sticky='NESW')
txt4.grid(row=1,column=3,sticky='NESW')
txt5.grid(row=1,column=5,sticky='NESW')
txt6.grid(row=1,column=6,sticky='NESW')
txt7.grid(row=1,column=7,sticky='NESW')
txt8.grid(row=1,column=8,sticky='NESW')
txt9.grid(row=1,column=4,sticky='NESW')


scrollb.grid(row=0, rowspan=2, column=9, sticky='nsew')
textoutput.pack(side='bottom')

label3 = Label(master, text="\nResults:\n")
inputmenu.pack(side='top')
label3.pack(side='bottom')

showResults()
master.winfo_toplevel().title("FlipOSRS")
master.mainloop()
