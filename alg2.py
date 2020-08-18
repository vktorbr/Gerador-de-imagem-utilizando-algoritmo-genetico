from PIL import Image, ImageDraw, ImageChops
import random
import matplotlib.pyplot as plt
from numpy import mean, std

tamanho_populacao = 100
tamanho_individuo = 200
prob_mutacao = 0.05

imagem_objetivo = Image.open('nome_arquivo.png').convert('RGB')
largura_imagem = imagem_objetivo.size[0]
altura_imagem = imagem_objetivo.size[1]

#classe gene - cada gene determina o RGB e o vertices de um triangulo
class Gene:
    def __init__(self, invisivel=False):
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)

        if invisivel:
            self.a = 0
        else:
            self.a = 50

        self.v1 = random.uniform(0, largura_imagem), random.uniform(0, altura_imagem)
        self.v2 = random.uniform(0, largura_imagem), random.uniform(0, altura_imagem)
        self.v3 = random.uniform(0, largura_imagem), random.uniform(0, altura_imagem)

#classe individuo - cada individuo representa uma imagem
class Individuo:

    def __init__(self, pai1=None, pai2=None):

        self.genes = []

        # cria um novo individuo com genes aleatorios
        if pai1 is None or pai2 is None:
            for i in range(tamanho_individuo):
                self.genes.append(Gene(invisivel=True))

        #cria um novo individuo com genes herdados dos pais e pode ter mutacao
        else:
            #genes dos individuos sao escolhidos aleatoriamente entre os pais
            for i in range(tamanho_individuo):
                if random.randint(0, 1) == 1:
                    self.genes.append(pai1.genes[i])
                else:
                    self.genes.append(pai2.genes[i])
            #Chance de ocorrer mutacao
            self.mutacao()
        self.fitness = self.get_fitness()

    #gera a imagem que um individuo representa
    def get_imagem(self):
        imagem = Image.new('RGB', (largura_imagem, altura_imagem))
        desenho = ImageDraw.Draw(imagem, 'RGBA')
        for i in range(tamanho_individuo):
            vertices = (self.genes[i].v1, self.genes[i].v2, self.genes[i].v3)
            cores = (self.genes[i].r, self.genes[i].g, self.genes[i].b, self.genes[i].a)
            desenho.polygon(vertices, cores)
        return imagem

    #fitness ? calculado pela diferen?a de pixels diferentes por o numero possivel
    def get_fitness(self):
        diferenca = ImageChops.difference(self.get_imagem(), imagem_objetivo)
        data = diferenca.getdata()
        quant_pixels_diferentes = 1.0 * sum(map(sum, data))
        max_pixels = altura_imagem * largura_imagem * 3 * 255
        erro = quant_pixels_diferentes / max_pixels
        fitness = 1 / (1 + erro)
        return fitness

    #mutacao ? feita para cada gene do individuo com chance de 5%
    #gene do individuo recebe um gene aleatorio
    def mutacao(self):
        for i in range(tamanho_individuo):
            if random.uniform(0,1) <= prob_mutacao:
                self.genes[i] = Gene()

class Populacao:

    def __init__(self):
        self.individuos = []

        for i in range(tamanho_populacao):
            self.individuos.append(Individuo())
        #ordena os individuos pelo fitness em ordem decrescente
        self.individuos.sort(key=lambda x: x.fitness, reverse=True)

    def lista_fitness(self):
        lista_fitness = []
        for j in range(tamanho_populacao):
            lista_fitness.append(self.individuos[j].fitness)
        return lista_fitness

    def get_melhor_fitness(self):
        return self.individuos[0]

    def get_pior_fitness(self):
        return self.individuos[tamanho_populacao - 1]

    def recombinacao(self, i, pai1, pai2):
        self.individuos[i] = Individuo(pai1, pai2)

    # dois pais diferentes sao escolhidos dos 5 melhores fitness
    def selecao_pais(self):
        pais_selecionados = 5
        for i in range(pais_selecionados, tamanho_populacao):
            dois_pais = random.sample(range(0, pais_selecionados), 2)
            pai1 = self.individuos[dois_pais[0]]
            pai2 = self.individuos[dois_pais[1]]
            self.recombinacao(i, pai1, pai2)
        self.individuos.sort(key=lambda x: x.fitness, reverse=True)


pop = Populacao()
geracoes = []
melhores = []
piores = []
media = []
desvio_padrao = []

for i in range(1000):
    geracao = i + 1
    geracoes.append(geracao)

    pop.selecao_pais()
    melhor = pop.get_melhor_fitness()
    melhores.append(melhor.fitness)

    pior = pop.get_pior_fitness()
    piores.append(pior.fitness)

    media.append(mean(pop.lista_fitness()))
    desvio_padrao.append(std(pop.lista_fitness()))

    print('GERACAO:', geracao, '|', 'MELHOR FITNESS:', melhor.fitness, '|', 'PIOR:', pior.fitness)

    # a cada 100 geracoes ? salva o melhor individuo
    if (geracao % 100 == 0):
        melhor.get_imagem().save(str(geracao) + '_geracao ' + str(round(melhor.fitness, 2)) +'_fitness' + '.png')

#plotacao
fig, ax = plt.subplots()
ax.set_title('Evolucao Fitness')
ax.plot(geracoes, melhores, color='green', label='Melhor')
ax.plot(geracoes, piores, color='red', label='Pior')
ax.plot(geracoes, media, color='blue', label='Media')
ax.plot(geracoes, desvio_padrao, color='orange', label='Desvio Padrao')

plt.ylabel('Fitness')
plt.xlabel('Geracoes')
plt.legend()
plt.savefig('grafico.png')
plt.show()


