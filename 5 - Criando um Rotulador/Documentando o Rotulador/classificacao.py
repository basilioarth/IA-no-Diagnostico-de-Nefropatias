import numpy as np
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split

class classificador(object):
	def __init__(self, metodo, data, perc_trein, folds):
		self.data = data
		self.metodo = metodo
		self.perc_test = (100-perc_trein)/100
		self.folds = folds
		self.acuracia = self.classificar()	

	def classificar(self):
		acuracia = [0]*self.data.shape[1]
		# acuracia é uma lista cuja quantidade de elementos é igual à quantidade de colunas do dataframe (data.shape[1])
		# e que possui, até o momento, todos os seus elementos sendo 0 (o número inteiro 0).
		for i in range(self.folds):
			# para cada uma das camadas da MLPC:
			for j in range(self.data.shape[1]):
				# para cada uma das colunas do dataframe já sem o atributo classe:
				x_train, x_test, y_train, y_test = self.trainTest(self.data, j)
				# temos a base particionada em treino e teste levando em consideração o atributo classe a coluna em
				# questão (representada pelo número assumido por j no momento).
				y_train = np.asarray(y_train, dtype="|S6")
				# convertemos y_train a uma matriz, especificando que o tipo de dado encontrado em y_train é string
				y_test = np.asarray(y_test, dtype="|S6")
				# convertemos y_test a uma matriz, especificando que o tipo de dado encontrado em y_test é string
				clf = self.metodo
				
				if x_train.size == 0:
					# caso não há elementos para treino, a acuracia correspondente àquela coluna tem  0 adicionado ao
					# seu valos atual
					acuracia[j] += 0
				else:
					# caso contrário, é calculada a acurácia pelo método escolhido (MLPClassifier) e o valor retornado
					# é adicionado ao valor que é assumido na posição da lista acuracia que corresponde a essa coluna
					# (: acuracia[j]).
					clf.fit(x_train, y_train)
					acuracia[j] += clf.score(x_test, y_test)
		
		acuracia = [i/self.folds for i in acuracia]
		# após o fim do cálculo da acurácia para cada uma das colunas do dataframe já sem o atributo classe, temos em
		# cada uma das posições da lista acuracia a soma do score obtido para essa posição em cada uma das camadas da
		# rede neural. Para termos um valor médio, dividimos o valor de cada uma dessas posições pelo número total de
		# camadas da rede neural.
		resultado = list(zip(self.data.columns, acuracia))
		# A função zip () pega iteráveis (pode ser zero ou mais), agrega-os em uma tupla e a retorna. Colocando-o dentro
		# do método list, retornamos uma lista onde cada elemento é uma tupla. O primeiro elemento da tupla é o nome da
		# coluna e o segundo elemento da tupla é a sua respectiva acurácia.
		return resultado

	def trainTest(self, data, attr):
		# Vale lembrar que X representa todas as colunas que serão utilizadas para predizer valores da coluna Y.
		Y = data.loc[:,data.columns[attr]].values
		# um ndarray com os valores assumidos por cada um dos registros dessa coluna do dataframe.
		X = data.drop(data.columns[attr], axis=1).values
		# um ndarray com os valores assumidos por cada um dos registros das colunas restantes do dataframe.
		x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=self.perc_test)
		# particionamos a base em treino e teste.
		return x_train, x_test, y_train, y_test

def classifica_bd(grupos, attr_cluster, porc_trein, folds):
	result = []
	# grupos é uma lista com os dados do bd discretizado fragmentados de acordo com o atributo attr_cluster.
	for grupo in grupos:
		# para cada um dos grupos:
		data = grupo.drop([attr_cluster], axis=1)
		# elementos do grupo atual sem o atributo classe
		clt = grupo[attr_cluster].unique()
		# valor assumido pelo atributo classe do grupo atual
		classif = classificador(mlp(max_iter=2000), data, porc_trein, folds)
		# instanciamos um objeto da classe classificador.
		result.append((clt,classif.acuracia))
		# adicionamos à lista result o valor assumido pelo atributo classe do grupo em questão (clt) e uma lista composta
		# por tuplas, onde o primeiro elemento da tupla é uma das colunas do db (com execeção do atributo classe, que já
		# foi retirado) e o segundo elemento é a acurácia dessa coluna (classif.acuracia).
	return result
	# retorna uma lista de tuplas que possui o conteúdo explicado pelo comentário imediatamente acima.