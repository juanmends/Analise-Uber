import pandas as pd
from collections import Counter
from datetime import datetime
import plotly.express as px

def calcular_duracao(str_inicio,str_fim):
    formato = "%Y-%m-%dT%H:%M:%S.000Z"
    inicio = datetime.strptime(str_inicio, formato)
    fim = datetime.strptime(str_fim, formato)
    duracao = fim - inicio
    segundos = duracao.seconds
    return segundos

def converte_segundos(tempo_em_segundos):
    horas, segundos_restantes = divmod(tempo_em_segundos,3600)
    minutos, segundos = divmod(segundos_restantes,60)
    return horas, minutos, segundos

def formata_endereco(endereco):
    if (endereco.split('-')[0]) == "":
        return endereco
    endereco_formatado = (endereco.split('-')[0]) + "-" + (endereco.split('-')[1])
    return endereco_formatado

def analisa_dados_func(csv_path, usuario):
    #Abrindo arquivo csv
    df = pd.read_csv(csv_path)

    #Ranking dos tipos de Corridas(UberX, Comfort, Black, ...)
    lista_tipos_de_corridas = df["product_type"].tolist()
    contador_tipo = Counter(lista_tipos_de_corridas)
    #Gráfico tipos de Corridas
    df_fig_tipos = pd.DataFrame(contador_tipo.items(), columns=['tipos', 'corridas'])
    fig_tipos = px.pie(df_fig_tipos, names='tipos', values='corridas', title='Tipos de Corridas mais Usados', hole=0.3)
    fig_tipos.write_html(f'templates/graficos/{usuario}tipos.html')


    #Quantidade de corridas completadas
    df_status_completadas = df[df["status"] == "completed"]
    corridas_completadas = df_status_completadas.shape[0]

    #Quantidade de corridas canceladas pelo motorista
    df_status_canceladas = df[df["status"] == "rider_canceled"]
    corridas_canceladas = df_status_canceladas.shape[0]

    #Locais de embarque mais frequentes
    lista_embarque = df["begintrip_address"].dropna().tolist()
    contador_embarque = Counter(lista_embarque)
    #Gráfico embarque
    df_fig_embarque = pd.DataFrame(contador_embarque.items(), columns=['local', 'corridas'])
    df_fig_embarque['local'] = df_fig_embarque['local'].apply(formata_endereco)
    fig_embarque = px.pie(df_fig_embarque, names='local', values='corridas', title='Locais de Embarque mais Comuns', hole=0.3)
    fig_embarque.write_html(f'templates/graficos/{usuario}embarque.html')

    # Locais de destino mais frequentes
    lista_destino = df["dropoff_address"].tolist()
    contador_destino = Counter(lista_destino)
    #Gráficos destino
    df_fig_destino = pd.DataFrame(contador_destino.items(), columns=['local', 'corridas'])
    df_fig_destino = df_fig_destino.dropna()
    df_fig_destino['local'] = df_fig_destino['local'].apply(formata_endereco)
    fig_destino = px.pie(df_fig_destino, names='local', values='corridas', title='Destinos mais Comuns', hole=0.3)
    fig_destino.write_html(f'templates/graficos/{usuario}destino.html')

    #Corrida mais distante
    lista_distancia = df["distance"].dropna().tolist()
    corrida_mais_distante = max(lista_distancia)

    #Corrida mais cara
    df_preco = df.dropna()
    df_preco = df_preco["fare_amount"]
    lista_preco = df_preco.tolist()
    corrida_mais_cara = max(lista_preco)

    #Corrida mais barata
    corrida_mais_barata = min(lista_preco)

    #Média de preço das corridas
    soma_precos = df_preco.sum()
    total_precos = df.dropna().shape[0]
    media_precos = soma_precos/total_precos

    #Horários em que mais chama corrida
    horarios = {
        "madrugada": 0,
        "manha" : 0,
        "tarde" : 0,
        "noite" : 0
    }
    df_horarios = df["request_time"]

    for i in range(df_horarios.shape[0]):
        data = df_horarios[i].split('T')
        time = (data[1]).split(':')
        hora = int(time[0]) - 3 #FUSO HORÁRIO DE BRASÍLIA
        if hora<0:
            hora += 24
        if hora<6:
            horarios["madrugada"]+=1
        elif hora<12:
            horarios["manha"]+=1
        elif hora<18:
            horarios["tarde"]+=1
        else:
            horarios["noite"]+=1
    contagem_horarios = Counter(horarios)
    #Gráfico dos Horários
    df_fig_horarios = pd.DataFrame(horarios.items(), columns=['horario','corridas'])
    fig_horarios = px.pie(df_fig_horarios, names='horario', values='corridas', title='Horários mais Comuns', hole=0.3)
    fig_horarios.write_html(f'templates/graficos/{usuario}horarios.html')

    #Duração média das corridas
    df_duracao = df.dropna().reset_index()
    df_duracao["duracao"] = 0
    for i in range(df_duracao.shape[0]):
        tempo_inicial = df_duracao["begin_trip_time"][i]
        tempo_final = df_duracao["dropoff_time"][i]
        df_duracao.loc[i, "duracao"] = calcular_duracao(tempo_inicial,tempo_final)
    soma_tempo = df_duracao["duracao"].sum()
    total_tempo = df_duracao.shape[0]
    media_tempo_segundos = soma_tempo/total_tempo
    media_final_horas, media_final_minutos, media_final_segundos = converte_segundos(media_tempo_segundos)

    #Corrida de maior duração
    lista_duracao = df_duracao["duracao"].tolist()
    maior_duracao = max(lista_duracao)
    horas_maior_duracao, minutos_maior_duracao, segundos_maior_duracao = converte_segundos(maior_duracao)

    #Corrida de menor duração
    menor_duracao = min(lista_duracao)
    horas_menor_duracao, minutos_menor_duracao, segundos_menor_duracao = converte_segundos(menor_duracao)

    # #Resultados
    # print(f"Total de corridas chamadas: {df.shape[0]}")
    # print(f"Tipos de viagens: {ranking_tipos_de_viagens}")
    # print(f"Corridas completadas: {corridas_completadas}")
    # print(f"Corridas canceladas pelo motorista: {corridas_canceladas}")
    # print(f"Locais de embarque mais frequentes: {ranking_embarque}")
    # print(f"Locais de destino mais frequentes: {ranking_destino}")
    # print(f"Corrida mais distante: {(corrida_mais_distante*1.609344):.2f}Km")
    # print(f"Corrida mais cara: R${corrida_mais_cara}")
    # print(f"Corrida mais barata: R${corrida_mais_barata}")
    # print(f"Média de preço por corrida: R${media_precos:.2f}")
    # print(f"Horário das corridas {ranking_horarios}")
    # print(f"Duração média de uma corrida {media_final_horas:.0f} horas, {media_final_minutos:.0f} minutos e {media_final_segundos:.0f} segundos")
    # print(f"Corrida com maior duração: {horas_maior_duracao} horas, {minutos_maior_duracao} minutos e {segundos_maior_duracao} segundos")
    # print(f"Corrida com menor duração: {horas_menor_duracao} horas, {minutos_menor_duracao} minutos e {segundos_menor_duracao} segundos")

    #Resultados
    uber_data = [
        {
            "title": "Uber Wrapped",
            "text": "Uma retrospectiva das suas viagens",
            "icon": "🚗",
            "isIntro": "true"
        },
        {
            "title": "Total de Corridas Chamadas",
            "value": df.shape[0],
            "icon": "🗓️"
        },
        {
            "title": "Tipos de Corridas",
            "chart_url": f'{usuario}/tipos'
        },
        {
            "title": "Corridas Completadas",
            "value": corridas_completadas,
            "icon": "✅"
        },
        {
            "title": "Corridas Canceladas pelo Motorista",
            "value": corridas_canceladas,
            "icon": "❌"
        },
        {
            "title": "Embarques Favoritos",
            "chart_url": f'{usuario}/embarque'
        },
        {
            "title": "Destinos Favoritos",
            "chart_url": f'{usuario}/destino'
        },
        {
            "title": "Corrida Mais Distante",
            "value": corrida_mais_distante,
            "unit" : "Km",
            "icon": "🛣️"
        },
        {
            "title": "Corrida Mais Cara",
            "value": "R$ "+ str(corrida_mais_cara),
            "icon": "💸"
        },
        {
            "title": "Corrida Mais Barata",
            "value": "R$ " + str(corrida_mais_barata),
            "icon": "💰"
        },
        {
            "title": "Média de Preço",
            "value": f"R$ {media_precos:.2f}",
            "icon": "📈"
        },
        {
            "title": "Horários Mais Comuns",
            "chart_url": f'{usuario}/horarios'
        },
        {
            "title": "Duração Média das Corridas",
            "value": f"{media_final_horas:.0f}h {media_final_minutos:.0f}min {media_final_segundos:.0f}s",
            "icon": "⏰"
        },
        {
            "title": "Corrida de Maior Duração",
            "value": f"{horas_maior_duracao}h {minutos_maior_duracao}min {segundos_maior_duracao}s",
            "icon": "⏳"
        },
        {
            "title": "Corrida de Menor Duração",
            "value": f"{horas_menor_duracao}h {minutos_menor_duracao}min {segundos_menor_duracao}s",
            "icon": "💨"
        },
        {
            "title": "Obrigado!",
            "text": "Continue explorando a cidade com o Uber",
            "icon": "🌟",
            "isOutro": "true"
        }
    ]

    return uber_data
