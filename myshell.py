#Sean Hammond
#17374356
import cmd 							#import all relevant modules.
import os
import sys
import subprocess
import getpass
import threading
import socket
from multiprocessing import Process
lock=threading.Lock()

class myShell(cmd.Cmd):

	USER= getpass.getuser()			#setting the class variables for details of User, Host and path.
	HOST= socket.gethostname()
	PWD= os.getcwd()
	path= os.getcwd()

	prompt= (USER + " in " + HOST + " at " + PWD + " --> ")	#setting the cmd module's prompt.




	def do_cd(self,args):
		if args:
			if args[-1].strip()=="&":									#checking for & to run command to background.
				p= Process(target=self.do_cd,args=(args[:-1].strip(),))
				p.start()
			else:
				try:
					if len(args)==0:
						print("current directory: "+ os.getcwd())		#if no argument is given, print current path and directory.
					else:
						os.chdir(args)
						self.PWD= os.getcwd()
						self.prompt= (self.USER + " in " + self.HOST + " at " + self.PWD + " --> ")	#if argument is given, and arg is a valid directroy, change to that directory and change prompt to reflect change. 
				except Exception as e:
					print("directory not found: "+ args)				#if directory is invalid, report error.
		else:
			print("current directory: "+ os.getcwd())				#if no argument is given, print current path and directory.



	def do_dir(self, args):
		files=[]
		if "&" in args:													#checks for & to run in background.
			p= Process(target=self.do_dir,args=(args[:-1].strip(),))
			p.start()
		else:
			if ">>" in args:
				if not args.split()[:-2]:								#if >> is used and there are no arguments used for dir, append contents of current directory to given file.
					with open (args.split()[-1],"a") as write:
						for i in os.listdir(self.PWD):
							write.write(i+"\n")
				else:
					with open (args.split()[-1],"a") as write:			#if >> is used and there are arguments given for dir, append contents of specified directory to given file.
						for i in os.listdir(self.PWD+"/"+args.split()[-3]):
							write.write(i+"\n")
			elif ">" in args:
				if not args.split()[:-2]:								#if > is used and there are no arguments used for dir, write contents of current directory to given file.
					with open (args.split()[-1],"w") as write:
						for i in os.listdir(self.PWD):
							write.write(i+"\n")
				else:
					with open (args.split()[-1],"w") as write:			#if > is used and there are arguments given for dir, write contents of specified directory to given file.
						for i in os.listdir(self.PWD+"/"+args.split()[-3]):
							write.write(i+"\n")
			elif args:
				try:								
					for i in os.listdir(self.PWD+"/"+args):				#if no output redirection is used and there are arguments given for dir, print contents of given directory.
						print(i)
				except Exception as e:
					print("Directory not found: "+ args)
			else:
				for i in os.listdir(self.PWD):							#if no output redirection is used and there are no arguments given for dir, print contents of current directory.
						print(i)




		




	def default(self, args):
		if "&" in args:
			p= Process(target=self.default,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			if ">>" in args:
				with open (args.split()[-1],"a") as write:				#if >> is used, append the output of the program to given file.
					subprocess.call(args.split()[:-2], stdout=write)
			elif ">" in args:
				with open (args.split()[-1],"w") as write:				#if >> is used, write the output of the program to given file.
					subprocess.call(args.split()[:-2], stdout=write)
			else:
				subprocess.call(args.split())				#if no output redirection is used, invoke the program normally.

	def do_clr(self, args):
		if "&" in args:
			p= Process(target=self.do_clr,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			print("\033[2J\033[H",end="")								#Print an ASCII character that clears the screen, then puts the prompt at the top of the screen.

	def do_quit(self, args):
		if "&" in args:
			p= Process(target=self.do_quit,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			exit()

	def do_environ(self, args):
		if "&" in args:
			p= Process(target=self.do_dir,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			d=os.environ
			if ">>" in args:
				with open (args.split()[-1],"a") as write:				#if >> is used, append the environment variables to given file.
					for k, v in d.items():
						write.write(k + " : " + v+"\n")

			elif ">" in args:
				with open (args.split()[-1],"w") as write:				#if >> is used, write the environment variables to given file.
					for k, v in d.items():
						write.write(k + " : " + v+"\n")
			elif args:
				print("Error: improper invocation of environ.")			#if arguments are given, report an error.

			else:
				for k, v in d.items():
					print(k + " : " + v)								#otherwise, print the environment variables.



	def emptyline(self):
		pass



	def do_help(self,args):
		if "&" in args:
			p= Process(target=self.do_help,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			if ">>" in args:
				with open (args.split()[-1],"a") as write:				#if >> is used, append the help contents to given file.
					with open ("readme","r") as lines:
						for line in lines:
							write.write(line)

			elif ">" in args:
				with open (args.split()[-1],"w") as write:				#if > is used, write the help contents to given file.
					with open ("readme","r") as lines:
						for line in lines:
							write.write(line)
			else:
				with open ("readme","r") as lines:						#otherwise, print 20 lines of help, then wait for an input before printing the next 20 lines.
					count=0
					lines=lines.readlines()
					for line in lines:
						print(line)
						count+=1
						if count==20:
							input("Press ENTER to see more.")
							count=0
					



	def do_echo(self, args):
		if "&" in args:
			p= Process(target=self.do_echo,args=(args[:-1].strip(),))	#if & is present, run the program in the background as a subprocess.
			p.start()
		else:
			if ">>" in args:
				with open (args.split()[-1],"a") as write:
					write.write(" ".join(args.split()[:-2]))				#if >> is used, append the echo contents to given file.

			elif ">" in args:
				with open (args.split()[-1],"w") as write:
					write.write(" ".join(args.split()[:-2]))				#if > is used, write the echo contents to given file.
			else:
				print(" ".join(args.split()))								#otherwise, split the arguments then join them on single white spaces and print them.


	def do_pause(self, args):
		lock.acquire()
		input("MyShell has been paused. Press ENTER to continue.")			#acquire the lock to prevent other processes from running, wait for an input, then release the lock.
		lock.release()


	def do_EOF(self,args):
		return True


if __name__ == '__main__':
	if len(sys.argv) > 1:													#if there are command line arguments given when the shell is launched, interpret the arguments as a batchfile and run commands from the given file.
		myShell.use_rawinput= False
		with open (sys.argv[1], "r") as batch:
			myShell(stdin = batch).cmdloop()
	else:
		myShell().cmdloop()													#CMD loop, checks for inputs and recurs the myShell class.
