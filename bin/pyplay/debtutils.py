from datetime import datetime
from collections import OrderedDict
import requests
import subprocess

class DebtUtils:
    def dataRetrieve():
        url = "http://www.sidra.ibge.gov.br/api/values/t/1737/p/201509-201704/v/63/n1/1/h/n/f/c"
        ipca = requests.get(url).json()
        drawee = {'201509':70000, '201512':10000, '201604':31500, '201605':31500,  '201606': 31500, 
        '201607':31500,  '201608':36750,  '201609':36750,  '201610':36750,  '201611':36750, 
        '201612':36750,  '201701':36750,  '201702':36750,  '201703':36750}
        drawee = OrderedDict(sorted(drawee.items()))
        output = "Data;Retirada;Índice acumulado;Valor Corrigido;Saldo Atualizado\n"
        
        vtotal=0
        for d, v in drawee.items():
            index = 1
            for i in range(0, len(ipca)):
                if ipca[i].get('D1C') == d:
                    for j in range(i, len(ipca)):
                        index = index*(1+ float(ipca[j].get('V'))/100)
                    break
                else:
                    pass
            if index != 1:
                vtotal = round(vtotal+v*index, 2)
                output = output + datetime.strptime(d,"%Y%m").strftime("%b/%Y") + ";" + str(v) + ";" +\
                str(index-1) + ";" + str(round(v*index, 2)) + ";" + str(vtotal) + "\n"
        return output, ipca
    def saveContent(input):    
        filename = "teste.csv"
        fd = open(filename, 'w')
        fd.write(input)
        fd.close()
        subprocess.Popen(['/usr/sbin/localc', filename])
