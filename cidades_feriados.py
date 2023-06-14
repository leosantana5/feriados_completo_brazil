import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import queue

def feriados(cidade, uf, ano, results_queue):
    url = f"https://www.feriados.com.br/feriados-{cidade}-{uf}.php?ano={ano}"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    soup = soup.find('div', id="calendar")
    soup = soup.find('div', class_="rounded_borders")
    soup = soup.find_all('div')

    for i in soup:
        try:
            tipo = str(i['title']).replace('</b>', '').replace('<b>', '')
        except:
            tipo = ''
        feriados1 = i.find_all(class_="style_lista_feriados")
        feriados2 = i.find_all(class_="style_lista_facultativos")
        feriados = feriados1 + feriados2

        for feriado in feriados:
            linha = str(feriado.get_text()).split("-")
            data = linha[0]
            feriado = linha[1]
            
            feriadoa = {
                "Municipio": str(cidade).replace('_', " "),
                "UF": str(uf).replace('_', " "),
                "Data": data,
                "Tipo": tipo,
                "Feriado": str(feriado).strip(),
            }

            results_queue.put(feriadoa)

def track_progress(future, progress):
    progress.update()

request = requests.get("http://www.calendario.com.br/api/cities.json").json()
results_queue = queue.Queue()

total_tasks = sum(len(cidades) for cidades in request.values())
anos = [2023, 2024]

with ThreadPoolExecutor() as executor, tqdm(total=total_tasks * len(anos)) as progress:
    futures = []
    for uf in request:
        for cidade in request[uf]:
            for ano in anos:
                if uf and cidade:
                    future = executor.submit(feriados, cidade, uf, ano, results_queue)
                    future.add_done_callback(lambda x: track_progress(x, progress))
                    futures.append(future)

    for future in futures:
        future.result()

results_list = []
while not results_queue.empty():
    results_list.append(results_queue.get())

df_feriados2 = pd.DataFrame(results_list)
df_feriados2.to_excel("feriados.xlsx", index=False)
