import random
import time
from termcolor import colored


# Speler stats
speler_health = 100
speler_shield = 0
speler_samen = speler_health + speler_shield

def fortnite():
    global speler_health, speler_shield, speler_samen  # Om de globale variabelen te gebruiken
    speler_health = 100
    speler_shield = 0
    speler_samen = speler_health + speler_shield
    ren = 'nee'

    print()
    print(colored('Welkom bij Fortnite Battle Royale!', 'red'))
    time.sleep(0.5)
    print('Je gaat vandaag proberen te overleven op een map met 99 vijanden.')
    time.sleep(0.5)
    print('Je begint in een Battle Bus die langs de map vliegt.')
    time.sleep(0.5)
    print('Je mag kiezen waar je wilt landen.')
    time.sleep(0.5)
    print('Je begint met' + colored(' 100 HP ', 'green'))
    time.sleep(0.5)
    print('En' + colored (' 0 shield', 'blue'))
    time.sleep(0.5)
    print('Keuzes: Pleasant Park, Tilted Towers, Loot Lake')


    keuze_land = input('Waar wil je landen? ').lower()

    if keuze_land == 'pleasant park':
        PP = input("Top, op welk huisje ga je landen? Blauw/Geel/Groen: ").lower()
        if PP == 'blauw':
            print('Je landt op het blauwe huis. Je opent een kist en krijgt een AR, ammo en 3 mini shields.')
            speler_shield += 50
        elif PP == 'geel':
            print('Je landt op het gele huis. Je opent een kist en krijgt een Scar, ammo en een grote shield.')
            speler_shield += 50
        elif PP == 'groen':
            print('Je landt op het groene huis. Je opent een kist en krijgt een pistol, ammo en bandages.')
        else:
            print('Ongeldige keuze! Huis bestaat niet. Probeer in andere potje!')
            quit()
            

    elif keuze_land == 'tilted towers':
        TT = input('Top, op welk gebouw wil je landen? Big Ben/Kroon/Boom: ').lower()
        if TT == 'big ben':
            print('Je landt bij de Big Ben. Je vindt een sniper en een paar granaten.')
        elif TT == 'kroon':
            print('Je landt op het Kroon-gebouw en krijgt een SMG en 3 kleine shields.')
            speler_shield += 50
        elif TT == 'boom':
            print('Je landt op het Boom-gebouw en krijgt een shotgun en bandages.')
        else:
            print('Ongeldige keuze! Gebouw bestaat niet. Probeer in andere potje!')
            quit()
        

    elif keuze_land == 'loot lake':
        LL = input('Top, waar wil je landen? Gras/Huis: ').lower()
        if LL == 'gras':
            print('Je landt in het gras bij Loot Lake. Je vindt een revolver en een medkit.')
        elif LL == 'huis':
            print('Je landt in het huis bij Loot Lake. Je vindt een burst rifle en 3 kleine shields.')
            speler_shield += 50
        else:
            print('Ongeldige keuze! Locatie bestaat niet. Probeer in andere potje!')
            quit()
            
    else:
        print('Ongeldige invoer!!!. Je kan nergens landen. Probeer andere potje!')
        quit()
        
        

    # Zorg dat shields niet boven 100 gaan
    if speler_shield > 100:
        speler_shield = 100

    print(f'\nJe gezondheid:' + colored (speler_health, 'green'))
    print(f'Je shields:' + colored (speler_shield, 'blue'))
    speler_samen = speler_health + speler_shield
    print(f'Samen:' + colored (speler_samen, 'yellow'))
    print()

    # Aantal vijanden dat over is
    getal = random.randint(50, 100)
    print(f'Er zijn nog {getal} vijanden over.')

    # Vechten of wegrennen
    v_of_w = input('\nJe ziet een vijand die je komt pushen. Wat doe je? vechten/wegrennen ').lower()

    if v_of_w == 'vechten':
        print('Je hebt besloten om te vechten tegen je vijand.')
        damage = random.randint(1, 200)
        print(f'Je vijand doet' + colored (damage, 'red') + 'damage')

        if damage > speler_samen:
            print('Helaas, je vijand heeft je verslagen. Je bent dood.')
            return False  # Spel beëindigen
        else:
            print('Je hebt je vijand verslagen!')
            speler_samen -= damage
            speler_health = max(0, speler_samen - speler_shield)  # Update health zonder shield
            print(f'Je hebt nog' + colored(speler_samen, 'yellow') + 'HP over.')

    elif v_of_w == 'wegrennen':
        print('Je hebt gekozen om weg te rennen. De storm heeft je ingehaald.')
        storm = random.randint(1, 99)
        print(f'De storm doet' + colored (storm, 'magenta') + 'damage')
    else:
        print('Dat is geen optie. Probeer opnieuw! ')
        quit()
    

        if storm > speler_samen:
            print('Oh nee, je bent dood door de storm. Eliminated by: Storm.')
            return False  # Spel beëindigen
        else:
            speler_samen -= storm
            speler_health = max(0, speler_samen - speler_shield)
            print(f'Je hebt nog' + colored(speler_health, 'green') + 'HP en' + colored(speler_shield, 'blue') + 'shield over.')

    # Loot keuze na gevecht
    if speler_samen > 0:
        loot_choice = input('Wil je de loot van iemand oppakken of bij je eigen blijven? oppakken/blijven ').lower()
        if loot_choice == 'oppakken':
            print('Je hebt de loot van je vijand opgepakt. Je hebt nu een Shotgun, MedKit en een grappler.')
        elif loot_choice == 'blijven':
            print('Je blijft bij je eigen loot.')
        else:
            ('Ongeldige invoer!')
            quit()

    # Vending machine, healing halen
    if speler_health < 50 or loot_choice == 'blijven':
        print('Je hebt weinig hp. Je ziet een vending machine met healing in de storm.')
        ren = input('Ren je daar naartoe? ja/nee ').lower()
        if loot_choice == 'blijven' or speler_health < 50:
            print()

        if ren == 'ja':
            print('Je rent naar de vending machine om healing te halen en daarna ga je pushen.')
            print('In de vending machine heb je: 1) big pot, 2) medkit, 3) chug jug.')
            wat = input('Wat kies je? 1, 2 of 3: ').lower()

            if wat == '1':
                print('Je hebt big pot gekozen.' + colored( '+50 shield.', 'green'))
                speler_shield += 50
                speler_health == speler_samen
            elif wat == '2':
                print('Je hebt medkit gekozen.' +  colored( '+50 hp.', 'green'))
                speler_health += 50
            elif wat == '3':
                print('Je hebt chug jug gekozen. Full health en shield!')
                speler_health = 100
                speler_shield = 100
            else:
                print('Ongeldige keuze!')

            # Zorg dat shields en health niet boven de 100 komen
            if speler_shield > 100:
                speler_shield = 100
            if speler_health > 100:
                speler_health = 100

            print(f'Je hebt nu' + colored(speler_health, 'green') + 'HP en' + colored(speler_shield, 'blue') + 'shield.')

    print()
    vijand2 = random.randint(5, 30)
    print(f'Er zijn nog {vijand2} vijanden over.')
    print()

    # pushen
    if ren == 'nee':
        print('Je hebt gekozen voor nee. Dus je gaat vijanden zoeken')
        print('Je ziet in de verte twee vijanden links en rechts')

        push = input('Welke ga je eerst pushen? links of rechts ').lower()
        print()
        if push == 'rechts':
            print('Je pusht rechter tegenstander')
            print('Hij wilt steen, papier, schaar met je spelen')
            sps = input('Wat kies je? (steen/papier/schaar): ').lower()
            print()
            woorden = ['steen', 'papier', 'schaar']
            random_woord = random.choice(woorden)

            print(f'Je vijand kiest {random_woord}')

            if sps == 'steen' and random_woord == 'schaar':
                print('Je hebt tegen hem gewonnen!')
            elif sps == 'steen' and random_woord == 'papier':
                print('Je hebt verloren')
                return False  # Spel beëindigen
            elif sps == 'papier' and random_woord == 'steen':
                print('Je hebt tegen hem gewonnen!')
            elif sps == 'papier' and random_woord == 'schaar':
                print('Je hebt verloren')
                return False  # Spel beëindigen
            elif sps == 'schaar' and random_woord == 'papier':
                print('Je hebt tegen hem gewonnen!')
            elif sps == 'schaar' and random_woord == 'steen':
                print('Je hebt verloren')
                return False  # Spel beëindigen
            elif sps == random_woord:
                print('Jullie doden elkaar tegelijke tijd.')
                quit()
                  # Roep de functie opnieuw aan voor gelijkspel
            else:
                print('Ongeldige invoer')

        elif push == 'links':
            print('Je hebt gekozen om je linker vijand te pushen')
            print('Maar hij is bang en rent weg')
            print('Je bent veilig')
            print('Je komt lang niemand tegen')
            print()

    print('Je komt in gevecht met een laatste vijand')
    print('Je voelt de spanning toenemen')

    actie = input("Wat doe je? Schiet van veraf of ga je dichterbij vechten? (veraf/dichtbij): ").lower()

    if actie == "veraf":
        print("Je pakt je sniper en mikt op de vijand van veraf.")
        resultaat = random.randint(1, 2)
        if resultaat == 1:
            print("Je hebt een perfecte headshot gemaakt! De vijand is verslagen!")
        else:
            print("De vijand teleporteert! Hij komt dichterbij en begint aan te vallen.")
            

    elif actie == "dichtbij":
        print("Je rent naar de vijand met je shotgun in de aanslag!")
        resultaat = random.randint(1, 2)
        if resultaat == 1:
            print("BOOM! Je hebt hem van dichtbij geraakt! De vijand valt op de grond.")
        else:
            print("De vijand ontwijkt je en activeert een krachtig schild! Je moet snel een andere strategie bedenken.")
            # Meer actie-opties hier

    else:
        print("Ongeldige keuze, de vijand valt je aan!")

    # Eindresultaat
    if resultaat == 1:
        print(colored('VICTORY ROYALE', 'yellow'))
    else:
        print('De vijand was te sterk en je verliest. HELAAS!!')

    # Herstarten van het spel
    opnieuw = input('Wil je nog een keer spelen? ja/nee ').lower()
    if opnieuw == 'ja':
        fortnite()
    else:
        print('Bedankt voor het spelen!')

fortnite()
