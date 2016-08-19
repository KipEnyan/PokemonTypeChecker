#from sqlalchemy import *
#engine = create_engine('sqlite:///:memory:', echo=True)
#connection = engine.connect()

#import argparse

#parser = argparse.ArgumentParser(description='Pokemon Type Composition Checker')

class Type():
    def __init__(self, strongTo, weakTo, immuneTo, strongFrom, weakFrom, immuneFrom):
        self.strongTo = strongTo
        self.weakTo = weakTo
        self.immuneTo = immuneTo
        self.strongFrom = strongFrom
        self.weakFrom = weakFrom
        self.immuneFrom = immuneFrom

allTypes = ["Bug","Electric","Fire","Grass","Normal","Rock","Dark","Fairy","Flying","Ground","Poison","Steel","Dragon","Fighting","Ghost","Ice","Psychic","Water"]
types = {}
types["Bug"] = Type(["Psychic","Grass","Dark"],["Fighting","Fire","Flying","Ghost","Poison","Steel","Fairy"],[],["Fire","Flying","Rock"],["Fighting","Grass","Ground"],[])
types["Electric"] = Type(["Flying","Water"], ["Dragon","Electric","Grass"],["Ground"],["Ground"],["Electric","Flying","Steel"],[])
types["Fire"] = Type(["Bug","Grass","Ice","Steel"],["Dragon","Fire","Rock","Water"],[],["Ground","Rock","Water"],["Bug","Fairy","Fire","Grass","Ice","Steel"],[])
types["Grass"] = Type(["Ground","Rock","Water"],["Bug","Dragon","Fire","Flying","Grass","Poison","Steel"],[],["Bug","Fire","Flying","Ice","Poison"],["Electric","Grass","Ground","Water"],[])
types["Normal"] = Type([],["Rock","Steel"],["Ghost"],["Fighting"],[],["Ghost"])
types["Rock"] = Type(["Bug","Fire","Flying","Ice"],["Fighting","Ground","Steel"],[],["Fighting","Grass","Ground","Steel","Water"],["Fire","Flying","Normal","Poison"],[])
types["Dark"] = Type(["Ghost","Psychic"],["Dark","Fighting","Fairy"],[],["Bug","Fighting","Fairy"],["Dark","Ghost"],["Psychic"])
types["Fairy"] = Type(["Dark","Dragon","Fighting"],["Fire","Poison","Steel"],[],["Poison","Steel"],["Bug","Dark","Fighting"],["Dragon"])
types["Flying"] = Type(["Bug","Fighting","Grass"],["Electric","Rock","Steel"],[],["Electric","Ice","Rock"],["Bug","Fighting","Grass"],["Ground"])
types["Ground"] = Type(["Electric","Fire","Poison","Rock","Steel"],["Bug","Grass"],["Flying"],["Grass","Ice","Water"],["Poison","Rock"],["Electric"])
types["Poison"] = Type(["Grass","Fairy"],["Ghost","Ground","Poison","Rock"],["Steel"],["Ground","Psychic"],["Bug","Fairy","Fighting","Grass","Poison"],[])
types["Steel"] = Type(["Fairy","Ice","Rock"],["Electric","Fire","Steel","Water"],[],["Fighting","Fire","Ground"],["Bug","Dragon","Fairy","Flying","Grass","Ice","Normal","Psychic","Rock","Steel"],["Poison"])
types["Dragon"] = Type(["Dragon"],["Steel"],["Fairy"],["Dragon","Ice","Fairy"],["Electric","Fire","Grass","Water"],[])
types["Fighting"] = Type(["Dark","Ice","Normal","Rock","Steel"],["Bug","Fairy","Flying","Poison","Psychic"],["Ghost"],["Fairy","Flying","Psychic"],["Bug","Dark","Rock"],[])
types["Ghost"] = Type(["Ghost","Psychic"],["Dark"],["Normal"],["Ghost","Dark"],["Bug","Poison"],["Normal","Fighting"])
types["Ice"] = Type(["Dragon","Flying","Grass","Ground"],["Fire","Ice","Steel","Water"],[],["Fighting","Fire","Rock","Steel"],["Ice"],[])
types["Psychic"] = Type(["Fighting","Poison"],["Psychic","Steel"],["Dark"],["Bug","Dark","Ghost"],["Fighting","Psychic"],[])
types["Water"] = Type(["Fire","Ground","Rock"],["Dragon","Grass","Water"],[],["Electric","Grass"],["Fire","Ice","Steel","Water"],[])

myTypes = ["Grass","Fairy","Fire","Bug","Electric","Psychic"]
testTypes = ["Grass","Psychic","Fairy","Fire","Bug","Electric"]
ericTypes = ["Electric", "Water","Ground","Rock"]
programRunning = True

def calculateStrongTo(myTypes):
    '''Returns a dict with the entered types as values and the types theyre strong against as keys'''
    strongTo = {}
    for aType in myTypes:
        for strongType in types[aType].strongTo:
            if not strongType in strongTo:
                strongTo[strongType] = [aType]
            else:
                strongTo[strongType].append(aType)

    return strongTo

def calculateNotStrongTo(strongTo):
    '''Returns a list of the types that are not in included in strongTo'''
    notStrongTo = []
    for aType in allTypes:
        if aType not in strongTo.keys():
            notStrongTo.append(aType)

    return notStrongTo

def calculateRedundantStrongTo(strongTo):
    '''Returns a dictionary with my redundant types as keys and the count as values'''
    redundantStrongTo = {}
    for strongAgainst, strongFrom in strongTo.items():
        if len(strongFrom) > 1:
            for redundant in strongFrom:
                if redundant in redundantStrongTo:
                    redundantStrongTo[redundant] += 1
                else:
                    redundantStrongTo[redundant] = 1

    return redundantStrongTo

def calculateMostRedundant(redundantStrongTo):
    '''Returns a list of the types with the most redundancies'''
    if(redundantStrongTo):
        maxRedundant = max(redundantStrongTo.values())
    mostRedundant = []

    for key, value in redundantStrongTo.items():
        if value == maxRedundant:
            mostRedundant.append(key)

    return mostRedundant

def calculateTypeLost(mostRedundant, strongTo):
    '''Returns a dict of the types to remove and what coverage will be lost'''
    lostTypes = {}
    for aRedundant in mostRedundant:
        for key, value in strongTo.items():
            if aRedundant in value and len(value) == 1:
                if aRedundant in lostTypes:
                    lostTypes[aRedundant].append(key)
                else:
                    lostTypes[aRedundant] = [key]
        if not aRedundant in lostTypes:
            lostTypes[aRedundant] = []

    return lostTypes

def calculateNotStrongToWeaknesses(notStrongTo):
    '''Takes a list of types youre not strong against and returns a dict of types that are strong against them'''
    notStrongToWeaknesses = {}
    for aType in notStrongTo:
        for strongType in types[aType].strongFrom:
            if strongType in notStrongToWeaknesses:
                notStrongToWeaknesses[strongType].append(aType)
            else:
                notStrongToWeaknesses[strongType] = [aType]

    return notStrongToWeaknesses

def calculateStrongToAdditions(notStrongToWeaknesses):
    '''Takes in a dict of types and their weaknesses and returns a list of the most common weaknesses'''
    maxStrong = 0
    strongToAdditions = []
    for value in notStrongToWeaknesses.values():
        if len(value) > maxStrong:
            maxStrong = len(value)

    for key, value in notStrongToWeaknesses.items():
        if len(value) == maxStrong:
            strongToAdditions.append(key)

    return strongToAdditions

def printStrongTo(strongTo):
    '''Prints a list of the types your team is strong against'''
    print("Your team is strong against ", end="")
    for key in strongTo.keys():
        if len(strongTo.keys()) == 1:
            print(key,end=". ")
        elif not key == list(strongTo)[-1]:
            print(key,end=", ")
        else:
            print("and " + key,end=". ")

    print("(" + str(len(strongTo.keys())) + "/18 types)")

def printNotStrongTo(notStrongTo):
    '''Prints a list of the types your team is not strong against'''
    print("Your team is not strong against ", end="")
    for item in notStrongTo:
        if len(notStrongTo) == 1:
            print(item,end=". ")
        elif not item == notStrongTo[-1]:
            print(item,end=", ")
        else:
            print("or " + item,end=". ")

    print("(" + str(len(notStrongTo)) + "/18 types)")

def printMostRedundant(mostRedundant, redundantStrongTo):
    '''Prints a list of your types with the most redundant type coverage'''
    if len(mostRedundant) > 1:
        print("Your types with the most redundant coverage are",end=" ")
        for item in mostRedundant:
            if not item == mostRedundant[-1]:
                print(item,end=", ")
            else:
                print("and " + item + ". (" + str(redundantStrongTo[item]) + " redundancies.)")
    elif len(mostRedundant) == 1:
        print("Your type with the most redundant coverage is " + str(mostRedundant[0]) + ". (" + str(redundantStrongTo[mostRedundant[0]]) + " redundancies.)")
    else:
        print("You have no type coverage redundancies.")

def printLostTypes(lostTypes):
    '''Prints what coverage would be lost if the most redundant types were removed'''
    minLost = 19
    for item in lostTypes.values():
        if len(item) < minLost:
            minLost = len(item)

    for key, value in lostTypes.items():
        if len(value) == minLost:
            print("If you removed " + key + ", you would lose",end=" ")
            if len(value) == 0:
                print("no type coverage.")
            for item in value:
                if len(value) == 1:
                    print(item + " coverage.")
                elif not item == value[-1]:
                    print(item,end=", ")
                else:
                    print("and " + item,end=" coverage.\n")

def printStrongToAdditions(strongToAdditions, notStrongToWeaknesses):
    for item in strongToAdditions:
        print ("Adding " + item + " would add type coverage against",end=" ")
        for aType in notStrongToWeaknesses[item]:
            if len(notStrongToWeaknesses[item]) == 1:
                print(aType + ".")
            elif not aType == notStrongToWeaknesses[item][-1]:
                print(aType,end=", ")
            else:
                print("and " + aType + ".")

def readInput():
    print("Please enter the type composition of your team, separated by commas.")
    entered = input()
    if entered == "exit":
        return False
    enteredTypes = entered.split(", ")
    for item in enteredTypes:
        if not item in allTypes:
            print("That's not a type of Pokemon. Try again.")
            return True

    return(doCalculations(enteredTypes))

def doCalculations(enteredTypes):
    strongTo = calculateStrongTo(enteredTypes)
    notStrongTo = calculateNotStrongTo(strongTo)
    redundantStrongTo = calculateRedundantStrongTo(strongTo)
    mostRedundant = calculateMostRedundant(redundantStrongTo)
    lostTypes = calculateTypeLost(enteredTypes, strongTo)
    notStrongToWeaknesses = calculateNotStrongToWeaknesses(notStrongTo)
    strongToAdditions = calculateStrongToAdditions(notStrongToWeaknesses)
    
    printStrongTo(strongTo)
    printNotStrongTo(notStrongTo)
    printMostRedundant(mostRedundant, redundantStrongTo)
    printLostTypes(lostTypes)
    printStrongToAdditions(strongToAdditions, notStrongToWeaknesses)
    print()
    return True


print("Welcome to the Pokemon Type Calculator!")
print("Type 'exit' to quit.")
while(readInput()):
    pass

