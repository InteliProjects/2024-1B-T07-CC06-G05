# Complexidade e corretude do algoritmo

## Sumário

- [1. Introdução Ant Colony Optmization](#c1)
- [2. Análise de Complexidade Pior e Melhor Caso](#c2)
- [3. Análise Matemática de Complexidade](#c3)
- [3.1. Complexidade de tempo](#c31)
- [3.2. Complexidade de espaço](#c32)
- [4. Analise de Corretude](#c4)
- [4.1. Invariante do Laço](#c41)
- [4.2. Prova por indução](#c42)
- [4.2.1. Base da indução](#c421)
- [4.2.2. Hipotese de indução](#c422)
- [4.2.3. Passo da indução](#c423)
- [Referências](#r)

## <a name="c1"></a>1. Introdução Ant Colony Optmization

<div align="justify">

&emsp;O algoritmo implementado pelo grupo O.V.O para solucionar o problema da AEGEA foi o *Ant Colony Optmization* (ACO). Esse algoritmo é baseado no comportamento de formigas reais, que liberam uma espécie de feromônio no caminho que passam para que outras formigas encontrem o caminho até a comida e voltem ao formigueiro. Nesse sentido, o algoritmo localiza as soluções movendo-se através de um espaço de parâmetros que representa todas as soluções possíveis. A equipe utilizou como base o artigo "*Ant Colony Optimization: An Advanced Approach to the Traveling Salesman Problem*" -  e o vídeo "*Ant colony optimization algorithm*" - Simulife Hub para implementar o algoritmo e construir sua análise de complexidade.

&emsp;Primeiramente, uma colônia de *k* formigas é criada (sendo *k* também o número de pontos que devem ser visitados pelos leituristas), um ponto inicial é escolhido arbitrariamente e uma melhor solução inicial é colocada para ter um custo inifito. Em seguida, é determinado o número de iterações que o algoritmo deverá ter que, para fins desse projeto, foi decidido que 1000 iterações traz resultados aceitáveis e condizentes, como demonstado nos testes realizados.

&emsp;Nesse sentido, em cada iteração, cada formiga da colônia começa a passar por um caminho, a partir do ponto inicial definido, nunca visitando um ponto em que já esteve. Elas escolhem o ponto que vão de acordo com uma heurítica probabilística dos feromônios que sentem no caminho, até que não tenham mais pontos para serem visitados. Assim, a probabilidade *P* da formiga ir para o ponto *v* a partir do ponto *u* é:

$$  P_{u, v} = \dfrac{(\tau_{u,v})^\alpha \cdot (\eta_{u,v})^\beta}{\sum_{vi \in v}((\tau_{u,v})^\alpha \cdot (\eta_{u,v})^\beta)}  $$

&emsp;Em que $ \tau_{u,v} $ é a quantidade de feromônio entre o ponto *u* e o ponto *v* e $ \eta_{u,v} $ é equivalente a $ \dfrac{1}{d_{u,v} + 1} $ . Assim, $ \alpha $ é um parâmetro que controla a influência dos feromônios na probabilidade e $ \beta $ é um parâmetro que controla a influência dos custos da distância entre os dois pontos na probabilidade. Para fins desse projeto, foi decidido que os valores de $ \alpha $ e $ \beta $ seriam respectivamente 1 e 2 para priorizar a distância entre os pontos.

&emsp;Nesse sentido, para cada um desses caminhos encontrados por cada formiga, feromônios são depositados nos vértices. Dessa forma, a quantidade que é depositada entre os pontos *u* e *v* é calculada da seguinte forma:

$$ \tau_{u, vi} = (1 - \rho)\tau_{u, vi} + \sum_k \Delta \tau_{k,u,vi} $$ 

&emsp;Em que $ \tau_{u, vi} $ é a quantidade de feromônio entre o pontos *u* e *vi*, $ \rho \in $ (0, 1) é um parâmetro que controla o quanto dos feromônios são evaporados. Para fins desse projeto, o grupo escolheu utilizar um valor de 0,3. O valor de $\Delta \tau_{k,u,vi} $ em que seu valor é 0 caso a formiga *k* não passe entre *u* e *vi*, e caso passe, é calculado como $ \dfrac{Q}{L_k} $ onde *Q* é a quantidade de feromônio depositada, que é calculada como $\dfrac{100}{d}$ no qual *d* é distância percorrida pela formiga, e $L_k$ é o custo do caminho da formiga *k*.

&emsp;Por fim, o caminho com o menor custo é comparado com a melhor solução até agora e, se for menor, a melhor solução é atualizada para se tornar essa solução encontrada.

## <a name="c2"></a>2. Análise de Complexidade Pior e Melhor Caso

&emsp;No algoritmo, como o seu critério de parada é o número de iterações passada por parâmetro, mesmo que o melhor caminho seja encontrado na primeira iteração, ele vai continuar iterando o número de vezes pré-determinado. Dessa forma, não há diferença de complexidade entre o pior e o melhor caso.

## <a name="c3"></a>3. Análise Matemática de Complexidade

&emsp;A análise matemática da complexidade nos permite avaliar o quão rápido um programa executa suas tarefas, quando se trata de complexidade de tempo, e o quanto ele exige de memória, ou seja, complexidade de espaço. Dessa forma, é importante avaliar essas duas complexidades para o Ant Colony Optmization na notação O.

### <a name="c31"></a>3.1. Complexidade de tempo

&emsp;Nós iniciamos o algoritmo calculando os caminhos por meio de dois *loops for*, que dependem do número de iterações que é constante no valor de 1000 e do número *k* de formigas. Dentro deles, há um terceiro *loop for* que percorre todos os valores de *Path* que depende do número *k* de formigas também. 

&emsp;Em seguida, mas ainda dentro do primeiro *loop for*, há mais dois *loops for* para o cálculo de feromônios, que possui complexidade de tempo de $k^2$ por percorrer a matriz de adjacência dos vértices. Depois, na construção de melhor rota, o algoritmo percorre toda a matriz de adjacência novamente, apresentando complexidade de $k^2$.

&emsp;Assim, conclui-se que a complexidade de tempo total é de O($k^2$), uma vez que o número de iterações é constante.

### <a name="c32"></a>3.2. Complexidade de espaço

&emsp;Nós iniciamos o algoritmo com um *array* unidimensional de *boolean* para o cálculo de pontos e caminhos visitados, que como tem o tamanho de número de formigas, possuindo complexidade *k*, bem como o *array* de *Path* de tamanho *k*.

&emsp;Em seguida, há a matriz de adjacência dos vértices, que possui complexidade $k^2$. Depois, a melhor rota encontrada é armazenada do *array bestRoute* que possui tamanho *k*.

&emsp;Assim, conclui-se que a complexidade de espaço total, uma vez que a quantidade de formigas e de vértices é a mesma, é de O($k^2$) também.

## <a name="c4"></a>4. Analise de Corretude

&emsp;&emsp;A análise de corretude consiste em uma análise matemática que verifica se um algoritmo está correto. Sendo assim, para qualquer entrada, ele manterá o seu funcionamento e devolverá uma saída coerente. Para realizar esta análise, encontramos um invariante do laço, isto é, uma característica do nosso algoritmo que se mantém constante em todas as iterações, e precisamos provar matematicamente, por indução matemática, que esta característica é verdadeira e constante. Dentre os algoritmos testados pelo grupo, escolhemos realizar a análise de corretude do algoritmo AntColony.

### <a name="c41"></a>4.1. Invariante do Laço

&emsp;&emsp;Dado que o seu funcionamento se baseia na dinâmica de feromonios, onde existe um reforço positivo para caminhos que levam a uma boa solução, foi encontrada a invariante abaixo:

&emsp;&emsp;Invariante do laço: O valor esperado dos feromonios numa iteração t, $\mathbb{E}[\tau_{ij}(t)]$, depende da quantidade inicial de feromonios, da contribuição de cada formiga até a iterção t e da taxa de evaporação. Matematicamente isso pode ser expresso como:

 $$ \mathbb{E}[\tau_{ij}(t)] = (1- \rho)^t\tau_{ij}(0) + \sum_{k=0}^{t-1}\sum_{s=1}^{m}((1-\rho)^{t-1-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s})$$

 Onde:
 - $\tau_{ij}(0)$ é a quantidade inicial de feromonios
 - $\rho$ é a taxa de evaporação
 - $Q$  é uma constante que diz o acrecimo de feromonios
 - $\delta_{ij}^s(k)$ é uma variavel que indica se o caminho ij estava presente na solução da formiga s na iteração k, valendo 1 se sim, 0 caso contrario.
 - $L_s$  é o custo(distancia) da solução encontrada pela formiga s
 - m é o numero de formigas
 - t é o número de iterações

 &emsp;&emsp; Vale ressaltar que o valor esperado, ou expectativa, é usado porque estamos tratando de um algoritmo probabilístico. Isto é, cada formiga pode escolher caminhos diferentes com base nas probabilidades, e isso influencia na atualização dos feromônios. O uso da expectativa nos dá uma tendência que nos ajuda a compreender se as atualizações, em sua média, convergem para um reforço ou não.

 ### <a name="c42"></a>4.2. Prova por indução

 #### <a name="c421"></a>4.2.1. Base da indução
 &emsp;&emsp; Em t =0, temos uma configuração inicial de feromonios, sendo assim:

$$ \mathbb{E}[\tau_{ij}(0)] = \tau_{ij}(0)$$

#### <a name="c422"></a> 4.2.2. Hipotese de indução

&emsp;&emsp;Para t=t temmos que:
$$\mathbb{E}[\tau_{ij}(t)] = (1- \rho)^t\tau_{ij}(0) + \sum_{k=0}^{t-1}\sum_{s=1}^{m}((1-\rho)^{t-1-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s})$$

&emsp;&emsp;É possível perceber que o primeiro termo é a quantidade de feromônios iniciais decrementada até o período t. O segundo termo diz respeito ao acréscimo de reforço na quantidade de feromônios nos caminhos utilizados até a iteração t. Este acréscimo também tem um fator de evaporação para os acréscimos de iterações anteriores, chegando até a iteração atual, cuja evaporação é inexistente, e portanto $(1- \rho)^{t-1-(t-1)} = (1- \rho)^{t-1-t+1} = (1-\rho)^0=1$.

#### <a name="c423"></a> 4.2.3. Passo da indução
 &emsp;&emsp; precisamos provar que para t+1, a hipotese de indução permanece valida, ou seja, este reforço se mantenha.Para isso iremos partir da formula da atualização dos feromônios:

 $$\tau_{ij}(t+1) = (1-\rho)\cdot \tau_{ij}(t) + \sum_{s = 1}^m \Delta \tau_{ij}^s(t) $$
 
&emsp;&emsp;  Tiramos o valor esperado de ambos os lados
$$\mathbb{E}[\tau_{ij}(t+1)]=  (1-\rho)\cdot \mathbb{E}[\tau_{ij}(t)] + \sum_{s = 1}^m \mathbb{E}[\Delta \tau_{ij}^s(t)]$$

&emsp;&emsp; sabemos o valor de $\mathbb{E}[\tau_{ij}(t)]$ pela hipotese de indução, assim substituimos:

$$\mathbb{E}[\tau_{ij}(t+1)]=  (1-\rho)\cdot((1- \rho)^t\tau_{ij}(0) + \sum_{k=0}^{t-1}\sum_{s=1}^{m}((1-\rho)^{t-1-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s})) + \sum_{s = 1}^m \mathbb{E}[\Delta \tau_{ij}^s(t)]$$

$$\mathbb{E}[\tau_{ij}(t+1)]=  (1- \rho)^{t+1}\tau_{ij}(0) + \sum_{k=0}^{t-1}\sum_{s=1}^{m}((1-\rho)^{t-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s}) + \sum_{s = 1}^m \mathbb{E}[\Delta \tau_{ij}^s(t)]$$

&emsp;&emsp; Se $\mathbb{E}[\Delta \tau_{ij}^s(t)] =\frac{Q\delta_{ij}^s(k)}{L_s}$ temos:

$$\mathbb{E}[\tau_{ij}(t+1)]=  (1- \rho)^{t+1}\tau_{ij}(0) + \sum_{k=0}^{t-1}\sum_{s=1}^{m}((1-\rho)^{t-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s}) + \sum_{s = 1}^m (\frac{Q\delta_{ij}^s(k)}{L_s} )$$

&emsp;&emsp; E finalmente:

$$\mathbb{E}[\tau_{ij}(t+1)]=  (1- \rho)^{t+1}\tau_{ij}(0) + \sum_{k=0}^{t}\sum_{s=1}^{m}((1-\rho)^{t-k} \cdot \frac{Q\delta_{ij}^s(k)}{L_s}) $$

&emsp;&emsp; Além de provar que existe um reforço positivo, podemos dizer que a qualidade das soluções tem uma tendência a aumentar, visto que para um L menor, o reforço é mais forte e para aquelas arestas que levam a um L menor, ou não são escolhidas, a evaporação vai  reduzindo as chances de escolha delas, garantindo asssim uma convergencia a uma boa solução.
  
  
## <a name="r"></a> Referências

MAY, B.; GREER, E.; HOLT, G.; VARGAS, K.; Ant Colony Optimization: An Advanced Approach to the Traveling Salesman Problem - Brigham Young University Provo, UT, USA. Acesso em: 07 jun. 2024.

Simulife Hub. Ant colony optimization algorithm. 1 vídeo (19 min). Simulife Hub, 2023. Disponível em: https://www.youtube.com/watch?v=u7bQomllcJw&t=2s. Acesso em: 08 jun. 2024.

</div>
