#used to manage files
import os

path_dictionnary= "gcode_dictionnary.txt"#I just changed my_dict into path, this may cause some errors

#this fonction just let's you creat a custum dictionnary
def opendictionnary(p):
    try:
        with open(p, "r") as file:
            global my_dict
            lines = file.readlines()
            my_dict = dict(line.strip().split('=') for line in lines)
        print("G12="+my_dict['G12'])
        print (my_dict)
    except:
        print ("Please enter a valid path")

def translate(gcode_encrypted):
    #opens file 
    with open (gcode_encrypted,"r") as gcode_file_encrypted:
        #lines is a list where every new line is a new element of teh list
        lines = gcode_file_encrypted.readlines()
        #makes a copy of lines
        lines2=lines
        #this loop remove the extra lines if your gcode has some
        opendictionnary(path_dictionnary)
        for i in range (len(lines)):
            lines2[i]=lines[i].replace("\n","")
        
        #makes a temporary variable used to remove elements who have nothing in them
        to_remove=[]
        
        for i in range (len(lines2)):
            #checks if in each line there is a space
            while " "in lines2[i]:
                #if there is a space it removes it
                lines2[i]=lines2[i].replace(" ","")

        for i in range(len(lines2)):
            #if a element of the list lines2 has nothing it is removed
            if lines2[i] == "":
                to_remove.append(i)

        # Remove empty lines in reverse order
        for i in reversed(to_remove):
            lines2.pop(i)

        #lines2 is a list of the gcode initial file where every line is separated
        lenght_dict=len(my_dict)
        for i in range (len(lines2)):
            for k in range (lenght_dict):
                try:
                    #checks if in dictionnary the value k is in lines2
                    if list(my_dict.keys())[k] in lines2[i]:
                        print ("ok")
                        
                        #change the value of lines2 into the translation
                        lines2[i] = lines2[i].replace(list(my_dict.keys())[k], my_dict[list(my_dict.keys())[k]]+" ")
                        
                        k=+1
                        
                        #adds @@@ at the beginning and end of a comment 
                    lines2_striped = lines2[i].removeprefix(";").lstrip()

                    #if a line starts with ; (in gcode this sybole is use to indicate comments)
                    if lines2_striped=="":
                        lines2[i]=""

                    #add a @@@ at the beginning and end of the comment and removes the ;
                    if lines2[i].startswith(";"):
                        lines2[i] = lines2[i].replace(lines2[i],"@@@ "+lines2[i][1:]+" @@@")

                        #if the line before lines2[i] is not a comment add a new line
                        if i > 0 and not lines2[i - 1].strip().startswith("@@@"):
                            lines2[i] = "\n" + lines2[i]

                        #if the line after lines2[i] is not a comment add a new line
                        if i < len(lines2) - 1 and not lines2[i + 1].strip().startswith(";"):
                            lines2[i] = lines2[i] + "\n"
                    
                    #locates comments who have a command before them
                    if ";" in lines2[i]:
                        lines2[i]=lines2[i].replace(";", "   @@@ ")
                        lines2[i]=lines2[i]+" @@@"
                    
                    else:
                        k=+1  
                except:
                    print ("error 5")
        for i in range(len(lines2)):
            #if a element of the list lines2 has nothing it is removed
            if lines2[i] == "":
                to_remove.append(i)

        #separates each element of the list by a nex line
        output="\n".join(lines2)

        #delet all the useless variables
        del(to_remove,lenght_dict,k,lines, lines2, i, gcode_encrypted, gcode_file_encrypted)

        #checks if translated.txt is available if not it tries to use translated(a_number).txt
        a=os.listdir()
        if "translated.txt"in a:
            a.remove("translated" and "translated.txt")
            z=1
            while True:
                if f"translated({z})" not in a:
                    if f"translated({z}).txt" not in a:    
                        name=f"translated({z})"
                        break
                if z>=1000:
                    print ("error : can't find appropriat name for file")
                    quit(code=NameError) 
                else:
                    z=z+1
        else:
            name = "translated"
        
        try:
            with open(name+".txt", 'w') as file:
                file.write(str(output))
                print ("Finished")
        except Exception as e:
            print(f"An error occurred: {e}")

#prints out the help menu
def help():
    print ("""This simple pthon program will help you translate gcode into a more readable forme to finaly understand it !\n
This are a few of the main commands : 
           
- translate : askes the gcode file adresse you want to decode and saves the output as a file name translated.txt           
- syntaxe : shows the syntaxe used in the translated file
- custom + path: give the name (if in the same folder as this program), or the path of a custom gcode syntax (by default marlin is used), if you decide to use this command, make sure to use the correct syntaxe (check the gcodedictionnary.txt file)
- quit : exit this program\n""")
    
print ("\nHi !\n")

help()

#main loop, asks the user commands and calls functions
a=True
while a==True:

    user_input = input("Enter a command : ").lower()

    if user_input=="quit":
        a=False
        print("\nBye bye")
    elif user_input.find("custom")==0:
        tmp1 = user_input.removeprefix("custom")
        path = tmp1.replace(" ","")
        print ('ok')
        print (path)
        opendictionnary(path)

    if user_input=="translate":
        path = input ("Enter the gcode path you want to translate : ")
        if path.lower()=='back':
            exit
        try:
            translate(path)
        except:
            print ("error 0")

    if user_input=="syntaxe":
        print ("""
@@@ comment @@@ : in between to @@@ there is a comment that was in the original file
The special gcode syntaxe is replaced by redable english, ex : G1 F700 -> Linear Move F700
""")

#dictionnary is nammed  : my_dict
#the gcode list is nammed : lines2
