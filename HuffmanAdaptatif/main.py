from math import log2;

def c2b(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def b2c(b):
    return chr(int(b,2))

class Node:
    def __init__(self, data, weight=0):
        self.left = None
        self.right = None
        self.data = data
        self.weight = weight

def copy(node):
    if node == None:
        return None
    else :
        c=Node(node.data, node.weight)
        c.left = copy(node.left)
        c.right = copy(node.right)
    return c

def search(n, d):
    if n.data == d:
        return ""
    else :
        if isinstance(n.left, Node) and search(n.left, d) != -1 :
            return "0"+search(n.left, d)
        else :
            if isinstance(n.right, Node) and search(n.right, d) != -1 :
                return "1"+search(n.right, d)
            else :
                return -1

def search2(tree, node):
    if tree == node:
        return ""
    else :
        if isinstance(tree.left, Node) and search2(tree.left, node) != -1 :
            return "0"+search2(tree.left, node)
        else :
            if isinstance(tree.right, Node) and search2(tree.right, node) != -1 :
                return "1"+search2(tree.right, node)
            else :
                return -1

def searchMax(tree):
    if isLeaf(tree):
        return tree
    elif searchMax(tree.left) >= search(tree.right):
        return searchMax(tree.left)
    else :
        return searchMax(tree.right)

def echange(tree, node1, node2):
    c1=copy(node1)
    c2=copy(node2)
    t=tree
    way1 = search2(tree, node1)
    way2 = search2(tree, node2)
    for x in way1[:-1]:
        if x =="0":
            t=t.left
        else:
            t=t.right
    if way1[-1]=="0":
        t.left=c2
    else:
        t.right=c2
    t=tree
    for x in way2[:-1]:
        if x == "0":
            t = t.left
        else:
            t = t.right
    if way2[-1]=="0":
        t.left = c1
    else:
        t.right = c1
    return c1

def isLeaf(node):
    return node.left == None or node.right == None

def parLargeur(tree):
    f=[]
    f+=[[tree, tree.weight]]
    i=0
    while i<len(f):
        if not isLeaf(f[i][0]):
            f += [[f[i][0].right, f[i][0].right.weight], [f[i][0].left, f[i][0].left.weight]]
        i += 1
    return f

def estFils(tree, node):
    if node == tree:
        return True
    elif tree == None:
        return False
    else:
        return estFils(tree.left, node) or estFils(tree.right, node)

def getParent(tree, node):
    if tree.left == node or tree.right == node:
        return tree
    else:
        if estFils(tree.left, node):
            return getParent(tree.left, node)
        elif estFils(tree.right, node):
            return getParent(tree.right, node)
        else:
            return -1

def inverse(l):
    f=[]
    for x in l:
        f=[x]+f
    return f

def exchange(tree, node):
    if node == tree:
        return
    l = parLargeur(tree)
    i=0
    while l[i][0] != node and (l[i][1] >= node.weight or estFils(l[i][0], node)):
        i+=1
    if node != l[i][0]:
        a = echange(tree, node, l[i][0])
    else:
        a = node
    p = getParent(tree, a)
    p.weight +=1
    if p != tree:
        exchange(tree, getParent(tree, a))
    if a == node:
        return -1
    else :
        return a


def update(tree, node):
    n = tree
    while n != node:
        if estFils(n.left, node):
            n = n.left
        else:
            n=n.right
    exchange(tree, n)

def estFeuille(node):
    if node.left == None and node.right == None :
        return True
    else:
        return False

def goTo(tree, way):
    t = tree
    for x in way:
        if x == "0":
            t = t.left
        else:
            t = t.right
    return t

def entropie(tree):
    s=0
    e=0
    l=[]
    for x in parLargeur(tree):
        if isLeaf(x[0]) and x[0].data != "NYT":
            s+=x[1]
            e+=len(search2(tree, x[0])*x[1])
            l+=[x[1]]
    eopt = 0
    for x in l:
        eopt+= (x/s) * log2(s/x)
    return e/s, eopt


def encode(m, tree = Node("NYT")):
    code = ""
    for x in m:
        if search(tree, x) == -1:
            way = search(tree, "NYT")
            code = code + " " + way + " " + c2b(x)
            t = tree
            for w in way:
                if w == "0":
                    t = t.left
                else:
                    t = t.right
            t.data=""
            t.left=Node("NYT")
            t.right=Node(x, 1)
            update(tree, t.right)
        else :
            way = search(tree, x)
            code = code + " " + way
            t = tree
            for w in way:
                if w == "0":
                    t = t.left
                else:
                    t = t.right
            t.weight += 1
            update(tree, t)

    return tree, code

def decode(c, tree = Node("NYT")):
    mot = ""
    x = c[:8]
    mot += b2c(x)
    tree.data = ""
    tree.left = Node("NYT")
    tree.right = Node(b2c(x), 1)
    c=c[8:]
    while len(c) != 0:
        w=""
        while not estFeuille(goTo(tree, w)) and len(c)>0:
            w += c[0]
            c = c[1:]
        n = goTo(tree, w)
        if n.data == "NYT":
            char = b2c(c[:8])
            c = c[8:]
            n.data = ""
            n.left = Node("NYT")
            n.right = Node(char, 1)
            mot += char
            update(tree, n.right)
        else:
            char = goTo(tree, w).data
            mot+=char
            goTo(tree, w).weight+=1
            update(tree, goTo(tree, w))
    return tree, mot


mot2 = "Quoique ce detail ne touche en aucune maniere au fond meme de ce que nous avons a raconter, il nest peut-etre pas inutile, ne fet-ce que pour etre exact en tout, dindiquer ici les bruits et les propos qui avaient couru sur son compte au moment ou il etait arrive dans le diocese. Vrai ou faux, ce quon dit des hommes tient souvent autant de place dans leur vie et surtout dans leur destinee que ce quils font. M. Myriel etait fils dun conseiller au parlement dAix; noblesse de robe. On contait de lui que son pere, le reservant pour heriter de sa charge, lavait marie de fort bonne heure, a dix-huit ou vingt ans, suivant un usage assez repandu dans les familles parlementaires. Charles Myriel, nonobstant ce mariage, avait, disait-on, beaucoup fait parler de lui. Il etait bien fait de sa personne, quoique dassez petite taille, elegant, gracieux, spirituel; toute la premiere partie de sa vie avait ete donnee au monde et aux galanteries. La revolution survint, les evenements se precipiterent, les familles parlementaires decimees, chassees, traquees, se disperserent. M. Charles Myriel, des les premiers jours de la revolution, emigra en Italie. Sa femme y mourut dune maladie de poitrine dont elle etait atteinte depuis longtemps. Ils navaient point denfants. Que se passa-t-il ensuite dans la destinee de M. Myriel? Lecroulement de lancienne societe francaise, la chute de sa propre famille, les tragiques spectacles de 93, plus effrayants encore peut-etre pour les emigres qui les voyaient de loin avec le grossissement de lepouvante, firent-ils germer en lui des idees de renoncement et de solitude? Fut-il, au milieu dune de ces distractions et de ces affections qui occupaient sa vie, subitement atteint dun de ces coups mysterieux et terribles qui viennent quelquefois renverser, en le frappant au coeur, lhomme que les catastrophes publiques nebranleraient pas en le frappant dans son existence et dans sa fortune? Nul naurait pu le dire; tout ce quon savait, cest que, lorsquil revint dItalie, il etait pretre. En 1804, M. Myriel etait cure de Brignolles. Il etait deja vieux, et vivait dans une retraite profonde."
mot = "maman"
code = ""


#res = encode(mot)
#print(res[0].right.weight)
#print(res[0].right.right.data)
#print(res[1])
#print(len(res[1]))
#print(parLargeur(res[0]))
#m = res[1].replace(" ", "")
#print(m)
#print(len(m))
#print(len(mot2)*8)

#resbis = decode(m)
#print(resbis[1])
#print(entropie(res[0]))

message = mot2

print("Le message est : "+message)

res = encode(message)
c = res[1].replace(" ", "")
print("Le code est : ", end="")
print(res[1], end="")
print(" ou ", end="")
print(c)
t = len(c)
print("Le taux de compression est ", end="")
print(1-(t/(len(message)*8)))
print("La longueur moyenne et l'entropie sont :", end="")
print(entropie(res[0]))
print("Le message décodé est : ", end="")
print(decode(c)[1])