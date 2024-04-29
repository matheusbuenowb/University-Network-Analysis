import speedtest; #Biblioteca referente ao medidor de velocidade speedtest, o qual contém 3 funcionalidades fundamentais para o programa
from datetime import datetime #Biblioteca para obter informações a respeito do horário  
from requests import get #Para obter uma requisição de um site
import csv
import os #Biblioteca para importar o comando 'CLS'


def testa_Jitter():
   
  latencia_result = [0,0,0,0,0]; #é criado um vetor para armazenar os valores do latencia
  jitter_result = [0,0,0,0]; #é criado um vetor para armazenar as variações entre (n - 1)... latencias para o cálculo do jitter  
  for c in range(0, 5):
    if(c == 0):
      test = speedtest.Speedtest(secure = True);
      best = test.get_best_server(); #é pego o melhor servidor baseado no quesito distância x latencia
      print(f"Latência {c + 1} : {test.results.ping} ms");
      latencia_result[c] = test.results.ping; #o valor do latencia é adicionado ao vetor
    else:
      best = test.get_best_server();
      print(f"Latência {c + 1} : {test.results.ping} ms");
      latencia_result[c] = test.results.ping; 
      jitter_result[c - 1] = abs(latencia_result[c] - latencia_result[c - 1]); #o valor pego entre a subtração da variação 
      #entre o latencia (n - 1) é armazenado no vetor jitter_result, para que no final o resultado seja divido por 4,
      #que foi o valor optado para trabalhar neste programa
      #Utiliza a função abs para que a soma seja efetuada  

  jitter_final = (sum(jitter_result))/4; #a função sum soma todos os valores obtidos das variações obtidas das latências
  return jitter_final;


qtd = int(input("Digite a quantidade de testes a serem realizados: "));
bloco = str(input("Digite o bloco em que o teste está sendo realizado: "));
sala = str(input("Digite a sala em que o teste será realizado: "));
transmissao = int(input("O teste é via transmissão Ethernet (1) ou Wi-Fi (2)? "));

if transmissao == 1:
  transmissao = 'Ethernet';
elif transmissao == 2:
  transmissao = 'Wi-Fi';

archive_name = "Bloco" + bloco + "_Sala" + sala + "_" + transmissao; 

with open(f"{archive_name}.csv", 'w') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  spamwriter.writerow(['Data'] + ['Horário'] + ['Horário e Data'] +['Download'] +
                      ['Upload'] + ['Latência'] + ['Jitter'] + ['Servidor'] + 
                      ['Local'] + ['Cidade e Estado'] + ['Latitude'] + ['Longitude'] + 
                      ['IP Cliente'] + ['Bloco'] + ['Transmissão'] + ['Sala'])
  for i in range(0, qtd): 
      print(f"\n Teste: {i + 1}") 
      teste = speedtest.Speedtest(secure = True);
      print("\nCarregando a lista de servidores...");
      teste.get_servers(); #a função get_servers serve para obter as informações referentes ao servidores disponíveis
      print("\nEscolhendo o melhor servidor...");   
      melhor_servidor = teste.get_best_server(); 
      #o objeto melhor_servidor recebe o melhor servidor escolhido baseado na medida latencia x distância
      print(f"\nMelhor servidor: {melhor_servidor['host']} localizado em {melhor_servidor['country']}\n");
        
      # Testando as velocidades e tempo de resposta
      print('\nRealizando o teste de download...');
      velocidade_download = round(teste.download(threads=None)*(10**-6)) #armazena os dados do teste de download nesta variável
      # é dividido por 10^6 por conta do valor não ser retornado na medida de Mb/s (megabits por segundo) 
      print('\nRealizando o teste de upload...');
      velocidade_upload = round(teste.upload(threads=None)*(10**-6)); #armazena os dados do teste de upload nesta variável
        
      print('\nTestando a latência (latencia)...');
      latencia_resultado = round(teste.results.ping); #A função round serve para arrendodar as casas decimais
      #para que dessa forma o número final esteja com casas decimais satisfatórias. 

      print('\nCalculando o Jitter...');  
      jitter_resultado = str(round(testa_Jitter(), 2)); 

      # Capturando data e hora do teste através das funções da biblioteca datetime.
      data_atual = datetime.now().strftime('%d/%m/%Y');
      hora_atual = datetime.now().strftime('%H:%M');
      local = melhor_servidor['country']
      servidor_atual = melhor_servidor['sponsor']
      cidade_estado = melhor_servidor['name']
      latitude = melhor_servidor['lat']
      longitude = melhor_servidor['lon']
      data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      print(f"\nDownload: {velocidade_download} Mbps")
      print(f"Upload: {velocidade_upload} Mbps")
      print(f"latencia: {latencia_resultado} ms")
      print(f"Jitter: {jitter_resultado} ms")
      IP_Externo = get('https://api.ipify.org').text;
      spamwriter.writerow([data_atual, hora_atual, data_hora, 
                          velocidade_download, velocidade_upload, 
                          latencia_resultado, jitter_resultado, 
                          servidor_atual, local, cidade_estado, 
                          latitude, longitude, IP_Externo, bloco, 
                          transmissao, sala])
      os.system("cls")


#df = pd.read_csv(f"{archive_name}.csv", sep = ',')

#df