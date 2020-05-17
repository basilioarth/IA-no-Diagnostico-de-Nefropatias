# IA-no-Diagnostico-de-Nefropatias
{ Estudo e implementação de algoritmos de agrupamento e de rotulação aplicados no diagnóstico de nefropatias por imagens de patologias renais }

        O projeto em questão se trata de um PIBIC do Laboratório de Inteligência Artifical, ocorrendo entre 01/08/2019 e 31/07/2020, ofertado pela
    Universidado Federal do Piauí. A ideia principal do projeto é o estudo e avaliação dos algoritmos de aprendizagem de máquina não supervisionados e algoritmos de rotulação para o desenvolvimento de processos de Descoberta de Conhecimento em Base de Dados (DCBD) em padrões em imagens de doenças renais.
        O objetivo do repositório é registrar o progresso do projeto de pesquisa. Aqui vão algumas explicações básicas sobre cada uma das pastas principais
    do repositório:

    1 - Entendendo a Base de Dados
        Uma base de dados com registros de patologias renais foi disponibilizada como base para a estruturação e aplicação prática de todo o estudo. No 
    arquivo dessa pasta analisei as especificidades dessa base de dados em busca de compreender melhor o tipo de informação com a qual trabalharia. É um arquivo basicamente "de exploração" sem muitas técnicas envolvidas.

    2 - Retirando Informações das Imagens
        Além da base de dados, um grupo de imagens (lâminas) renais foi disponibilizado para uso no projeto. Nos arquivos dessa pasta temos a aplicação 
    de técnicas de Processamento Digital de Imagens (PDI) para a retirada de algumas informações consideradas relevantes para o estudo e que, ao mesmo tempo, se adaptaram melhor para o caso específico. Em um desses arquivos, utilizo a matriz de co-ocorrência para a retirada de informações.

    3 - Transformando a Base de Dados
        Nessa etapa temos a reestruturação da base de dados já com os novos atributos (informações que foram retiradas das imagens). Essa reestruturação 
    tem o fito de corrigir algumas inconsistências e/ou erros presentes na base, assim como adaptar a base para melhor ser utilizada pelos algoritmos futuramente aplicados.

    4 - Testando Algoritmos de Clusterização
        Nessa etapa temos uma série de arquivos, cada um deles destinado a aplicação dos algoritmos escolhidos, bem como para a realização de alguns 
    testes relevantes com cada um deles.

    5 - Testes Para a Criação do Rotulador
        Essa pasta é destinada para o entendimento do funcionamento do rotulador que será utilizado no projeto. Até o memento, um aquivo foi
    criado com o objetivo de auxiliar na compreensão das especificidades do rotulador em estudo. Além disso, o próprio código do rotulador disponibilizado
    está sendo documentado. 
