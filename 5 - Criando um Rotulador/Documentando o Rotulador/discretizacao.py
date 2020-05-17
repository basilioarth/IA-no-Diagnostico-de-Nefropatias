import pandas as pd
import numpy as np

class discretizador(object):
	def __init__(self, db, vector_num_faixas, metodo, attr_cluster):
		self.db = db
		self.vector_num_faixas = vector_num_faixas
		self.metodo = metodo 
		self.attr_cluster = attr_cluster
		# atributo classe
		self.data, self.ddb, self.infor = self.discretize_db()

	def discretize_db(self):
		cluster = self.db[self.attr_cluster]
		# atributo classe
		data = self.db.drop([self.attr_cluster], axis=1)
		# base original - atributo classe
		values = data.values    
		# numpy array com o valor de cada um dos atributos restantes para cada um dos registros da base de maneira
		# sequencial. Em outras palavras: todos os valores presentes em cada linha da base.

		ddb = []
		infor = []

		for j in range(0, data.shape[1]):
			# for que percorre as colunas do df, com exceção da coluna que representa o atributo classe, pois, nesse
			# caso, data já é o df sem o atributo classe. Lembrando que range vai de 0 ao número imediatamente anterior
			# ao segundo parâmetro.
			if self.metodo is "EWD":
				disc_attb = pd.cut(values[:,j], bins = self.vector_num_faixas[j], labels = False, retbins= True)
			# 1º Parâmetro: A matriz de dentrada a ser armazenada em bin. Deve ser unidimensional. No caso, values[:,j]
			# retorna o valor de cada uma da lihas da coluna j.
			# 2º Parâmetro: Quando um inteiro, define o número de compartimentos de largura igual no intervalo da matriz
			# unidimensional passada (no caso, values[:,j]). Em outras palavras, bins + 1 definirá quantas faixas de
			# valor serão criadas.
			# 3º Parâmetro: Especifica os rótulos para os compartimentos retornados. Deve ter o mesmo comprimento que os
			# compartimentos resultantes. Se Falso, retorna apenas indicadores inteiros dos compartimentos.
			# 4º Parâmetro: Se as caixas devem ser devolvidas ou não. Útil quando caixas são fornecidas como escalares.
			# Retorna um objeto do tipo matriz que representa o respectivo bin para cada valor de values[:,j]. Em outras
			# palavras, cada um dos registros será classificado por um dos valores possíveis de serem assumidos pelo bin.
			# Se o bin for 3, por exemplo, poderá assimir os valores: 0, 1 ou 2. O tipo depende do valor dos labels.
			# Quando falso, retorna uma matriz de números inteiros.
			# Para maiores detalhes, acesse: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.cut.html
			elif self.metodo is "EFD":
				disc_attb = pd.qcut(values[:,j], self.vector_num_faixas[j], labels = False, retbins = True, duplicates = 'drop')
			#Função de discretização baseada em quantis. Discretize a variável em buckets de tamanho igual, com base na
			# classificação ou nos quantis de amostra. Por exemplo, 1000 valores para 10 quantis produziriam um objeto
			# categórico indicando associação de quantis para cada ponto de dados.
			# 1º Parâmetro: A matriz de dentrada a ser armazenada em bin. Deve ser unidimensional. No caso, values[:,j]
			# retorna o valor de cada uma da lihas da coluna j.
			# 2º Parâmetro: número de quantis
			# 3º Parâmetro: Especifica os rótulos para os compartimentos retornados. Deve ter o mesmo comprimento que os
			# compartimentos resultantes. Se Falso, retorna apenas indicadores inteiros dos compartimentos.
			# 4º Parâmetro: Se as caixas devem ser devolvidas ou não. Útil quando caixas são fornecidas como escalares.
			# 5º Parâmetro: Opcional. Se as bordas da lixeira não forem exclusivas, aumente o ValueError ou elimine não
			# exclusivos.
			# Para maiores detalhes, acesse: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html#pandas.qcut

			ddb.append(disc_attb[0])
			# estamos adicionando à lista ddb uma matriz formada de números inteiros. Tais números representam a respec-
			# tiva classificação daquele registro em bin. Exemplo: na linha 1 temos 5.3 que foi classificado como 2 (um
			# dos possíveis valoreas a serem assumidos), logo, a primeira informação dessa linha será 2.
			infor.append((data.columns[j],disc_attb[1]))
			# estamos adicionando à lista infor a coluna em questão e um array que possui os limites dos intervalos da
			# discretização realizada. Exemplo: 'sepal_length', array([4.3, 5.1, 5.8, 6.4, 7.9]). Intervalos possíveis:
			# 4.3 - 5.1; 5.1 - 5.8; 5.8 - 6.4; 6.4 - 7.9

		ddb = np.asarray(ddb, dtype = 'int32')
		# estamos convertendo a lista ddb a uma matriz. Especificamos que o tipo de dados que estarão presentes na futu-
		# matriz é int32.

		for x in range (0, data.shape[1]):
		   data.loc[:,data.columns[x]] = [y[x] for y in ddb.T]
		   # cada uma das linhas da coluna de índice x da base está recebendo o correspondente valor da linha da matriz
		   # transposta de ddb.
		data[self.attr_cluster] = cluster
		# Adicionamos à base, agora transformada, o atributo classe que foi isolado inicialmente nesse código.
		
		return ddb,data, infor
		# Está retornando a base de dados discretizada/base original em bin (ddb), a transposta da base discretizada com
		# o atirbuto cluster (data) e a lista com o atributo e as respectivas faixas de valor assumidas nesse atributo
		# após a discretização (infor).
	