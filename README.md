# Sistemas-operacionais-T1

#### Alunos: Willian Weyh, Davi Nunes, Guilherme S. Silva, Eduardo Castro
Repositório dedicado à implementação do Trabalho 1 da disciplina de Sistemas Operacionais, ministrada pelo professor 
Fillipo Novo Mor, na Pontifícia Universidade Católica do Rio Grande do Sul (PUCRS), no semestre 2026/02.

## Sumário

- [Objetivo do trabalho](#objetivo-do-trabalho)
- [Como rodar o programa](#como-rodar-o-programa)
    - [Passo 1 - Compilar o projeto](#passo-1---compilar-o-projeto)
    - [Passo 2 - Executar threads sem sincronização (T1)](#passo-2---executar-threads-sem-sincronização-t1)
    - [Passo 3 - Threads com mutex (T2)](#passo-3---threads-com-mutex-t2)
    - [Passo 4 - Processos sem sincronização (P1)](#passo-4---processos-sem-sincronização-p1)
    - [Passo 5 - Processos com semáforo (P2)](#passo-5---processos-com-semáforo-p2)
    - [Para medir tempo de execução](#para-medir-tempo-de-execução)
    - [Removendo classes de execução](#clean-remover-executaveis)
- [Ambiente e Hardware](#ambiente-e-hardware)
- [Tabela de tempo de execução](#tabela-de-tempo-de-execução)
- [Análise de Corrupção](#análise-de-corrupção)
- [Análise do gráfico](#análise-do-gráfico)
- [Observações técnicas](#observações-técnicas)
- [Conclusão](#conclusão)
- [Evidências](#evidências)
- [Links externos](#links)

## Objetivo do trabalho
O objetivo deste trabalho é comparar o comportamento de Threads (POSIX pthreads) e Processos (fork) em relação a 
três aspectos principais: overhead de criação, custo de comunicação e consistência de dados. Para isso, foi implementado 
um contador compartilhado que deve atingir o valor de 1 bilhão, distribuindo o trabalho entre múltiplas unidades de 
execução (N = 2, 4 e 8), com e sem mecanismos de sincronização.

## Como rodar o programa

### Passo 1 - Compilar o projeto

```bash
make all
```

### Passo 2 - Executar threads sem sincronização (T1)

```bash
make runT1 N=2
make runT1 N=4
make runT1 N=8
```

### Passo 3 - Threads com mutex (T2)

```bash
make runT2 N=2
make runT2 N=4
make runT2 N=8
```

### Passo 4 - Processos sem sincronização (P1)

```bash
make runP1 N=2
make runP1 N=4
make runP1 N=8
```

### Passo 5 - Processos com semáforo (P2)

```bash
make runP2 N=2
make runP2 N=4
make runP2 N=8
```

### Para medir tempo de execução
```bash
time make runT1 N=2
time make runT1 N=4
time make runT1 N=8

time make runT2 N=2
time make runT2 N=4
time make runT2 N=8

time make runP1 N=2
time make runP1 N=4
time make runP1 N=8

time make runP2 N=2
time make runP2 N=4
time make runP2 N=8
```
### Clean (Remover executaveis)
```bash
make clean
```

## Ambiente e Hardware
Hardware utilizado em x86
![x86_data](Assets/x86_data.jpeg)

Hardware ARM
```
sysctl -a | grep hw.ncpu
hw.ncpu: 12
```
![arm_data](Assets/ARM_data.png)

Para este trabalho foram criadas 4 classe sendo elas

``` c
threads_no_mutex.c -> Nosso T1, programa com threads sem mutex
threads_mutex.c -> Nosso T2, programa com threads aplicando o mutex

process_free.c -> Nosso P1, programa com processos sem utilizar semáforos
process_sem.c -> Nosso P2, programa com processos e utilizando dos semáforos

```

## Tabela de tempo de execução

Para a construção do gráfico de escalabilidade, os experimentos foram executados em dois ambientes distintos, 
correspondentes às arquiteturas x86 e ARM. Em cada ambiente, cada experimento foi executado três vezes para cada valor 
de N (2, 4 e 8), sendo apresentados os tempos médios dessas execuções. Essa abordagem foi adotada para reduzir variações 
ocasionais causadas pelo sistema operacional, como escalonamento de processos e interferência de outras tarefas, 
garantindo maior confiabilidade, consistência dos resultados e permitindo uma comparação mais precisa entre as diferentes 
arquiteturas.

### Arquitetura Arm
| N | T1 - Threads (sem mutex) | T2 - Threads (mutex) | P1 - Processos (sem sync) | P2 - Processos (semáforo) |
|--|---------------------------|----------------------|----------------------------|----------------------------|
| 2 | 0.736s | 8.077s  | 0.732s | 51m07.70s |
| 4 | 0.315s | 16.632s | 0.340s | 38m43.00s |
| 8 | 0.187s | 15.163s | 0.212s | 54m52.94s |

## Arquitetura (x86)

| N | T1 - Threads (sem mutex) | T2 - Threads (mutex) | P1 - Processos (sem sync) | P2 - Processos (semáforo) |
|--|---------------------------|----------------------|----------------------------|----------------------------|
| 2 | 1.083s | 38.671s | 0.917s | 1m21.560s |
| 4 | 1.004s | 35.285s | 0.850s | 1m30.724s |
| 8 | 1.089s | 38.774s | 1.071s | 2m15.551s |

## Análise de Corrupção

Nos experimentos T1 e P1, o valor final do contador não atingiu 1 bilhão devido à ocorrência de condições de corrida 
(race conditions). A operação de incremento (counter++) não é atômica, sendo composta por leitura, incremento e escrita.
Quando múltiplas threads ou processos executam essa operação simultaneamente, ocorrem sobrescritas de valores, resultando 
na perda de incrementos.
Observou-se que, quanto maior o número de workers (N), menor o valor final obtido, evidenciando o aumento da concorrência 
e, consequentemente, das colisões de escrita. Em sistemas com múltiplos núcleos, esse efeito é amplificado devido ao 
paralelismo real proporcionado pelo hardware.

## Análise do gráfico
![Escalabilidade em ARM](graph/grafico_arm.png)
![Escalabilidade em x86](graph/grafico_x86.png)

O conjunto de gráficos apresenta a relação entre o tempo de execução e o número de workers (N) para os diferentes modelos 
de execução avaliados, considerando duas arquiteturas distintas: ARM e x86.
Em ambos os ambientes, observa-se que os cenários sem sincronização (T1 e P1) apresentam clara redução no tempo de 
execução à medida que o número de threads/processos aumenta, evidenciando boa escalabilidade devido ao paralelismo efetivo. 
No entanto, conforme discutido anteriormente, esses cenários produzem resultados incorretos devido à ocorrência de condições 
de corrida.
Por outro lado, o cenário com sincronização via mutex (T2) mantém o valor correto do contador em ambas as arquiteturas, 
porém apresenta aumento significativo no tempo de execução, especialmente ao passar de 2 para 4 workers. Esse comportamento 
evidencia o impacto do overhead de sincronização e da contenção do lock, que limita o paralelismo. Nota-se ainda que, mesmo 
com o aumento do número de threads, o desempenho não melhora, pois a região crítica impõe execução praticamente serial.
O cenário com processos e semáforo (P2) apresenta o maior custo de execução nos dois ambientes, sendo significativamente mais 
lento devido ao uso intensivo de chamadas de sistema para controle de acesso à memória compartilhada. Contudo, destaca-se 
uma diferença relevante entre as arquiteturas: enquanto no ambiente x86 os tempos de execução se mantêm na ordem de minutos, 
na arquitetura ARM os tempos são substancialmente maiores, chegando a dezenas de minutos. Essa diferença evidencia o impacto 
da arquitetura na eficiência das operações de sincronização, especialmente em workloads fortemente dependentes de syscalls.
A utilização de escala logarítmica no eixo Y permite visualizar adequadamente as diferenças entre os cenários, uma vez que 
os tempos variam em diferentes ordens de magnitude. As linhas tracejadas representam tendências aproximadas, reforçando os 
comportamentos observados: ganho de desempenho nos cenários sem sincronização e perda de escalabilidade quando mecanismos 
de controle de concorrência são introduzidos, com impacto ainda mais acentuado na arquitetura ARM.

## Observações técnicas

s valores 0644 e 0666 representam permissões de acesso no padrão Unix, expressas em notação octal, sendo utilizados para 
definir quem pode ler ou escrever em recursos do sistema, como semáforos e memória compartilhada. Cada dígito corresponde, 
respectivamente, ao dono, grupo e outros usuários. O valor 0644 concede permissão de leitura e escrita ao dono (6 = 4 + 2), 
enquanto grupo e outros possuem apenas leitura (4). Já o valor 0666 permite leitura e escrita para todos os usuários. 
Além disso, a flag IPC_CREAT indica que o recurso deve ser criado caso ainda não exista. No contexto deste trabalho, 
essas permissões foram utilizadas para simplificar o acesso e evitar problemas de autorização durante a execução.
Durante a implementação do experimento com processos e semáforos (P2), foi observado um comportamento inicial de aparente 
travamento do programa, interpretado como um possível loop infinito. No entanto, identificou-se que a causa estava 
relacionada ao uso de semáforos nomeados (sem_open), que persistem no sistema mesmo após o término do processo. 
Quando uma execução anterior era interrompida abruptamente, o semáforo podia permanecer em estado inconsistente, 
fazendo com que chamadas subsequentes a sem_wait bloqueassem indefinidamente. Esse problema foi solucionado com a 
utilização de sem_unlink antes da criação do semáforo, garantindo um estado limpo a cada execução.
Adicionalmente, verificou-se que o uso de semáforos introduz um overhead significativo, tornando a execução substancialmente 
mais lenta, especialmente para grandes volumes de operações. Isso ocorre devido ao custo elevado das chamadas de sistema 
envolvidas em cada operação de sincronização, já que cada incremento do contador exige operações de bloqueio e desbloqueio 
controladas pelo sistema operacional.
Com a execução dos experimentos em diferentes arquiteturas (x86 e ARM), foi possível observar uma diferença significativa 
de desempenho, especialmente no cenário P2 (processos com semáforo). Notou-se que, na arquitetura x86 (Intel Core i5-14600KF), 
o tempo de execução foi consideravelmente menor em comparação com a arquitetura ARM. Essa diferença ocorre principalmente 
devido a fatores arquiteturais e de implementação de sistema operacional. Processadores x86 tendem a possuir maior 
desempenho em operações que envolvem chamadas de sistema intensivas, como sem_wait e sem_post, além de apresentarem maior 
frequência de clock e otimizações mais maduras para execução concorrente. Por outro lado, arquiteturas ARM, embora mais 
eficientes energeticamente, geralmente possuem maior latência em operações de sincronização e menor desempenho em workloads 
altamente dependentes de syscalls. Além disso, o experimento P2 é fortemente limitado pelo custo de sincronização, já que 
cada incremento exige duas chamadas de sistema. Nesse contexto, qualquer diferença na eficiência dessas operações entre 
arquiteturas se torna amplificada, justificando a discrepância observada nos tempos de execução.
Por fim, observou-se que a variação do hardware também influencia diretamente a magnitude dos erros nos cenários sem 
sincronização. Em sistemas com múltiplos núcleos, o maior nível de paralelismo aumenta a probabilidade de acessos 
simultâneos à variável compartilhada, intensificando a ocorrência de condições de corrida e, consequentemente, a perda de 
incrementos.

## Conclusão
Os resultados obtidos demonstram claramente o trade-off entre desempenho e consistência em sistemas concorrentes. 
Threads apresentaram menor overhead de criação em comparação com processos, pois são mais leves e compartilham o 
mesmo espaço de memória, evitando a necessidade de mecanismos adicionais de comunicação. Já os processos possuem maior 
custo de criação (via fork) e exigem o uso de memória compartilhada (shm) para comunicação, aumentando a complexidade e o overhead.
Em relação à comunicação, as threads mostraram-se mais eficientes, uma vez que compartilham memória de forma nativa, 
enquanto processos dependem de mecanismos de IPC, como memória compartilhada e semáforos, que introduzem maior custo operacional.
Os experimentos também evidenciaram que, embora a ausência de sincronização proporcione melhor desempenho (T1 e P1), ela 
resulta em inconsistência de dados devido a condições de corrida. Por outro lado, o uso de mecanismos de sincronização 
(mutex e semáforos) garante a corretude do resultado, porém com impacto significativo no tempo de execução. Esse impacto 
é especialmente evidente no caso de processos com semáforos (P2), devido ao alto custo das chamadas de sistema envolvidas 
em cada operação de sincronização.
Além disso, a comparação entre arquiteturas evidenciou que esse custo não é uniforme: no ambiente x86, os tempos de execução 
para o cenário P2 foram significativamente menores quando comparados à arquitetura ARM. Isso demonstra que workloads 
intensivos em sincronização são altamente sensíveis à eficiência das chamadas de sistema e às características do hardware subjacente.
Assim, conclui-se que threads são mais eficientes para comunicação e possuem menor overhead de criação, enquanto 
processos oferecem maior isolamento ao custo de desempenho e maior complexidade. Adicionalmente, a escolha do modelo de 
concorrência e da arquitetura de execução deve considerar o tipo de carga de trabalho, especialmente quando há forte 
dependência de mecanismos de sincronização.

## Evidências

![Execucao](Assets/Execucao_ARM.png)
![Execucao_ARM](Assets/Execucao_ARM.png)
![semaforos_ARM](Assets/semaforos_ARM.png)

![x86_processos_livres8](Assets/x86_processos_livres8.jpeg)
![x86_processos_livres_2](Assets/x86_processos_livres_2.jpeg)
![x86_processos_livres_4](Assets/x86_processos_livres_4.jpeg)

![x86_semaforos_2](Assets/x86_semaforos_2.jpeg)
![x86_semaforos_4](Assets/x86_semaforos_4.jpeg)
![x86_semaforos_8](Assets/x86_semaforos_8.jpeg)

![x86_threads_2](Assets/x86_threads_2.jpeg)
![x86_threads_4](Assets/x86_threads_4.jpeg)
![x86_threads_8](Assets/x86_threads_8.jpeg)

![x86_threads_mutex_2](Assets/x86_threads_mutex_2.jpeg)
![x86_threads_mutex_4](Assets/x86_threads_mutex_4.jpeg)
![x86_threads_mutex_8](Assets/x86_threads_mutex_8.jpeg)

## Links
[Vídeo tutorial de pthreads] (https://www.youtube.com/watch?v=ldJ8WGZVXZk&t=305s)
[Vídeo tutorial de pthreads com Mutex] (https://www.youtube.com/watch?v=raLCgPK-Igc)
[Argumentos em linha de comando] (https://www.geeksforgeeks.org/cpp/command-line-arguments-in-c-cpp/)
[Processo e Semáfaros] (https://www.youtube.com/watch?v=ukM_zzrIeXs)
[Octal Notation] (https://medium.com/@thapavishal117/linux-permissions-using-numbers-known-as-octal-notation-2081f554c645)
[Memória Compartilhada] (https://www.youtube.com/watch?v=WgVSq-sgHOc)