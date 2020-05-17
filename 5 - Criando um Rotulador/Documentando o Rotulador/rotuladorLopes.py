import man_dados
from discretizacao import discretizador as disc
from classificacao import classifica_bd as clas
from rotulacao import rotular as rotulador 
from sklearn import metrics

class Rotulador(object):
	def __init__ (self, bd, attr_cluster_name, discre_method, bins, per_trein, V, folds):
		self.bd = bd
		self.frames_originais = man_dados.group_separator(bd, attr_cluster_name)
		# recebe uma lista com os dados do bd original fragmentados de acordo com o atributo attr_cluster_name. No caso,
		# o atributo/coluna 'classe'.

		discretizacao = disc(bd, bins, discre_method, attr_cluster_name)
		self.base_discretizada = discretizacao.ddb
		# recebemos a base discretizada
		self.infor = discretizacao.infor
		# uma lista contendo todas as colunas e todas as respectivas possíveis faixas de valor a serem assumidas como
		# registro dessa coluna
		self.frames_discretizados = man_dados.group_separator(self.base_discretizada, attr_cluster_name)
		# recebe uma lista com os dados do bd discretizado fragmentados de acordo com o atributo attr_cluster_name. No
		# caso, o atributo/coluna 'classe'.

		self.classificacao = clas(self.frames_discretizados, attr_cluster_name, per_trein, folds)
		# é uma lista de tuplas. O primeiro elemento de cada uma das tuplas é o valor assumido pelo atributo classe em
		# um determinado grupo (um dos grupos presentes em frames_discretizados). O segundo elemento é também uma lista
		# de tuplas, onde o primeiro elemento da tupla é uma das colunas do db (com execeção do atributo classe, que já
		# foi retirado) e o segundo elemento é a acurácia dessa coluna (classif.acuracia).
		# em outras palavras temos uma lista que informa um valor assumido pelo atributo classe e as correspondentes
		# acurácias assumidas pelas outras colunas da dataframe quanto a esse valor do atributo classe.

		self.rotulo = rotulador(self.frames_originais, self.frames_discretizados, attr_cluster_name, self.classificacao, V, self.infor)

dataset = man_dados.read_csv('./databases/iris.csv')
# dataset = man_dados.read_csv(r'C:\Users\LENOVO\Desktop\UFPI\LINA\PIBIC 2019-2020 (01.08.2019 a 31.07.2020)\Bases\Bases Numéricas\base_limpa_numerica_1atributo.csv')

# Importamos a base de dados desejada

rotulo = Rotulador(dataset, 'classe', 'EFD', [3,3,3,3], 60, 10, 10).rotulo
# rotulo = Rotulador(dataset, 'Diagnóstico', 'EFD', [3,3,3,3], 60, 10, 10).rotulo
# Rotulamos os grupos formados
print('Rótulo: ', rotulo)
# Printamos os rótulos formados.

IS = metrics.silhouette_score(dataset.drop(['classe'], axis=1), dataset['classe'])
BD = metrics.davies_bouldin_score(dataset.drop(['classe'], axis=1), dataset['classe'])
# Calculamos as medidas de acertividade
print('Silhouette Score: ', IS)
print('Davies Bouldin Score: ', BD)

'''
print('\n')
for clt in dataset['classe'].unique():
	regras = [i[1] for i in rotulo if i[0] == clt][0]
	for regra in regras:
		dataset.drop(dataset[(~(dataset[regra[0]]>= regra[1]) & (dataset[regra[0]]<= regra[2])) & (dataset['classe'] == clt)].index, axis=0, inplace=True)
IS = metrics.silhouette_score(dataset.drop(['classe'], axis=1), dataset['classe'])
BD = metrics.davies_bouldin_score(dataset.drop(['classe'], axis=1), dataset['classe'])

print('Scores após uma alteração que eu ainda não entendi: ')
print('Silhouette Score: ', IS)
print('Davies Bouldin Score: ', BD)
'''