import os
import sys
import subprocess
import shlex

#Global variables
PathToControlFile="/tmp/RadioControl"
MPlayerCommand = "mplayer -input file=/tmp/RadioControl -slave -playlist "

#Playslists' global variables
Playlists=[]        
NumberOfPlaylists = 0 
RadioNames=[]      
PlaylistTarget=0 

RadioName1="Radio ShoutCast"
RadioName2="Radio Backstage (www.radiobackstage.com)"

#Function: init of playlists' list
#Params: none
#Return: none
def InitPlaylistList():
	global Playlists
	global RadioNames
	global NumberOfPlaylists

	#playlist 1
	Playlists.append("http://yp.shoutcast.com/sbin/tunein-station.pls?id=1057392")
	RadioNames.append("Radio Shoutcast")

	#playlist 2
	Playlists.append("http://panel3.serverhostingcenter.com:2199/tunein/radiobackstage1.pls")
	RadioNames.append("Radio Backstage")

	#playlist 3
	Playlists.append("http://yp.shoutcast.com/sbin/tunein-station.pls?id=1425714")
	RadioNames.append("Techno")

	NumberOfPlaylists=3
	return

#Function: play choosen playlst / target playlist
#Params: none
#Return: none
def PlayPlaylist(TgtPlaylist):
	global Playlists
	global MPlayerCommand

	os.system("pkill -f mplayer")
	PlaylistCmd = MPlayerCommand + Playlists[TgtPlaylist]
	
	#starts mplayer process and e direct its stdout to /dev/null (so nothing of mplayer will be displayed, except errors)
	FNULL = open(os.devnull,'w')
	args = shlex.split(PlaylistCmd)
	InterfaceMPlayer = subprocess.Popen(args, shell=False, stdin=subprocess.PIPE, stdout=FNULL, stderr=subprocess.STDOUT)

	#volume set to 50%
	os.system('echo "volume 50" >'+PathToControlFile)

	return


#Function: create control file of mplayer (fifo file)
#Params: none
#Return: none
def CreateControlFile():
	if (os.path.exists(PathToControlFile)):
		return

	try:
		os.mkfifo(PathToControlFile)
	except:
		print "[ERROR] Failed to create control file. Please, check path to this file."
		exit(1)

#Function: show menu
#Params: none
#Return:  option
def ShowMenu():
	global RadioNames
	global PlaylitsEscolhida

	print "-----------------------"
	print "    Option menu        "
	print "-----------------------"
	print "Current on-line radio: "+RadioNames[PlaylistTarget]
	print " "
	print "<p> Play/pause"
	print "<s> Exit"
	print "<+> Volume up"
	print "<-> Volume down"
	print "<d> Next radio"
	print "<a> Prior radio"
	print " "
	option = raw_input("Option> ")

	return option


#------------------
#Main program
#------------------

InitPlaylistList()
CreateControlFile()

PlayPlaylist(PlaylistTarget)

while True:
	try:
		os.system("clear")
		KeyPressed = ShowMenu()

		if (KeyPressed == "p"):
			print "[ACTION] Play/Pause"
			os.system('echo "pause" > '+PathToControlFile)

		if (KeyPressed == "s"):
			print "[ACTION] Exit"
			os.system('echo "quit 0" > '+PathToControlFile)
			os.system("pkill -f mplayer")
			exit(1)

		if (KeyPressed == "+"):
			print "[ACTION] Volume up"
			os.system('echo "volume +10" > '+PathToControlFile)

		if (KeyPressed == "-"):
			print "[ACTION] Volume down"
			os.system('echo "volume -10" > '+PathToControlFile)

		if (KeyPressed == "d"):
			print "[ACTION] Next radio"
			PlaylistTarget = PlaylistTarget + 1
			if (PlaylistTarget == NumberOfPlaylists):
				PlaylistTarget = 0
			PlayPlaylist(PlaylistTarget)

		if (KeyPressed == "a"):
			print "[ACTION] Prior radio"
			PlaylistTarget = PlaylistTarget - 1
			if (PlaylistTarget < 0):
				PlaylistTarget = NumberOfPlaylists-1
			PlayPlaylist(PlaylistTarget)


	except (KeyboardInterrupt):
		print "This application is being terminated. Good bye."
		exit(1)