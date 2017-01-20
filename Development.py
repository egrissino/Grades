## Single file grade program
## Evan Grissino
## Monday November 9, 2015

##===========================================
##              Control Flow
##===========================================

def main():
    declare()
    
    print("\n=======  Main Menu  ==========\n")
    for i in range(len(classes)):
        print("{} : for {}\n".format(i+1, classes[i]))
        
    print("\n=================\n")
    print("{} : to change info and settings".format(len(classes)+1))
    
    prog = input("\nPlease choose a class or enter new name to add class:")

    try:
        prog = int(prog)
    except:
        if prog == "goodbye":
            return True
        elif len(prog) > 1:
            addclass(prog, classes)
            return False
        
    for i in range(len(classes)):
        if prog == i+1:
            gradeForClass(classes[i])
            return False

    if prog == len(classes)+1:
        changeSetsInfo(classes, info)
        return False

    else:
        return False

#==================================
def gradeForClass(cn):
    global classname
    classname = cn
    close = False
    while close == False:
        close = options(mainmenu())

#===================================
def changeSetsInfo(classes, info):              ## UNREVISED
    print("\n1 to delete a class\n")
    print("2 to change info")
    choice = input("\n:")
    
    if choice == '1':
        print("\n====================")
        for i in range(len(classes)):
            print("{}\n".format(classes[i]))
        print("====================\n")
        delclass = input("Enter the class you wish to delete:")
        

        if delclass in classes:
            check = input("ARE YOU SURE YOU WANT TO DELETE? (y/n):")
            if check != 'y':
                return
            del classes[classes.index(delclass)]
            sets = dictRead("{}.settings.txt".format(delclass))
            for item in sets:
                os.remove("{}.{}.txt".format(delclass, item))
            
            os.remove("{}.settings.txt".format(delclass))
            os.remove("{}.info.txt".format(delclass))
            
        else:
            print("\nSorry thats not a class your currently taking!")
        
        writer("settings.txt", classes)

    if choice == '2':
        print("LOL too bad you cant.. yet")
    
#===================================
        
def addclass(newclass, classes):                ## UNREVISED
    info = dictRead("info.txt")
    if newclass in classes:
        print("\nYou are already in that class!")
        delete = input("\ndelete class? (y/n):")
        if delete == 'y':
            classes.remove(newclass)
    else:
        classes.append(newclass)
        
        outfile = open("{}.info.txt".format(newclass), 'w')
        infoDict = { 'class' : newclass, 'semester' : info['semester']}
        for key in infoDict:
            line = str(key + "\t\t" + infoDict[key] + '\n')
            outfile.write(line)
        outfile.close()
        writer("{}.settings.txt".format(newclass), [])
        
    writer("settings.txt", classes)
        

##=================================================================
##                       gradeForClass methods
##=================================================================

def mainmenu():
    
    print("\n\n==== {0}: {1} {2} ====\n".format(info["Name"], classname, info["Semester"]))
    print("1 for current grade!\n")
    print("2 for grades!\n")
    print("3 for settings!\n")
    print("4 for class info!\n")
    print("5 for next grade calculator!\n")
    print("0 to go back to go back to classes!\n")
    num = input(":")
    try:
        num = int(num)
    except:
        num = 6
        
    return num

##======================================

def options(num):
    if num == 1:
        grad()
    if num == 2:
        addgrade()
    if num == 3:
        change(weight[classname])
    if num == 4:
        change(info)
    if num == 5:
        nextGrade()
    if num == 0:
        return True
    else:
        return False

##======================================

def change(Dict):
    
    print("\n           ----- Change -----      ")
    
    for key in Dict:
        print("{0}".format(key).rjust(20), "{0}".format(Dict[key]).ljust(20))

    print("\n1 change/add")
    print("2 delete")
    print("3 exit")
    inpt = int(input(":"))

    if inpt == 1:
        key = input("\n\nEnter key to change or enter new to add:").lower()
        value = input("Enter new value:")

        if Dict == info:
            info[key] = value
        else:
            if key in Dict:
                weight[classname][key] = value
            else:
                if key != "":
                    grades[classname][key] = []
                    weight[classname][key] = value
                    
            write(grades, weight)

        
    if inpt == 2:
        key = input("Enter key to remove:")
        if key in Dict:
            del grade[classname][key]
            del weight[classname][key]
            
        write()

    if inpt != 3:
        change(Dict)
        
##===========================================
##              Text-File r/w
##===========================================
    
def read():
    infile = open("data.txt", 'r')
    data = [line.rstrip() for line in infile]
    infile.close()
    classes = []
    dic = {}
    weight = {}
    for i in range(len(data)):
        item = data[i]
        if "<class>" in item:
            try:
                numTypes = int(item[-2:])
            except:
                numTypes = 0

            start = int(i) + 1
            end = start + numTypes * 2 + 1

            for i in range(start, end):
                if i == start:
                    #class
                    Class = data[i]
                    classes.append(Class)
                    dic[Class] = {}
                    weight[Class] = {}
                    
                elif i % 2 == 0:
                    #subject
                    subject = data[i][0:-3]
                    
                    dic[Class][subject] = []
                    weight[Class][subject] = data[i][-2:]

                elif i % 2 == 1:
                    #grades
                    grades = data[i]
                    if len(grades) > 0:
                        grades = data[i].split(", ")
                        grades = [float(i) for i in grades]
                    else:
                        grades = []
                        
                    dic[Class][subject] = grades
                    
        if "<info>" in item:
            info = {}
            start = int(i) + 1
            infoList = data[start:]
            for i in range(len(infoList)):
                if i % 2 == 0:
                    key = infoList[i]
                    value = infoList[i+1]

                    info[key] = value

    return [dic, weight, classes, info]
   
#=======================================

def write():
    data = []
    for clas in grades:
        data.append("<class>{}".format(str(len(grades[clas])).zfill(2)))
        data.append(clas)
        for subject in grades[clas]:
            data.append("{}:{}".format(subject, weight[clas][subject]))
            gradelist = ""
            for grade in grades[clas][subject]:
                gradelist += str(int(grade)) + ", "
            data.append(gradelist.rstrip(", "))
            
    data.append("<info>")
    for key in info:
        data.append(key)
        data.append(info[key])

    outfile = open("data.txt", 'w')
    [outfile.write(line + "\n") for line in data]
    outfile.close()


#=======================================

    
def declare():
    data = read()
    
    global grades
    grades = data[0]
    
    global weight
    weight = data[1]
    
    global classes
    classes = data[2]
    
    global info
    info = data[3]

##==============================================
##                  Grades
##==============================================

def addgrade():
    sets = weight[classname]
    subjects = []
    for item in sets:
        subjects.append(item)

    print("")

    i = 0
    for i in range(0, len(subjects)):
        print("{0} for {1}\n".format(i+1, subjects[i]))

    print("==========\n{} to exit".format(i+2))
    
    print("")
    
    num = int(input(":"))
    
    for i in range(0, len(subjects)):
        if num-1 == i:
            gradechange(subjects[i])
    

##=============================================
            
def gradechange(subject):
    
    classGrades = grades[classname][subject]
    print()
    print(subject)
    print("\nGrades: ", end="")
    
    for i in range(len(classGrades)):
        print(float(classGrades[i]), end=", ")
        
    print()
    print("1 to add")
    print("2 to remove")
    print("3 to remove all")
    print("4 back\n")
    
    inpt = int(input(":"))
    
    if inpt == 1:
        classGrades.append(input("Enter one new grade:"))
    if inpt == 2:
        num = float(input("Enter the grade you wish to remove:"))
        if float(num) in classGrade:
            classGrade.remove(num)
    if inpt == 3:
        if input("ARE YOU SURE?? THIS WILL DELETE ALL GRADES (y/n):") == 'y':
            writer(filename, [])
    if inpt == 4:
        addgrade()
        
    write(grades weight, info)
    else:
        gradechange(filename)
    
##==============================================

def average(data):
    data = [float(item) for item in data]
    if len(data) > 0:
        s = sum(data)
        l = len(data)
        avg = (s/l)/100
    else:
        avg = 0
    return avg

##==============================================

def grad():
    settings = dictRead("{}.settings.txt".format(classname))
    delim = ", "
    grade = []
    total = []
    for item in settings:
        if float(average(reader("{}.{}.txt".format(classname, item), delim))) > 0:
            grade.append(float(average(reader("{}.{}.txt".format(classname, item), delim))) * float(settings[item]))
            total.append(float(settings[item]))

    if sum(total) != 0:
        grade = sum(grade)/sum(total) * 100
    else:
        grade = 0
    
    print("\nYour current grade for {} is {:.3f}%\n\n".format(dictRead("{}.info.txt".format(classname))["class"], grade))

##==============================================
    

close = False
while close == False:
    close = main()


        
