import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

engine = create_engine('sqlite:///feriados.db')

def feriados(cidade, uf):

    url = f"https://www.feriados.com.br/feriados-{cidade}-{uf}.php"

    html = requests.get(url).content


    soup = BeautifulSoup(html, 'html.parser')

    # _____________   FUNCIONANDO 100%

    soup = soup.find('div', id="calendar")
    soup = soup.find('div', class_="rounded_borders")
    soup = soup.find_all('div')

    feriados_sql = []
    for i in soup:
        try:
            tipo = str(i['title']).replace('</b>','').replace('<b>','')

        except:
            tipo = ''
        feriados1 = i.find_all(class_="style_lista_feriados")
        feriados2 = i.find_all(class_="style_lista_facultativos")
        feriados = feriados1 + feriados2
 
        
        for feriado in feriados:

            # print('-------------------')
            linha = str(feriado.get_text()).split("-")
            data = linha [0]
            feriado = linha[1]
            
            
            
            feriadoa = {
                "Municipio":cidade,
                "UF":uf,
                "Data":data,
                "Tipo":tipo,
                "Feriado":feriado,
            }
            feriados_sql.append(feriadoa)

    df_feriados = pd.DataFrame(feriados_sql)

    df_feriados.to_sql(name='feriados', con=engine, if_exists='append', index=False)
    print(f"Base de Feriados ATUALIZADA - {cidade} - {uf}")
    
request = requests.get("http://www.calendario.com.br/api/cities.json").json()

for uf in request:
    for cidade in request[uf]:
        feriados(cidade, uf)
    

