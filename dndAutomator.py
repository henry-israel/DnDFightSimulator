import random
import numpy as np
import collections

class basicFunctionality:
    #Stuff for every ddnd
    def __init__(self, stats=[0,0,0,0,0,0], verbosity=False):
        #Stats = character stats
        if not isinstance(verbosity, bool):
            raise TypeError("Verbosity must be a bool!")
        for i in stats:
            self.checkValues(i)

        self.verbose=verbosity
        self.statnames=["Str", "Dex", "Con", "Int", "Wis", "Cha"] #DnD stats
        self.statvalues = stats

    def checkValues(self, variable):
        if not isinstance(variable, int):
            raise TypeError("Entered values of stats, ac, hp, damage + prof can only be of type int")
        if variable<0:
            raise ValueError("Entered values of stats, ac, hp, damage + profmust be >= 0")

    def setVerbose(self, verbosevalue):
        if not isinstance(verbosevalue, bool):
            raise TypeError("Verbosity can only be true/false")
        self.verbose=verbosevalue
        return 1

    def rollDice(self, dicenum):
        #Rolls a dice
        self.checkValues(dicenum)
        return random.randint(1, dicenum)


    #Stat values
    def displayStats(self):
        #Return character stat values + stat names
        return dict(zip(self.statnames, self.statvalues))

    def getStat(self, statname):
        if statname not in self.statnames:
            raise NameError(f"Could find {statname} please specify one from {self.statnames}")
        statindex=list(self.displayStats().keys()).index(statname)
        return self.statvalues[statindex], statindex

    def statModifiers(self):
        #Get array of stat modifiers
        return [int(np.floor((x-10)/2)) for x in self.statvalues]

    def displayStatModifiers(self):
        #Return stat modifiers + stat names
        return dict(zip(self.statnames, self.statModifiers()))

    def displayFullStats(self):
        #Return Statnames : Stat values, Modifiers
        return dict(zip(self.statnames, zip(self.statvalues, self.statModifiers())))

    #Individual Stats
    def Str(self):
        strength,_ = self.getStat('Str')
        return strength
    def Dex(self):
        dexterity,_=self.getStat('Dex')
        return dexterity
    def Con(self):
        constitution = self.getStat('Con')
        return constitution
    def Int(self):
        intelligence = self.getStat('Int')
        return intelligence
    def Wis(self):
        wisdom = self.getStat('Wis')
        return wisdom
    def Cha(self):
        charisma = self.getStat('Cha')
        return charisma

    def changeStat(self, statname, statmod):
        if statname not in self.statnames:
            raise NameError(f"Could find {statname} please specify one from {self.statnames}")

        if self.verbose==True:
            print(f"Modifying {statname} by {statmod}")
        _, statindex=self.getStat(statname)
        self.statvalues[statindex]=max(0, statmod+self.statvalues[statindex])

        if self.verbose==True:
            print(f"{statname} is now {self.statvalues[statindex]}")
        return 1

    def statsRoll(self, statname):
        #Rolls 1 d20 and adds stat modifier
        if self.verbose==True:
            print(f"Attempting to roll {statname}")

        if statname not in self.statnames:
            raise NameError(f"Could find {statname} please specify one from {self.statnames}")

        modifier=self.displayStatModifiers()[statname]
        diceroll = self.rollDice(20)
        totalroll = modifier + diceroll
        if self.verbose==True:
            print(f"Rolled {diceroll} + {modifier}={totalroll}")
            if diceroll==20:
                print("CRIT!")
            if diceroll==1:
                print("CRIT FAIL!")
        return diceroll, modifier, totalroll


class weaponsAndSpells(basicFunctionality):
    def __init__(self, stats=[0,0,0,0,0,0], isproficient=False, proficiency=0, verbosity=False):
        super().__init__(stats, verbosity)
        #Equpped weapons

        self.weaponstat='Str'
        self.tohit=0
        self.weapondice=1
        self.weapondamage=4
        self.damagemodifier=0
        self.damagetype="Bludgeoning"

        self.ranged=False
        self.equiped=False

        if not isinstance(isproficient, bool):
            raise TypeError("Is proficient can only be type:Bool")

        self.isprof=isproficient
        self.profval=proficiency

    def equipWeapon(self, weaponstat, tohit, weapondice, weapondamage,
                    damagemodifier=0, damagetype="Piercing", ranged=False):

        self.checkValues(tohit)
        self.checkValues(weapondice)
        self.checkValues(weapondamage)
        self.checkValues(damagemodifier)
        if weaponstat not in self.statnames:
            raise NameError(f"Could find {weaponstat} please specify one from {self.statnames}")

        self.weaponstat=weaponstat
        self.tohit=tohit
        self.weapondice=weapondice
        self.weapondamage=weapondamage
        self.damagemodifier=damagemodifier
        self.damagetype=damagetype

        if self.verbose:
            print(f"Equipped new weapon, uses {self.weaponstat},",
                  f" rolls + {self.damagemodifier} to hit.",
                  f" Does {self.weapondice}d{self.weapondamage}+{self.damagemodifier}",
                  f"{self.damagetype} damage")
        self.ranged=ranged
        self.equiped=True
        return 1



    def damageRoll(self):
        #rolls damage
        #Total dice : Number of dice to roll
        #weapon damage : Damage weapon does
        #damage modifier : Extra damage
        self.checkValues(self.weapondice)
        self.checkValues(self.weapondamage)
        self.checkValues(self.damagemodifier)

        if self.verbose==True:
            print(f"Rolling {self.weapondice}d{self.weapondamage}(s)+{self.damagemodifier}")
        dicerolls = []

        i=0
        while i < self.weapondice:
            dicerolls.append(self.rollDice(self.weapondamage))
            i+=1

        rolleddamage=sum(dicerolls)
        totaldamage=rolleddamage+self.damagemodifier

        if self.verbose==True:
            print(f"Rolled {dicerolls} +{self.damagemodifier} for total of {totaldamage}")

        return totaldamage



    def rollToHit(self, enemyac):
        #rolls to hit and does damage
        #EnemyAC = enemy ac
        #Weapon stat : what stat to use the weapon
        #Tohit : How much added to hit
        #total dice: Number of damage die
        #weapon damage : weapon damage
        #damage modifier : extra damage
        self.checkValues(enemyac)
        self.checkValues(self.tohit)
        if self.verbose:
            print(f"Rolling to hit against {enemyac}")

        statroll, mod, totalroll = self.statsRoll(self.weaponstat)


        hitroll = totalroll+self.tohit

        if self.verbose:
            print(f"Added +{self.tohit} to roll")

        if self.isprof:
            hitroll+=self.profval
            if self.verbose:
                print(f"Proficient with this weapon, adding {self.profval} to hit")
        if hitroll >= enemyac:

            if self.verbose:
                print(f"Roll of {hitroll} hits!")
            damage = self.damageRoll()
            if statroll==20:
                critdamage=self.rollDice(self.weapondamage)
                if self.verbose:
                    print(f"YOU CRITICALLY HIT! Doing an extra {critdamage} damage")
                damage+=critdamage
        else:
            damage = 0
            if self.verbose:
                print(f"Roll of {hitroll} misses! Sorry!")

        return hitroll, damage


class dndCharacter(weaponsAndSpells):
    def __init__(self, hitdie=[False, 0, 0, 0], armorclass=1, isproficient=False,
                 proficiency=2, stats=[0, 0, 0, 0, 0, 0], basehp=0, position=(0,0), team='a',
                 verbosity=False):
        #basehp = hp with no hitdie
        #hitdie = [usehit die, number of hit die, value of hit die, modifier]
        #armorclass = AC
        #profciency = proficiency
        #stats = stats
        #Position = Location on map
        #Team = Label on map
        #verbosity : Enables print statements in class

        #Double check we've not done something dumb!
        weaponsAndSpells.__init__(self, stats, isproficient, proficiency, verbosity)


        self.checkValues(basehp)
        for i in range(1,len(hitdie)):
            self.checkValues(i)
        if not isinstance(hitdie[0], bool):
            raise TypeError("Use hit die can only be true or false!")

        if len(position)!=2:
            raise ValueError("Position should be tuple of 2 coordinates")
        if not isinstance(position[0], int) or not (position[1], int):
            raise TypeError("Position should be specified in ints")

        if not isinstance(team, str):
            raise TypeError("Team should a string")

        self.checkValues(armorclass)
        self.checkValues(proficiency)

        self.position=position
        self.team=team
        #Hitpoint dice stuff
        self.usehitdie=hitdie[0]
        self.hitdie=hitdie[1]
        self.hitval=hitdie[2]
        self.hitmod=hitdie[3]

        self.maxhp=1

        self.initiative=self.rollInitiative()

        if self.usehitdie:
            if self.verbose:
                print("Using hit die")
            self.hp = self.setHP()
            self.maxhp=self.hp
        else:
            if self.verbose:
                print("Using basehp")
            self.hp=basehp
            self.maxhp=self.hp

        self.ac = armorclass
        self.prof = proficiency


        self.alive=True

    ############ Individual stats ########################
    def setHP(self):
        if self.verbose:
            print("Rolling HP!")
        i=0
        dicerolls=[]
        while i<self.hitdie:
            dicerolls.append(self.rollDice(self.hitval))
            i+=1

        totalhp=sum(dicerolls)+self.hitmod
        if self.verbose:
            print(f"Rolled {dicerolls}+{self.hitmod} for total of {totalhp}")
        return totalhp

    def changeAC(self, changevalue):
        if self.verbose:
            print(f"Changing AC from {self.ac} to {self.ac+changevalue}")
        self.ac = max(self.ac+changevalue,0)
        return self.ac

    def changeHP(self, changevalue):
        if self.verbose:
            print(f"Changing HP from {self.hp} to {self.hp+changevalue}")
        self.hp = max(self.hp+changevalue,0)
        return self.hp

    def amIAlive(self):
        #Quick check to see if I'm alive or not
        if self.hp<=0:
            self.alive=False
        else:
            self.alive=True
        return self.alive

    def rollInitiative(self):
        initiative=self.statsRoll('Dex')
        if self.verbose:
            print("ROLL FOR INITIATIVE, Rolled {initiative}")
        return initiative
    ################ Dice Rolls ##########################



    def savingThrow(self, statname, savevalue):
        #Returns true if saved, false if not saved
        if statname not in self.statnames:
            raise NameError(f"Could find {statname} please specify one from {self.statnames}")
        saved=False
        _,_,rollvalue=self.statsRoll(statname)
        if rollvalue>=savevalue:
            saved=True
            if self.verbose:
                print(f"Rolled {rollvalue} against {savevalue}, you're saved")
        else:
            if self.verbose:
                print(f"Rolled {rollvalue} against {savevalue}, you failed!")
        return saved

    ############# Other Combat Stuff #############################
    def takeDamage(self, enemyroll, enemydamage):
        #enemyroll : Roll done by oponenent
        #enemydamage : Damage done by oponent
        self.checkValues(enemyroll)
        self.checkValues(enemydamage)
        if self.verbose==True:
            print(f"Enemy has rolled {enemyroll} against your ac of {self.ac}")
        if enemyroll>=self.ac:
            self.changeHP(-enemydamage)
            self.amIAlive()
            if self.alive:
                if self.verbose:
                    print("You take {enemydamage}, HP now : {self.hp}")
            else:
                if self.verbose:
                    print("YOU HAVE DIED!")
        return 1

    def moveCharacter(self, newcoord):
        if self.verbose:
            print(f"Moving from {self.position} to {newcoord}")
        self.position=newcoord




class swarm(basicFunctionality):
    def __init__(self, swarmsize=1, swarmhitdie=[False,0,0,0], swarmac=0, swarmstats=[0,0,0,0,0,0],
                  swarmbasehp=0, team='a', pos=None, verbosity=False,):
        #hitdie=

        super().__init__(swarmstats, verbosity=verbosity)

        self.checkValues(swarmsize)
        self.checkValues(swarmac)

        self.swarmhitdie=swarmhitdie
        self.swarmac=swarmac
        self.swarmsize=swarmsize
        self.swarmstats=swarmstats
        self.swarmbasehp=swarmbasehp

        self.team=team

        if pos==None:
            self.positions=[(int(i),int(j)) for i,j in zip(np.arange(self.swarmsize),
                                             np.arange(self.swarmsize))]
        else:
            if len(pos)<len(list(set(pos))):
                raise ValueError ("All set positions must be unique!")
            if len(pos)<swarmsize:
                raise ValueError ("Positions must account for every swarm member!")
            self.positions=pos

        swarmcounter=0
        self.fullswarm=[]
        while swarmcounter<self.swarmsize:
            self.fullswarm.append(dndCharacter(hitdie     =   self.swarmhitdie,
                                               armorclass =   self.swarmac,
                                               stats      =   self.swarmstats,
                                               position   =   self.positions[swarmcounter],
                                               basehp     =   self.swarmbasehp,
                                               verbosity  =   self.verbose,
                                               team       =   self.team))
            swarmcounter+=1

        #Sort by initiatives
        self.sortSwarmByInitiative() #initiative order
        self.aliveswarm=self.fullswarm
        self.deadswarm=[]

        self.totalalive=len(self.aliveswarm)
        self.totaldead=len(self.deadswarm)

    def sortSwarmByInitiative(self):
        if self.verbose:
            print("Sorting")
        initiativedict={sw : sw.initiative for sw in self.fullswarm}
        self.initiatives={k : v for k,v in sorted(initiativedict.items(),
                                                 key=lambda item: item[1])}
        self.fullswarm=list(self.initiatives.keys())

        return 1


    def swarmAttack(self, numberofattackers=0, enemyac=10):
        if numberofattackers>len(self.aliveswarm):
            raise ValueError("Number of attackers cannot exceed swarmsize")
        attackerindices=sorted(random.sample(range(0,self.swarmsize), numberofattackers))

        damage=0
        rollvals=[]
        for i in attackerindices:
            attacker=self.aliveswarm[i]
            if attacker.amIAlive:
                rollval, dmg=attacker.rollToHit(enemyac)
                damage+=dmg
                rollvals.append(rollval)
            else:
                if self.verbose:
                    print("Attempted to attack with a dead man!")
        if self.verbose:
            print(f"Total damage is : {damage}")

        return damage, rollvals

    def cleanTheDead(self):
        tempalive=[]
        tempdead=[]
        for sw in self.fullswarm:
            if sw.amIAlive():
                tempalive.append(sw)
            else:
                tempdead.append(sw)
        self.aliveswarm=tempalive
        self.deadswarm=tempdead
        if len(self.aliveswarm)==0:
            print(f"Swarm {self.team} is dead!")
        else:
            if self.verbose:
                print(f"Total alive : {len(self.aliveswarm)}\n Total dead : {len(self.deadswarm)}")


    def changeSwarmHP(self, changehp):
        self.checkValues(changehp)
        for sw in self.fullswarm:
            sw.changeHP(changehp)
        if self.verbose:
            print("Whole swarm has had {changehp} added to their hp")
        self.cleanTheDead()
        return 1

    def rollAgainstSwarm(self, enemyroll, enemydamage):
        for sw in self.aliveswarm:
            sw.takeDamage(enemyroll, enemydamage)
        self.cleanTheDead()

    def statCheckSwarm(self, stat, statcheck):
        for sw in self.fullswarm:
            sw.savingThrow(stat, statcheck)
        return 1

    def equipSwarm(self, totaltoarm=0, rearm=False, armrandom=False, armindexarr=None,
                 weaponstat='Str', tohit=0, weapondice=0, weapondamage=0,
                    damagemodifier=0, damagetype="Piercing", ranged=False):


        #Takes total number of swarm to arm and if this arming should be
        #random; Arm index if specific indices are preffered
        if armrandom and armindexarr!=None:
            raise SyntaxError("Cannot arm specific troops and have random on!")
        if not isinstance(armrandom, bool):
            raise TypeError("Cannot have non-bool entry for arm random")
        self.checkValues(totaltoarm)
        if totaltoarm>len(self.aliveswarm):
            raise ValueError("Total Armed cannot exceed living swarm size!")

        if self.verbose:
            print(f"Attempting to arm {totaltoarm} members of the swarm!")

        if not armrandom and armindexarr!=None:
            if self.verbose:
                print(f"Did not specify random or arms, arming first {totaltoarm} unarmed members")

        totalunarmed=0
        arraytoarm=[]
        for idx, cha in enumerate(self.aliveswarm):
            if cha.equiped==True:
                if rearm==True:  
                    arraytoarm.append(idx)
                    totalunarmed+=1
            else:
                arraytoarm.append(idx)
                totalunarmed+=1


        if armindexarr!=None:
            for i in armindexarr:
                if i>totalunarmed-1:
                    raise ValueError(f"Specified value of {i} exceeds total alive {len(self.aliveswarm)}")

        if not rearm and totaltoarm>totalunarmed:
            if self.verbose:
                print(f"Total troops requested exeeds total available, reducing total to {totalunarmed}")
            totaltoarm=totalunarmed

        if armrandom:
            armindexarr=random.sample(arraytoarm, totaltoarm)
        elif armindexarr==None:
            armindexarr=arraytoarm[0:totaltoarm]

        for arm in armindexarr:
                self.aliveswarm[arm].equipWeapon(weaponstat, tohit,
                                             weapondice, weapondamage,
                                             damagemodifier, damagetype, ranged)



#################################################################
#MAKE THEM FIGHT

class singleCombat():
    def __init__(self, character1, character2, verbosity=False):
    #Takes 2 dnd characters as input and makes them fight!
       self.character1=character1
       self.character2=character2
       self.verbose=verbosity
       if self.verbose:
           self.checkHP(self.character1, self.character2)


    def checkHP(self, c1, c2):
        print(f"Character 1 ({c1.team}) HP : {c1.hp}")
        print(f"Character 2 ({c2.team}) HP : {c2.hp}")
        return c2.hp, c2.hp

    def charattack(self, c1, c2):
        #Takes 2 characters and fights them
        rollval, dmg=c1.rollToHit(c2.ac)
        c2.takeDamage(rollval, dmg)
        if self.verbose:
            print(f"Rolled {rollval} and {dmg} damage against {c2.ac} AC")
        if self.verbose:
            c1hp,c2hp=self.checkHP(c1, c2)
        return 1


    def singleround(self):
        if self.character1.initiative > self.character2.initiative:
            if self.verbose:
                print("Character 1 goes first!")
            self.charattack(self.character1, self.character2)
            if self.character1.amIAlive() and self.character2.amIAlive():
                self.charattack(self.character2, self.character1)
        else:
            if self.verbose:
                print("Character 2 goes first!")
            self.charattack(self.character2, self.character1)

            if self.character1.amIAlive() and self.character2.amIAlive():
                self.charattack(self.character1, self.character2)



    def attackloop(self):
        #Loops attack until someone dies
        if self.character1.initiative >= self.character2.initiative:
            turn=0
        else:
            turn=1

        while self.character1.amIAlive() and self.character2.amIAlive():
            if self.verbose:
                print("Combat now on turn {turn}")
            if turn%2==0:
                self.charattack(self.character1, self.character2)
            else:
                self.charattack(self.character2, self.character1)
            turn+=1
        if self.verbose:
            print(f"Combat over, took {turn} turns")



class groupCombat():
    def __init__(self, swarm1, swarm2, verbosity):
        #Takes two swarms and makes them fight!
        self.swarm1=swarm1
        self.swarm2=swarm2

        self.verbose=verbosity

    def selectcombatants(self):
        fighter1=random.randint(0,len(self.swarm1.aliveswarm)-1)
        fighter2=random.randint(0,len(self.swarm2.aliveswarm)-1)
        return fighter1, fighter2

    def individualfight(self, fighter1, fighter2):
        #2 swarm members fight
        if fighter1>=len(self.swarm1.aliveswarm):
            raise ValueError(f"{fighter1} exceeds number of members of swarm1")
        if fighter2>=len(self.swarm2.aliveswarm):
            raise ValueError(f"{fighter2} exeeds number of members of swarm2")


        if not self.swarm1.aliveswarm[fighter1].amIAlive():
            if self.verbose:
                print("Fighter 1 of swarm {swarm1.team} is already dead!")
                return 1

        if not self.swarm2.aliveswarm[fighter2].amIAlive():
            if self.verbose:
                print("Fighter 2 of swarm {swarm2.team} is already dead!")
                return 1

        combat=singleCombat(self.swarm1.aliveswarm[fighter1],
                            self.swarm2.aliveswarm[fighter2],
                            verbosity=self.verbose)
        combat.singleround()
        if self.verbose:
            print(f"SWARM 1 HAS {len(self.swarm1.aliveswarm)} MEMBERS LEFT")
        self.swarm1.cleanTheDead()
        if self.verbose:
            print(f"SWARM 2 HAS {len(self.swarm2.aliveswarm)} MEMBERS LEFT")
        self.swarm2.cleanTheDead()
        if self.verbose:
            print("==============")
        return 1

    def allOutWar(self):
        #Two swarms fight until 1 is eliminated
        turn=0
        while len(self.swarm1.aliveswarm)!=0 and len(self.swarm2.aliveswarm)!=0:
            f1, f2 = self.selectcombatants()
            if self.swarm1.aliveswarm[f1].amIAlive() and self.swarm2.aliveswarm[f2].amIAlive():
                self.individualfight(f1,f2)
                turn+=1
        if self.verbose:
            print(f"Combat over, took {turn} turns")
        return len(self.swarm1.aliveswarm), len(self.swarm2.aliveswarm)


class mapstuff:
    def __init__(self, mapshape=np.zeros((10,10)), verbosity=False):
        #Mapshape : Define some space, 0s are accesible 1s are not
        if(np.size(mapshape)==0):
            raise ValueError("mapshape must be larger than 0!")
        self.map=mapshape.astype(str)
        self.resetMap()
        self.verbose=verbosity

    def resetMap(self):
        for row in self.map:
            for el in range(len(row)):
                if row[el]!='1':
                    row[el]='0'
        return 1


    def updatePositions(self, newcoords, team):
        #Takes list of tuples of starting positions for each fighter and plots on grid
        #team is some string

        self.resetMap()
        if not isinstance(team, str):
            raise TypeError("Team must be of type str")
        for i in newcoords:
            for j in [0,1]:
                if i[j]>=self.map.shape[j]:
                    i[j]=self.map.shape[j]-1
                    if self.verbose:
                        print("Specified coordminate out of range, setting to max")
            self.map[i]=team

        return newcoords

    def movecharacter(self, oldpos, newpos, team):
        self.map[oldpos]='0'
        self.map[newpos]=team

    def distance(self, pos1, pos2):
        #Gives n-dimensional taxi gap
        if len(pos1)!=len(pos2):
            raise SyntaxError("Dimension of positions must match")
        dist=0
        for i, p1 in enumerate(pos1):
            dist+=abs(p1-pos2[i])
        return dist

    def freepoints(self, pos):
        freepoints=[]
        for posx in range(-1,2):
            for posy in range(-1,2):
                #print(posx,posy)
                if self.map[(pos[0]+posx,pos[1]+posy)]=='0':
                    freepoints.append((posx,posy))
        return freepoints

    def closestenemy(self, position, enemyswarm):
        #here we'll use taxicab metric
        totalenemies=len(enemyswarm.aliveswarm)
        enemypositions=[e.position for e in enemyswarm.aliveswarm]
        distances=[self.distance(position, epos) for epos in enemypositions]

        enemydistdict={d : sw for sw, d in zip(enemyswarm.aliveswarm, distances)}
        enemydistssorted=collections.OrderedDict(sorted(enemydistdict.items()))
        enemydistlist=list(enemydistssorted.keys())

        target=None

        count=0
        while count<totalenemies:

            dis=enemydistlist[count]
            sw=enemydistssorted[dis]
            pos=sw.position
            surroundings=self.freepoints(pos)

            if len(surroundings)==0 or sw.hp<=0:
                count+=1
                continue
            else:
                position=surroundings[0]
                count=totalenemies+2
                target=sw

        return position, target

    def furthestfreepoint(self, position, enemyswarm):
        #gets furthest point from a swarm
        enemypositions=[e.position for e in enemyswarm.aliveswarm]
        freespace=[]
        largestdist=-1
        bestcoord=position

        for rowcoord, rowvals in enumerate(self.map):
            for colcoord, colval in enumerate(rowvals):
                if colval=='0':
                    freespace.append((rowcoord, colcoord))
        if len(freespace)==0:
            if self.verbose:
                print("NOWHERE TO RETREAT TO! (coward)")
            return position
        for i in freespace:
            meandist=np.mean([self.distance(i, ep) for ep in enemypositions])
            if meandist>largestdist:
                largestdist=meandist
                bestcoord=i

        if self.verbose:
            print(f"Furthest coordinate is {bestcoord}, distance={largestdist}")
        return bestcoord, largestdist


class characterAI(mapstuff):
    def __init__(self, character, mapshape=np.zeros((10,10)),
                 verbosity=False):
        #character = dnd character
        #mapshape -> Comes from map stuff
        self.char=character

        mapstuff.__init__(self, mapshape, verbosity)

    def movenear(self, enemyswarm):
        oldpos=self.char.position
        
        newpos, target = self.closestenemy(oldpos, enemyswarm)
        self.char.position=newpos
        
        self.movecharacter(oldpos, self.char.position, self.char.team)
        if self.verbose:
            print(f"Moved to {self.char.position}")
        return target

    def meleeAttack(self, enemyswarm):
        if self.verbose:
            print("Moving in for a melee attack")
        target=self.movenear(enemyswarm)
        if target==None:
            if self.verbose:
                print("No target available!")
            return 0
        combat=singleCombat(self.char,target,
                            verbosity=self.verbose)
        combat.charattack(self.char, target)
        if self.verbose:
            print("Fight ended!")
        return 1

    def retreatInstinct(self, enemyswarm):
        if self.verbose:
            print("Attempting to run!")
        coord,_=self.furthestfreepoint(self.char.pos,enemyswarm)
        if self.verbose:
            print(f"Retreating to {coord}")
        oldcoord=self.char.position
        self.char.position=coord
        self.movecharacter(oldcoord, self.char.position,self.char.team)
        return 1
    
    def rangedAttack(self, enemyswarm):
        _,target=self.closestenemy(self.char.position,enemyswarm)
        if self.distance(target.position, self.char.position)<2:
            self.retreatInstinct(enemyswarm)
            if self.verbose:
                print("Enemy too close to ranged attack, retreating")
        else:
            if self.verbose:
                print(f"Doing ranged attack on enemy at {target.position}")
            combat=singleCombat(self.char, target)
            combat.charattack(self.char, target)
        return 1
    
    def combatTechnique(self, enemyswarm):
        if self.char.ranged:
            self.rangedAttack(enemyswarm)
        else:
            self.meleeAttack(enemyswarm)

class swarmAI:
    def __init__(self, swarm1, swarm2, mapshape=np.zeros((30,30)), verbosity=False):
        #Takes 2 swarms and makes them fight "intelligently"
        self.swarm1=swarm1
        self.swarm2=swarm2
        self.mapshape=mapshape
        self.verbose=verbosity

        self.swarm1AI=[characterAI(ai, self.mapshape,
                                   self.verbose) for ai in swarm1.fullswarm]

        self.swarm2AI=[characterAI(ai, self.mapshape,
                                   self.verbose) for ai in swarm2.fullswarm]

        self.order=0
        self.turnarr={}

        self.turnorder()



    def turnorder(self):
        swarm1_inits=[i[2] for i in list(self.swarm1.initiatives.values())]
        swarm2_inits=[i[2] for i in list(self.swarm2.initiatives.values())]

        s1_i=0
        s2_i=0

        while self.order<len(self.swarm1.initiatives)+len(self.swarm1.initiatives):
            if s1_i>=len(self.swarm1.initiatives):
                s1init=-999
            else:
                s1init=swarm1_inits[s1_i]

            if s2_i>=len(self.swarm2.initiatives):
                s2init=-999
            else:
                s2init=swarm2_inits[s2_i]

            if s1init>=s2init:
                self.turnarr[self.order] = [self.swarm1.fullswarm[s1_i],
                                            self.swarm1AI[s1_i], self.swarm2]
                s1_i+=1
            else:
                self.turnarr[self.order] = [self.swarm2.fullswarm[s2_i],
                                            self.swarm2AI[s2_i], self.swarm1]
                s2_i+=1
            self.order+=1

    def oneturnswarmcombat(self):
        #does one turn of combat for the swarm
        combatnum=1
        if self.verbose:
            print("DOING COMBAT!")
        for i in range(self.order):
            attackclass, attacker, defender=self.turnarr[i]
            didfight=0
            if attackclass.amIAlive():
                if self.verbose:
                    print(f"Fight {combatnum}")
                    print("-----")
                didfight=attacker.combatTechnique(defender)
                self.swarm1.cleanTheDead()
                self.swarm2.cleanTheDead()
                if self.verbose:
                    print("")
            combatnum+=1
            if self.verbose and didfight==1:
                averagehp1=np.mean([i.hp for i in self.swarm1.fullswarm])
                averagehp2=np.mean([i.hp for i in self.swarm2.fullswarm])
                print(f"Swarm 1 (team {self.swarm1.team}) has {len(self.swarm1.aliveswarm)} survivors")
                print(f"Swarm 1 (team {self.swarm1.team}) average HP : {averagehp1}")
                print(f"Swarm 2 (team {self.swarm2.team}) has {len(self.swarm2.aliveswarm)} survivors")
                print(f"Swarm 2 (team {self.swarm2.team}) average HP : {averagehp2}")
                print("")

        if self.verbose:
            if len(self.swarm1.aliveswarm)==0:
                print(f"SWARM 2 (TEAM {self.swarm2.team}) WINS!")
                print(f"TEAM {self.swarm2.team} HAS {len(self.swarm2.aliveswarm)} survivors")
            else:
                print(f"SWARM 1 (TEAM {self.swarm1.team}) WINS!")
                print(f"TEAM {self.swarm1.team} HAS {len(self.swarm1.aliveswarm)} survivors")

    def runfullcombat(self):
        totalrounds=1
        while len(self.swarm1.aliveswarm)>=1 and len(self.swarm2.aliveswarm)>=1:
            if self.verbose:
                print("\n=============================")
                print(f"ROUND {totalrounds})")
            self.oneturnswarmcombat()
            self.swarm1.cleanTheDead()
            self.swarm2.cleanTheDead()
            totalrounds+=1

if __name__ == "__main__":
    swarmpos=[(10,10), (9,4), (2,4), (9,1), (3,9)]
    swarmpos2=[(10,0), (5,4), (1,3), (9,9), (0,0)]

    s1=swarm(swarmsize=5, swarmac=14, swarmbasehp=12,
                swarmstats=[10, 10, 12, 10, 8, 16], team='a', pos=swarmpos)
    s1.equipSwarm(totaltoarm=2, rearm=True, tohit=3, 
                  weapondice =2, weapondamage=8)
    s1.equipSwarm(totaltoarm=3, rearm=False, weaponstat='Dex', tohit=4,
                  weapondice=1, weapondamage=10,ranged=True)

    s2=swarm(swarmsize=5, swarmac=14, swarmbasehp=12,
                swarmstats=[10, 10, 12, 10, 8, 16], team='b', pos=swarmpos2)
    s2.equipSwarm(totaltoarm=5, rearm=True, tohit=3, 
                  weapondice =2, weapondamage=8)
   

    ai=swarmAI(s1, s2, mapshape=np.zeros((12,12)), verbosity=True)
    ai.runfullcombat()
