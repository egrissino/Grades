## Evan Grissino
## 10/25/15
## Grades Tools

import os

##=================================================================
##                       main methods
##=================================================================

def main():
    
    print("\n=======  Main Menu  ==========\n")
    classes = reader("settings.txt", ", ")
    info = dictRead("info.txt")
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
def changeSetsInfo(classes, info):
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
        
def addclass(newclass, classes):
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
    info = dictRead("info.txt".format(classname))
    
    print("\n\n==== {0}: {1} {2} ====\n".format(info["name"], classname, info["semester"]))
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
        change("{}.settings.txt".format(classname))
    if num == 4:
        infoChange(infoRead(classname))
    if num == 5:
        nextGrade()
    if num == 0:
        return True
    else:
        return False



##===============================================
##                      tools
##===============================================

def reader(filename, delim):
    infile = open(filename, 'r')
    data = [line.rstrip() for line in infile]
    infile.close()
    if len(data) > 0:
        for i in range(len(data)):
            if delim == "\t\t":
                data[i] = data[i].split(delim)
            else:
                data = data[i].split(delim)
        
        return data
    else:
        return data

##===============================================
    
def writer(filename, vals, ):
    outfile = open(filename, 'w')
    if len(vals) == 0:
        outfile.write('')
        outfile.close()
    else:
        for i in range(0, len(vals)-1):
            outfile.write(str(vals[i]) + ", ")
        outfile.write(str(vals[-1]))
        outfile.close()

##===============================================
        
def change(filename):
    
    Dict = dictRead(filename)
    
    print("\n ----- Change -----")
    for key in Dict:
        print("{0}".format(key).rjust(10), "{0}".format(Dict[key]).ljust(20))

    print("\n1 change/add")
    print("2 delete")
    print("3 exit")
    inpt = int(input(":"))

    if inpt == 1:
        key = input("\n\nEnter key to change or enter new to add:").lower()
        value = input("Enter new value:")
        
        if key in Dict:
            Dict[key] = value
        else:
            file = classname + "." + key + '.txt'
            writer(file, [])
            Dict[key] = value

        
    if inpt == 2:
        key = input("Enter key to remove:")
        if key in Dict:
            del Dict[key]

    outfile = open(filename, 'w')
    for key in Dict:
        line = str(key + "\t\t" + Dict[key] + '\n')
        outfile.write(line)
    outfile.close()

    if inpt != 3:
        change(filename)

##===============================================
                      
def dictRead(filename):
    lists = reader(filename,'\t\t')
    dic = {}
    for i in range(len(lists)):
        key = lists[i][0]
        value = lists[i][1]
        dic[key] = value

    return dic

##===============================================
##                      applets
##===============================================
        
def nextGrade():
    sets = dictRead("{}.settings.txt".format(classname))
    files = []
    for item in sets:
        files.append(item)

    print("")

    i = 0
    for i in range(0, len(files)):
        print("{}\n".format(files[i]))

    classGrade = input("Which type of grade?").lower()
    
    final = float(input("\nEnter your desired final grade:"))
    gradeWanted = final
    
    file = '{}.{}.txt'.format(classname, classGrade)
    delim = ', '

    grade = []
    total = []
    
    for key in sets:
        if key.lower() != classGrade:
            grades = average(reader("{}.{}.txt".format(classname, key), delim))
            if grades != 0:
                grade.append(float(grades) * float(sets[key]) * 100)
                total.append(float(sets[key]))
            else:
                final -= float(sets[key])*100
    
    
    

    ptsNeeded = final - sum(grade)
    
    if ptsNeeded > float(sets[classGrade])*100:
        print("Sorry you cant get that grade :( ")
    
    nextGrade = (ptsNeeded/float(sets[classGrade]) * (len(reader("{}.{}.txt".format(classname, classGrade), delim)) + 1)) - sum(reader("{}.{}.txt".format(classname, classGrade), delim))
    print("\nYou need to get at least a {:.3f}% on the next {} to keep your grade above an {}%".format(nextGrade, classGrade, gradeWanted))





##==============================================
##                  Grades
##==============================================

def addgrade():
    sets = dictRead("{}.settings.txt".format(classname))
    files = []
    for item in sets:
        files.append(item)

    print("")

    i = 0
    for i in range(0, len(files)):
        print("{0} for {1}\n".format(i+1, files[i]))

    print("==========\n{} to exit".format(i+2))
    
    print("")
    
    num = int(input(":"))
    
    for i in range(0, len(files)):
        if num-1 == i:
            gradechange("{}.{}.txt".format(classname, files[i]))
    

##=============================================
            
def gradechange(filename):
    oldvals = reader(filename, ", ")
    clas = filename.rstrip('.txt')
    clas = clas.lstrip("{}.".format(classname))
    
    print('')
    print(clas)
    print("\nGrades: ", end="")
    
    for i in range(len(oldvals)):
        print(float(oldvals[i]), end=", ")
        
    print()
    print("1 to add")
    print("2 to remove")
    print("3 to remove all")
    print("4 back\n")
    
    inpt = int(input(":"))
    
    if inpt == 1:
        oldvals.append(input("Enter one new grade:"))
        writer(filename, oldvals)
    if inpt == 2:
        num = float(input("Enter the grade you wish to remove:"))
        for item in oldvals:
            if float(item) == num:
                oldvals.remove(item)
        writer(filename, oldvals)
    if inpt == 3:
        if input("ARE YOU SURE?? THIS WILL DELETE ALL GRADES (y/n):") == 'y':
            writer(filename, [])
    if inpt == 4:
        addgrade()
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
