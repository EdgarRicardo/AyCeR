# import all the required modules
import json
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from socketsClass import SocketsMultibroadcast

# Interfaz del chat
class GUI:
	def on_closing(self):
		if messagebox.askokcancel("No te vayas chavo :(", "Seguro quieres salirte del chat?"):
			self.msg="El usuario "+self.name+" se fue :("
			snd= threading.Thread(target = self.sendMessage)
			snd.start()
			snd= threading.Thread(target = self.sendMessage, args=(0,2,))
			snd.start()
			self.Window.destroy()
			s.closeSocketEscritura()
			s.closeSocketLectura()

	# constructor method
	def __init__(self):
		
		#Messages
		self.msg = ""
		# chat window which is currently hidden
		self.Window = Tk()
		self.Window.withdraw()
		self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
		
		# login window
		self.login = Toplevel()
		# set the title
		self.login.title("Login")
		self.login.resizable(width = False,
							height = False)
		self.login.configure(width = 400,
							height = 300)
		# create a Label
		self.pls = Label(self.login,
					text = "Escribe tu nombre de usuario",
					justify = CENTER,
					font = "Helvetica 14 bold")
		
		self.pls.place(relheight = 0.15,
					relx = 0.2,
					rely = 0.07)
		# create a Label
		self.labelName = Label(self.login,
							text = "Nickname: ",
							font = "Helvetica 12")
		
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.25)
		
		# create a entry box for
		# tyoing the message
		self.entryName = Entry(self.login,
							font = "Helvetica 14")
		
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.3)
		
		# set the focus of the curser
		self.entryName.focus()
		
		# create a Continue Button
		# along with action
		self.go = Button(self.login,
						text = "Entrar",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
		
		self.go.place(relx = 0.4,
					rely = 0.6)
		self.Window.mainloop()

	def goAhead(self, name):
		self.login.destroy()
		self.layout(name)

		self.msg=self.name
		snd= threading.Thread(target = self.sendMessage, args=(0,1,))
		snd.start()

		self.msg="El usuario "+self.name+" entró al chat :)"
		snd= threading.Thread(target = self.sendMessage)
		snd.start()
		# the thread to receive messages
		rcv = threading.Thread(target=self.receive)
		rcv.start()

	# The main layout of the chat
	def layout(self,name):
		
		self.name = name
		# to show chat window
		self.Window.deiconify()
		self.Window.title("CHATROOM")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 15,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.74,
							relheight = 0.06,
							rely = 0.008,
							relx = 0.011)
		
		self.entryMsg.focus()
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendButton(self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
		
		self.textCons.config(cursor = "arrow")
		
		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)
		
		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight = 1,
						relx = 0.974)
		
		scrollbar.config(command = self.textCons.yview)
		
		self.textCons.config(state = DISABLED)

	# function to basically start the thread for sending messages
	def sendButton(self, msg):
		self.textCons.config(state = DISABLED)
		self.msg=self.name+": "+msg
		self.entryMsg.delete(0, END)
		snd= threading.Thread(target = self.sendMessage, args = (1,0,) )
		snd.start()

	# function to receive messages
	def receive(self):
		while True:
			try:
				data, address = s.sockLectura.recvfrom(1024)
				message = json.loads(data.decode('utf-8'))
				# if the messages from the server is NAME send the client's name
				if "login" not in message:
					# insert messages to text box
					self.textCons.config(state = NORMAL)
					self.textCons.insert(END,
										message["msg"]+"\n\n")
					
					self.textCons.config(state = DISABLED)
					self.textCons.see(END)
			except Exception as e:
				print("Error!")
				print(e)
				s.closeSocketLectura()
				print("Socket de Lectura Cerrado")
				break
		
	# function to send messages
	def sendMessage(self, flag=False, login=0):
		if flag:
			self.textCons.config(state=DISABLED)
		while True:
			try:
				data = {}
				data["msg"] = self.msg
				if login == 1:
					data["login"] = True
				elif login == 2:
					data["login"] = False
				toSend = json.dumps(data) 
				sent = s.sockEscritura.sendto(toSend.encode('utf-8'), (s.IP_A, s.PORT))
				break
			except Exception as e:
				print("Error!")
				print(e)
				s.closeSocketEscritura()
				print("Socket de Escritura Cerrado")
				break
#Crear sockets
s = SocketsMultibroadcast()
# Crear interfaz
g = GUI()
