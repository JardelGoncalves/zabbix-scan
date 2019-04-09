<p align="center">
  <img width="300" src="logo.png">
</p>

Ferramenta que retorna todos os servidores zabbix acessiveis pela internet no [Shodan](https://www.shodan.io/) e todos os servidores com usuário e senha padrões de instalação.

**OBS:** *Não me responsabilizo pelo uso inadequado da ferramenta.*

### Requisito
- Ter o pip3 instalado
  - `sudo apt-get install python3-pip`

### Executando
Baixando dependências
```
pip3 install -r requeriments.txt
```


Exemplo de execução:
```
python3 scan.py --c 43456kdfsdf4

ou

python3 scan.py --c 43456kdfsdf4 -t 4
```

`-t` é referente ao numero de threads, porém, o mesmo pode ser omitido. Seu valor padrão é 4.
