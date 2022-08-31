from bs4 import BeautifulSoup
import requests
import re
import  libtorrent as lt
import time
import os

nomefilme = input(("Digite o nome do filme:"))
nome2 = nomefilme.replace(' ', '%20')
print(nome2)
url = 'https://yts.rs/browse-movies/'+nome2
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


#pega o nome do filme
movieData = [a.attrs.get('title') for a in soup.select('a')]
movie =movieData
res = list(filter(lambda item: item is not None, movieData))
res2 = []
for i in res:
    #print(i)
    if i != "Search" and i != "Browse":
        res2.append(i)

#pegar o link
movieLink = [a.attrs.get('href') for a in soup.select('a')]
link = movieLink[9:]
link2 = link[:-16]
linkF=[]
tr = 0
tam = len(link2)/2


for i in link2:
    if((tr%2) ==0):
        linkF.append(i)
    tr = tr +1


os.system('cls')
#exibir dados na tela
print("Filmes encontrados: ")
indx = 1
for i in res2:
    print("["+str(indx)+"]"+" - "+ str(i))
    indx = indx + 1
op = input("Digite sua opção:")
linkMag = linkF[int(op)-1]

#proxima pagina
url = 'https://yts.rs'+linkMag
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
movieQuality = soup.select('a',{'class': 'download-torrent popup123'})

#pega o link do torrent
q720 = str(movieQuality[9])
a720 = q720.split('"')
q1080 = str(movieQuality[10])
a1080 = q1080.split('"')

print("")
print("[1]"+res2[int(op)-1]+"em 720p")
op2 = input("[2]"+res2[int(op)-1]+"em 1080p")
if(int(op2)==1):
    magenet = a720[3]
if(int(op2)==2):
    magenet = a1080[3]


print(magenet)
#####torrent download
ses = lt.session()
ses.listen_on(6881, 6891)
pasta = r"C:\Users\silva\PycharmProjects\pythonProject\Downloads"
params = {
    'save_path': pasta,
    'storage_mode': lt.storage_mode_t(2),

}
link = "MAGNET_LINK_HERE"
handle = lt.add_magnet_uri(ses, magenet, params)
ses.start_dht()

print('downloading metadata...')
while (not handle.has_metadata()):
    time.sleep(1)
print('got metadata, starting torrent download...')
while (handle.status().state != lt.torrent_status.seeding):
    os.system('cls')
    s = handle.status()
    state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
    print('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)
