from shodan import Shodan, APIError
from time import sleep
import argparse
from zabbix_api import ZabbixAPI
from multiprocessing.dummy import Pool as ThreadPool
from os import system, name as NameSystem


class ZabbixScan:
    def __init__(self, shodan_key, number_thread = 2):
        self.api = Shodan(shodan_key)
        self.number_thread = number_thread
        self.login_success = []
        self.total = 0

    def getServers(self):
        server_list = []
        try:
            results = self.api.search('zabbix')   
            server_list = results['matches']

        except APIError as e:
            print("Error: {0}".format(e))

        return server_list

    def verify(self, host):
        try:
            zapi = ZabbixAPI(server="http://{0}/zabbix".format(host['ip_str']))
            zapi.login("Admin", "zabbix")
            self.login_success.append(host)
        except:
            pass

    def getCountry(self, servers):
        regiao = {}
        for server in servers:
            country_name = server['location']['country_name']
            if country_name not in regiao:
                regiao[country_name] = 0
            regiao[country_name] += 1
        
        return regiao


    def execute(self):
        servers = self.getServers()
        

        self.total = len(servers)
        pool = ThreadPool(self.number_thread)

        results = pool.map(self.verify, servers)
        pool.close()
        pool.join()

        system('cls' if NameSystem == 'nt' else 'clear')
        print('Total de Servidores Zabbix: {0}'.format(len(servers)))
        print('\n\nQuantidade de servidores por pais:')
        
        paises = self.getCountry(servers)
        for pais in sorted(paises.keys()):
            print(pais, '=', paises[pais])

        print('\n\nQuantidade de servidores com username e senha padrão:')        
        paises_login = self.getCountry(self.login_success)
        for pais in sorted(paises_login.keys()):
            print(pais, '=', paises_login[pais])
        

def header():
    head = '''
 ______     ______     ______     ______     __     __  __        ______     ______     ______     __   __    
/\___  \   /\  __ \   /\  == \   /\  == \   /\ \   /\_\_\_\      /\  ___\   /\  ___\   /\  __ \   /\ "-.\ \   
\/_/  /__  \ \  __ \  \ \  __<   \ \  __<   \ \ \  \/_/\_\/_     \ \___  \  \ \ \____  \ \  __ \  \ \ \-.  \  
  /\_____\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\   /\_\/\_\     \/\_____\  \ \_____\  \ \_\ \_\  \ \_\\\\"\_\ 
  \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_/   \/_/\/_/      \/_____/   \/_____/   \/_/\/_/   \/_/ \/_/ 


Author: Jardel Gonçalves Ferreira
Github: github.com/JardelGoncalves
'''
    print(head)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--chave', dest="key", help="A sua chave da API do Shodan", required=True)
    parser.add_argument('-t', '--thread', dest="thread", help="Numero de threads", default=4, required=False)
    args = parser.parse_args()

    key = args.key 
    thread = args.thread

    zabbix = ZabbixScan(key, int(thread))
    zabbix.execute()

if __name__=='__main__':
    header()
    sleep(4)
main()