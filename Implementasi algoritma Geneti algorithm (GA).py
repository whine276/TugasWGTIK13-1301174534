import random
import math

#fungsi untuk membagi array/list (digunakan saat crossover)
def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

#menginisiasi populasi secara random berdasarkan ukuran populasi dan panjang kromosomnya
def initRandPop(ukuranPop, pjgKromosom):
    randPop = []
    for i in range(0,ukuranPop):
        col = []
        for j in range(0,pjgKromosom):
            col.append(random.randint(0,9))
        randPop.append(col)
    return randPop

#men-decode 1 kromosom berdasarkan batas bawah  dan batas atas
def decodeGEN(kromosom, batasBawah, batasAtas):
    pembilang = 0.0
    penyebut = 0.0
    for i in range(1, len(kromosom)+1):
        x = 10**(-i)
        pembilang = pembilang + kromosom[i-1] * x
        penyebut = penyebut + x
    hitung = ((batasAtas-batasBawah)/(9*penyebut))*pembilang
    phenotype = batasBawah+hitung
    return phenotype

#men-decode seluruh kromosom pada populasi
def decode(populasi, pjgKromosom):
    decodeAll = []
    for i in range(0,len(populasi)):
        splittedPop = split(populasi[i],len(populasi[i])//2)
        firstKrom = splittedPop[0]
        secondKrom = splittedPop[1]
        decodeFirst = decodeGEN(firstKrom, -1, 2)
        decodeSecond = decodeGEN(secondKrom, -1, 1)
        decodeAll.append([decodeFirst, decodeSecond])
    return decodeAll

#menghitung 1 fitness pada array/list yang sudah di-decode
def hitungFitness(x, y):
    h = (math.cos(math.pow(x,2)) * math.sin(math.pow(y,2))) + (x + y)
    return -h

#menghitung seluruh fitness dan mengeluarkan array/list baru berupa semua fitness
def hitungAllFitness(decKrom):
    allFitness = []
    for i in range(0,len(decKrom)):
        allFitness.append(hitungFitness(decKrom[i][0],decKrom[i][1]))
    return allFitness

# mencari parent menggunakan algoritma tournament selection
def parent_selection(fitness, ukuranPop):
    best = random.randint(0,ukuranPop-1)
    ukuranTournament = random.randint(0,ukuranPop-1)+1
    for i in range(1, ukuranTournament+1):
        selanjutnya = random.randint(0,ukuranPop-1)
        if fitness[best] > fitness[selanjutnya]:
            best = selanjutnya
    return best

#fungsi crossover berdasarkan probabilitas crossover(pc)
def crossover(populasi, fitness, pc, ukuranPop, pjgKromosom):
    n = 0
    child = []
    idxParent = parent_selection(fitness, ukuranPop)
    idxParent2 = parent_selection(fitness, ukuranPop)
    child.append(populasi[idxParent].copy())
    child.append(populasi[idxParent2].copy())
    if random.random() < pc:
        crossOver = random.randint(0,pjgKromosom-1)
        for i in range(crossOver):
            child[0][i] = populasi[idxParent2][i]
            child[1][i] = populasi[idxParent][i]
    return child

#fungsi mutasi berdasarkan probabilitas mutasi(pm)
def mutasi(child, pm, pjgKromosom):
    if random.random() < pm:
        child[random.randint(0,pjgKromosom-1)] = random.randint(0,9)

#mencari survivor dengan parameter fitnessnya
def getSurvivor(fitness):
    idxMax = 0
    for i in range(len(fitness)):
        if fitness[i] < fitness[idxMax]:
            idxMax = i
    return idxMax

#me-replace seluruh populasi lama ke populasi baru
def generalReplacement(poplama, popbaru, fitness, ukuranPop, pjgKromosom):
    newpop = []
    newpop.append(poplama[getSurvivor(fitness)].copy())
    newpop.append(poplama[getSurvivor(fitness)].copy())
    for i in range(2,len(popbaru)):
        newpop.append(popbaru[i].copy())
    return newpop

ukuranPopulasi = 90
pjgKromosom = 18
pm = 0.7
pc = 0.5
generasi = 40
pop = initRandPop(ukuranPopulasi,pjgKromosom)

for i in range(generasi):
    i = 0
    newPop = []
    while len(newPop) < len(pop):
        decodeAll = decode(pop.copy(), pjgKromosom)
        fitness = hitungAllFitness(decodeAll.copy())
        child = crossover(pop.copy(), fitness.copy(), pc, ukuranPopulasi, pjgKromosom)
        mutasi(child[0],pm, pjgKromosom)
        mutasi(child[1],pm, pjgKromosom)
        newPop.append(child[0].copy())
        newPop.append(child[1].copy())
    pop = generalReplacement(pop.copy(), newPop.copy(), fitness.copy(), ukuranPopulasi, pjgKromosom)
print("Kromosom Terbaik: ", pop[getSurvivor(fitness)])
print("Decode Kromosom Terbaik (x,y): ", decodeAll[getSurvivor(fitness)][0]," , ", decodeAll[getSurvivor(fitness)][1])
print("Nilai maksimum: ", -1 * fitness[getSurvivor(fitness)])