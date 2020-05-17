
class rotulador(object):
	def __init__ (self, cluster, holdout_val,V):
		self.medias = [(i, acuracia*100) for i, acuracia in holdout_val]
		# é uma lista de tuplas em que o primeiro elemento de cada tupla é uma das colunas do dataframe e o segundo ele-
		# mento é a sua respectiva acurácia.
		self.medias.sort(key=lambda x: x[1], reverse=True)
		# método que ordena uma lista de forma crescente (reverse = False) ou decrescente (reverse = True). O parâmetro
		# key serve para designar uma função que será o critério de ordenação. No caso, estamos especificando através
		# da função lamba que o o segundo elemento da lista de tuplas é o que deve ser analizado para a ordenação. Esse
		# segundo elemento trata-se justamente da acurácia daquela coluna para o valor assumido pelo atributo classe
		# no grupo específico.
		self.min = self.medias[0][1]-V
		# valor mínimo aceitável para que o valor de um atributo qualquer seja considerado como algo que caracteriza os
		# elementos daquele grupo (ou seja, para que esse valor seja considerado como um rótulo). No caso, especificamos
		# o valor mínimo subtraindo do valor da maior acurácia o valor de V (no caso, é 10).
		self.titulos = cluster.columns.values.tolist()
		# convertemos uma Serie em uma Lista. No caso, nossa lista será formada pelo nome das colunas/atributos do nosso
		# dataframe (com exceção, como já sabemos, do atributo classe).
		self.data = cluster
		# nosso dataframe completo (sem o atributo classe).
	
	def rotular_bd_discretizada(self, infor, cluster_disc):
		rotulos = []
		for i in range(self.data.shape[1]):
			# para cada uma das colunas do dataframe
			if self.medias[i][1] >= self.min:
				# se a acurácia for maior ou igual ao limite mínimo estipulado
				attr = self.medias[i][0]
				# nome da coluna cuja a acurácia é minimamente aceitável.
				info = [i[1] for i in infor if i[0]==attr][0]
				# buscamos na lista que possui todas as colunas e as respectivas faixas de valor a serem assumidas por
				# aquela coluna pela coluna que coincide com a coluna em questão. Da lista de faixas de valor a serem
				# assumidos, pegamos o primeiro valor.
				most_comun_value = cluster_disc[attr].mode()[0]
				# selecionamos, da lista de todas as colunas e suas respectivas faixas de valor, a coluna que coincide
				# com a coluna em questão. Dos possíveis valores existentes, calculamos a moda (o valor que mais aparece).
				rotulo = (attr,round(info[most_comun_value],2), round(info[most_comun_value+1],2))
				# estamos atribuindo à lista rotula uma tupla com três elementos. O primeiro elemento é o nome da coluna
				# que assume acurácia maior ou igual à minimamente aceitável. Os outros dois valores são os valores mais
				# comuns assumidos por essa coluna.
				rotulos.append(rotulo)
		return rotulos
		
def rotular( grupos, grupos_disc, attr_cluster, classificacao_infor, V, discretizacao_infor):
	rotulo = []
	if discretizacao_infor:
		# se houver alguma informação de discretização
		for grupo in grupos_disc:
			# para cada um dos grupos formados pelos dados discretizados
			clt = grupo[attr_cluster].unique()[0]
			# valor assumido pelo atributo classe daquele grupo
			class_info = [i[1] for i in classificacao_infor if i[0]==clt][0]
			# o for serve paraa percorremos todos os elementos da lista de classificação em busca daquele cujo o primeiro
			# elemento da tupla é igual ao valor assumido pelo atributo classe do grupo em questão, pois é em relação a
			# esse grupo que queremos fazer a rotulação. i[0] representa o primeiro elemento da lista de tuplas classifi-
			# cacao_infor. Caso encontremos o grupo que estamos procurando, pegamos o segundo elemento da tupla (i[1])
			# que também é uma lista de tuplas e, após isso, selecionamos o primeiro elemento dessa lista ( [i[1]][0] )
			# que é uma tupla que tem como primeiro elemento uma das outras colunas do dataframe e o segundo elemento a
			# sua respectiva acurácia.
			# OBS: ainda há duvidas quanto ao uso do [0] final.
			rotulador_ = rotulador(grupo.drop([attr_cluster], axis=1), class_info, V)
			rotulo.append((clt, rotulador_.rotular_bd_discretizada(discretizacao_infor, grupo.drop([attr_cluster], axis=1))))
			# estamos adicionando à lista rotulo o valor assimido pelo atributo classe nesse grupo em específico e uma
			# lista com todos os outos atriubtos (outras colunas) que possuem acurácia maior ou igual ao limite mínimo
			# aceitável e os seus respectivos valores mais comuns.
	return rotulo
