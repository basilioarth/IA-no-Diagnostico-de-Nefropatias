from collections import Counter

class rotulador(object):
	def __init__ (self, cluster, holdout_val,V):
		self.medias = [(i, acuracia*100) for i, acuracia in holdout_val]
		self.medias.sort(key=lambda x: x[1], reverse=True)
		self.min = self.medias[0][1]-V
		self.titulos = cluster.columns.values.tolist()
		self.data = cluster
	
	def rotular_bd_discretizada(self, infor, cluster_disc):
		rotulos = []
		for i in range(self.data.shape[1]):
			if self.medias[i][1] >= self.min: 
				attr = self.medias[i][0]
				info = [i[1] for i in infor if i[0]==attr][0]
				most_comun_value = cluster_disc[attr].mode()[0]
				rotulo = (attr,round(info[most_comun_value],2), round(info[most_comun_value+1],2))
				rotulos.append(rotulo)
		return rotulos
		
def rotular( grupos, grupos_disc, attr_cluster, classificacao_infor, V, discretizacao_infor):
	rotulo = []
	if discretizacao_infor:
		for grupo in grupos_disc:
			clt = grupo[attr_cluster].unique()[0]
			class_info = [i[1] for i in classificacao_infor if i[0]==clt][0]
			rotulador_ = rotulador(grupo.drop([attr_cluster], axis=1), class_info, V)
			rotulo.append((clt, rotulador_.rotular_bd_discretizada(discretizacao_infor, grupo.drop([attr_cluster], axis=1))))
	return rotulo
