from math import log2

def addTable(l, c):
    if c in l[0]:
        l[1][l[0].index(c)] += 1
    else:
        l[0].append(c)
        l[1].append(1)


def sort(l):
    res = [[], []]
    i = 1
    k=0
    while k < len(l[0]):
        for j in range(len(l[0])):
            if l[1][j] == i:
                res[0].append(l[0][j])
                res[1].append(l[1][j])
                k+=1
        i+=1
    return res

def sort2(l):
    res = [[], [], []]
    i = 1
    k=0
    while k < len(l[0]):
        for j in range(len(l[0])):
            if l[1][j] == i:
                res[0].append(l[0][j])
                res[1].append(l[1][j])
                res[2].append(l[2][j])
                k+=1
        i+=1
    return res

def constrTable(t):
    res = t+[[""]*len(t[0])]
    while len(res[0])>1:
        res[2][0]+="0"
        res[2][1]+="1"
        k = [res[0][:2], res[1][0]+res[1][1], res[2][:2]]
        del(res[0][:2])
        del(res[1][:2])
        del(res[2][:2])
        res[0] = [k]+res[0]
        res[1] = [k[1]]+res[1]
        res[2] = [""]+res[2]
        res = sort2(res)

    table = [[], []]
    while len(res[0])>0:
        if isinstance(res[0][0], str):
            table[0]+=res[0][0]
            table[1].append(res[2][0])
            del(res[0][0])
            del(res[2][0])
        else:
            k = res[0][0]
            k[2][0] = res[2][0] + k[2][0]
            k[2][1] = res[2][0] + k[2][1]
            del (res[0][0])
            del (res[2][0])
            res[0] = k[0] + res[0]
            res[2] = k[2] + res[2]
    return(table)

def entropie(m):
    l = [[], []]
    for x in m:
        addTable(l, x)
    t = sort(l)
    table = constrTable(t)
    e=0
    s=0
    for i in range(len(l[0])):
        for j in range(len(table[0])):
            if l[0][i] == table[0][j]:
                e+=len(table[1][j])*l[1][i]
                s+=l[1][i]
    eopt = 0
    for i in range(len(l[0])):
        eopt += (l[1][i]/s) * log2(s/l[1][i])
    return e/s, eopt


def encode(message):
    l = [[], []]
    for x in message:
        addTable(l,x)
    t = sort(l)
    table = constrTable(t)

    code = ""
    for x in message:
        i = table[0].index(x)
        code = code + table[1][i] + " "
    code = code[:-1]
    return table, code

def decode(table, code):
    c = code
    m=""
    k=""
    while len(c)>0:
        k+=c[0]
        c=c[1:]
        if k in table[1]:
            i = table[1].index(k)
            m+=table[0][i]
            k=""
    return(m)

m2 = "maman"
m = "Quoique ce detail ne touche en aucune maniere au fond meme de ce que nous avons a raconter, il nest peut-etre pas inutile, ne fet-ce que pour etre exact en tout, dindiquer ici les bruits et les propos qui avaient couru sur son compte au moment ou il etait arrive dans le diocese. Vrai ou faux, ce quon dit des hommes tient souvent autant de place dans leur vie et surtout dans leur destinee que ce quils font. M. Myriel etait fils dun conseiller au parlement dAix; noblesse de robe. On contait de lui que son pere, le reservant pour heriter de sa charge, lavait marie de fort bonne heure, a dix-huit ou vingt ans, suivant un usage assez repandu dans les familles parlementaires. Charles Myriel, nonobstant ce mariage, avait, disait-on, beaucoup fait parler de lui. Il etait bien fait de sa personne, quoique dassez petite taille, elegant, gracieux, spirituel; toute la premiere partie de sa vie avait ete donnee au monde et aux galanteries. La revolution survint, les evenements se precipiterent, les familles parlementaires decimees, chassees, traquees, se disperserent. M. Charles Myriel, des les premiers jours de la revolution, emigra en Italie. Sa femme y mourut dune maladie de poitrine dont elle etait atteinte depuis longtemps. Ils navaient point denfants. Que se passa-t-il ensuite dans la destinee de M. Myriel? Lecroulement de lancienne societe francaise, la chute de sa propre famille, les tragiques spectacles de 93, plus effrayants encore peut-etre pour les emigres qui les voyaient de loin avec le grossissement de lepouvante, firent-ils germer en lui des idees de renoncement et de solitude? Fut-il, au milieu dune de ces distractions et de ces affections qui occupaient sa vie, subitement atteint dun de ces coups mysterieux et terribles qui viennent quelquefois renverser, en le frappant au coeur, lhomme que les catastrophes publiques nebranleraient pas en le frappant dans son existence et dans sa fortune? Nul naurait pu le dire; tout ce quon savait, cest que, lorsquil revint dItalie, il etait pretre. En 1804, M. Myriel etait cure de Brignolles. Il etait deja vieux, et vivait dans une retraite profonde."
#res = encode(m)
#print (res[0])
#print(res[1])
#print(decode(res[0], res[1].replace(" ", "")))
#print(entropie(m))

message = "zakaria"

print("Le message est : "+message)

res = encode(message)
c = res[1].replace(" ", "")
print("Le code est : ", end="")
print(res[1], end="")
print(" ou ", end="")
print(c)
print("Le dictionnaire est :", end="")
print(res[0])
t = len(c)
print("Le taux de compression est ", end="")
print(1-(t/(len(message)*8)))
print("La longueur moyenne et l'entropie sont :", end="")
print(entropie(message))
print("Le message décodé est : ", end="")
print(decode(res[0],c))