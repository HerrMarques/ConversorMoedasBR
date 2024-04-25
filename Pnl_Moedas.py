import dash
import datetime
import pandas as po
import plotly.express as pex
from dash import Dash, html, dcc,Input,Output,State

# Section 1: Código de Conversão
real_port={"Moeda":"Real Português",
           "Governo":"Manuel I de Portugal",
           "Data de Implementação":datetime.datetime(1500,4,22),
           "Fim da Vigência":datetime.datetime(1833,10,7),
           "Símbolo":"R",
           "Taxa de Conversão":"ouro:1200"
           }
real_bra={"Moeda":"Real Brasileiro",
           "Governo":"D. Pedro II",
           "Data de Implementação":datetime.datetime(1833,10,8),
           "Fim da Vigência":datetime.datetime(1942,10,31),
           "Símbolo":"Rs",
           "Taxa de Conversão":1200/2500
           }
cr={"Moeda":"Cruzeiro",
           "Governo":"Getúlio Vargas",
           "Data de Implementação":datetime.datetime(1942,11,1),
           "Fim da Vigência":datetime.datetime(1967,2,12),
           "Símbolo":"Cr$",
            "Taxa de Conversão":{1000:1} # mil-réis corresponde a um cruzeiro
        #    datetime.datetime(1964,11,30)
           #datetime.datetime(1967,2,12)
           }
crN={"Moeda":"Cruzeiro Novo",
           "Governo":"Castelo Branco",
           "Data de Implementação":datetime.datetime(1967,2,13),
           "Fim da Vigência":datetime.datetime(1970,5,14),
           "Símbolo":"NCr$",
           "Taxa de Conversão":{1000:1} # mil cruzeiros corresponde a um cruzeiro novo
           }
cr2={"Moeda":"Cruzeiro",
           "Governo":"Emílio Garrastazu Médici",
           "Data de Implementação":datetime.datetime(1970,5,15),
           "Fim da Vigência":datetime.datetime(1986,2,27),
           "Símbolo":"Cr$",
           "Taxa de Conversão":{1:1} # um cruzeiro novo corresponde a um cruzeiro
        #    datetime.datetime(1984,8,15),
           }
crz={"Moeda":"Cruzado",
           "Governo":"José Sarney",
           "Data de Implementação":datetime.datetime(1986,2,28),
           "Fim da Vigência":datetime.datetime(1989,1,15),
           "Símbolo":"Cz$",
           "Taxa de Conversão":{1000:1} # mil cruzeiros corresponde a um cruzado
           }
crzN={"Moeda":"Cruzado Novo",
           "Governo":"José Sarney",
           "Data de Implementação":datetime.datetime(1989,1,16),
           "Fim da Vigência":datetime.datetime(1990,3,15),
           "Símbolo":"NCz$",
           "Taxa de Conversão":{1000:1} # mil cruzados corresponde a um cruzado novo
           }
cr3={"Moeda":"Cruzeiro",
           "Governo":"Fernando Collor",
           "Data de Implementação":datetime.datetime(1990,3,16),
           "Fim da Vigência":datetime.datetime(1993,7,31),
           "Símbolo":"Cr$",
           "Taxa de Conversão":{1:1} # um cruzado novo corresponde a um cruzeiro
           }
creal={"Moeda":"Cruzeiro Real",
           "Governo":"Itamar Franco",
           "Data de Implementação":datetime.datetime(1993,8,1),
           "Fim da Vigência":datetime.datetime(1994,6,30),
           "Símbolo":"CR$",
           "Taxa de Conversão":{1000:1} # mil cruzeiros corresponde a um cruzeiro real
           }
brl={"Moeda":"Real",
           "Governo":"Itamar Franco",
           "Data de Implementação":datetime.datetime(1994,7,1),
           "Fim da Vigência":"",
           "Símbolo":"R$",
           "Taxa de Conversão":{2750:1} #dois mil setessentos e cinquenta cruzeiros reais corresponde a um real
           }
# Ordem Cronológica das Moedas
ocm=["real_port","real_bra","cr","crN","cr2","crz","crzN","cr3","creal","brl"]

tab=po.DataFrame([real_port,real_bra,cr,crN,cr2,crz,crzN,cr3,creal,brl])
tab.index=ocm
tab['Data de Implementação']=po.to_datetime(tab['Data de Implementação'], errors='coerce',format="%d/%m/%Y")
tab['Fim da Vigência']=po.to_datetime(tab['Fim da Vigência'], errors='coerce',format="%d/%m/%Y")

infl=po.read_csv('20240402030810.csv',sep=';')
in30=po.read_csv("Inflação 1930-1994.csv",sep=";")
in30["Variação Acumulada no Ano"]=in30["Variação Acumulada no Ano"].str.replace(',','.')
in30.index = po.to_datetime(in30.index, format='%B %Y')
infl=infl[1:30]
infl["Data"]=infl.index
infl["Data"]=infl["Data"].str.replace("dezembro",'Dec')
infl.index = po.to_datetime(infl["Data"], format='%b %Y')
infl=infl.drop(columns='Data')
infl=infl.rename(columns={"Variação acumulada no ano durante o Plano Real":
                          "Variação Acumulada no Ano"})
infl=po.concat([in30,infl])
infl["Variação Acumulada no Ano"]=infl["Variação Acumulada no Ano"].astype(float)/100
infl=infl.rename_axis('Data')

def edit_num(num:float,moeda_final:StopAsyncIteration):

    sufixos = ['Milhão','Bilhão','Trilhão','Quadrilhão','Quintilhão','Sextilhão','Octilhão',
                'Nonilhão', 'Decilhão','', 'Mil', 'Milhões de', 'Bilhões de', 'Trilhões de','Quadrilhões de',
               'Quintilhões de','Sextilhões de','Octilhões de', 'Nonilhões de', 'Decilhões de']
    computus=['','Conto de Réis','Contos de Réis']
    if num == 0.0000:
        return 'zero'
    
    magnitude = 9
    while num >= 1000:
        magnitude += 1
        num /= 1000

    if  moeda_final in ('Real Brasileiro','Real Português'):
        if magnitude==11:
            magnitude=9
            if num==1:
                cpt=1
            else:cpt=2
        elif magnitude>11:
            magnitude-=2
            cpt=2
    else:cpt=0
    
    if num==1 and magnitude>10:
        magnitude-=11
        if cpt==2:
            cpt=1

    return '{} {} {}'.format(round(num, 2), sufixos[magnitude],computus[cpt])

def inflacao_acumulada(args):
    # Verificar se há pelo menos uma taxa de inflação fornecida
    if len(args) < 1:
        return "Erro: Forneça pelo menos uma taxa de inflação."
    
    # Calculando a inflação acumulada
    inflacao_acumulada = 1
    for taxa_inflacao in args:
        inflacao_acumulada *= (1 + taxa_inflacao)
    
    inflacao_acumulada -= 1
    return inflacao_acumulada

def corr_infl(valor,periodo_in,periodo_dest):
   """
    Parameters:
        valor        : Quantidade na moeda original.
        periodo_in   : Período de que se quer converter.
        periodo_dest : Período para qual se quer converter.
   """
   taxas=tuple(i for _,i in infl.query(str(min(periodo_in,periodo_dest))+"<`Data`<"+\
      str(max(periodo_in,periodo_dest)))["Variação Acumulada no Ano"].items())
   corre=valor
   infl_periodo=inflacao_acumulada(taxas)
   
   if periodo_in> periodo_dest:
      corre=corre/(1+infl_periodo)
   else:
      corre=corre*(1+infl_periodo)

   if periodo_dest>=1994 and periodo_in >=1994:
        print(f'R${valor} em {periodo_in} tem o mesmo poder de compra que R$ {corre} em {periodo_dest}.')
   else:return corre


    
    # return conv
    # print(corr_infl(conv,ano_in,ano_dest))

def converter(moeda_orig:str,valor:float,ano_dest:int,ano_in=None):
    """
    Parameters:
        mod_orig: Moeda de Origem.
        valor   : Quantidade na moeda original.
        ano_dest: Ano a se converter.
    """
    mod_original=tab.query("`Moeda`==@moeda_orig").index[0]
    if not ano_in:
        ano_in=tab.query("`Moeda`==@moeda_orig")['Data de Implementação'].iloc[0].year

    if ano_dest<tab['Data de Implementação'].iloc[1].year:
        moeda_final= tab['Moeda'].iloc[0]
        cifra= tab['Símbolo'].iloc[0]
    elif ano_dest>tab['Data de Implementação'].iloc[-1].year:
        moeda_final= tab['Moeda'].iloc[-1]
        cifra= tab['Símbolo'].iloc[-1]
    else:
        moeda_final= tab[(tab['Data de Implementação'].dt.year <= ano_dest) &
                      (tab['Fim da Vigência'].dt.year >= ano_dest)]['Moeda'].iloc[0]
        cifra= tab[(tab['Data de Implementação'].dt.year <= ano_dest) &
                      (tab['Fim da Vigência'].dt.year >= ano_dest)]['Símbolo'].iloc[0]
      
    if tab[tab['Moeda']==moeda_orig]['Fim da Vigência'].iloc[0].year<ano_dest:
        mod_final=tab.query("`Moeda`==@moeda_final").index[0]
        mds=ocm[ocm.index(mod_original):ocm.index(mod_final)+1]
        conv=valor
        for i in mds:
            conv=(conv/next(iter(globals()[i]["Taxa de Conversão"])))*\
            globals()[i]["Taxa de Conversão"][next(iter(globals()[i]["Taxa de Conversão"]))]
        conv=round(conv,2)
    elif tab[tab['Moeda']==moeda_orig]['Data de Implementação'].iloc[0].year>ano_dest:
        mod_final=tab.query("`Moeda`==@moeda_final").index[0]
        mds=ocm[ocm.index(mod_final):ocm.index(mod_original)+1][::-1][:-1]
        conv=valor
        for i in mds:
            conv=float((conv*next(iter(globals()[i]["Taxa de Conversão"])))*\
            globals()[i]["Taxa de Conversão"][next(iter(globals()[i]["Taxa de Conversão"]))])
        conv=round(conv,2)
    
    conv_edit=edit_num(conv,moeda_final)

    # print(f"A quantia de {valor} unidades de {moeda_orig} corresponderia a {conv_edit} unidades de "
    #        f"{moeda_final}({cifra}) em {ano_dest}.")
    return conv_edit,moeda_final,cifra


# Section 2:Painel
###########Código para criar o painel

site = Dash(__name__)

cores = {
    'CordeFundo': '#111111',
    'texto': '#AFE1AF'
}

site.layout = html.Div(id='principal',style={'backgroundColor': cores['CordeFundo']}, children=[
    html.H1(
        children='Conversor de Moedas',
        style={
            'textAlign': 'center',
            'color': cores['texto']
        }
    ),
    html.H2(children='Moedas do Brasil', style={
        'textAlign': 'center',
        'color': cores['texto']
    }),
    html.H4(children='Converta as Moedas brasileiras',
        style={
            'textAlign': 'center',
            'color': cores['texto']
        }),
    html.Br(),
    html.Div(id='secInserir',style={'color': cores['texto'],
            'backgroundColor': cores['CordeFundo']},
            children=[
        html.Label('Selecione a Moeda',
        style={
            'margin-right': '5px',
            'color': cores['texto']
        }),
        dcc.Dropdown( 
            id='SelecMoeda',
            value='Real',
            options=[i for i in tab["Moeda"]],
            style={
            'textAlign': 'center',
            'display': 'inline-block',
            'margin-right': '80px',
            'color': cores['texto'],
            'backgroundColor': '#808089'
        }            ),
        html.Label('Selecione o Ano Alvo',
        style={
            'margin-right': '5px',
            'color': cores['texto']
        }),  
        # dcc.Dropdown( 
        #     id='Anode',
        #     options=[i for i in range(1500,datetime.datetime.now().year)], 
        # style={
        #     'textAlign': 'left',
        #     'display': 'inline-block',
        #     'margin-right': '60px',
        #     'color': cores['texto'],
        #     'backgroundColor': cores['CordeFundo']
        # }            ),
        dcc.Dropdown( 
            id='AnoAlvo',
            options=[i for i in range(1500,datetime.datetime.now().year)], 
            value=1964,
            style={
            'textAlign': 'left',
            'display': 'inline-block',
            'margin-right': '60px',
            'color': cores['texto'],
            'backgroundColor':'#808089'
                    }),
        html.Label('Digite a Quantia',
            style={
            'margin-right': '5px',
            'color': cores['texto']
        }),
        dcc.Input(
            id='inputQuant',
            value=200,
            style={'color': cores['texto'],
            'backgroundColor': '#808089'}
            ),
        html.Button(children='Converter', id='btnConverter',style={'margin-left':'15px','color': cores['texto'],
            'backgroundColor': '#28282B'},n_clicks=0),
        # html.Button('Ocultar', id='btnOcultar',role='ok',style={'margin-left':'15px','color': cores['texto'],
            # 'backgroundColor': '#28282B'})
    ]
            ),
    html.Br(),
    html.Div(style={
        'margin':'25px',
        'font-size':'25px'}
    ,children=[
        # html.H4(children=f'Converção de {moeda_orig} para {moeda_final}({cifra})',style={
        # 'textAlign': 'center',
        # 'color': cores['texto']}),  
        html.P(id='sec_Conversao'#children=[f"A quantia de {valor} unidades de {moeda_orig} corresponderia a {conv_edit} unidades de "
            #f"{moeda_final}({cifra}) em {ano_dest}."]
            ,style={
        'textAlign': 'center',
        'color': cores['texto']})
        ]  # Text for the hidden section
    )
])

@site.callback(
    Output(component_id='sec_Conversao', component_property='children'),
    [Input(component_id='btnConverter', component_property='n_clicks')],
    [State(component_id='SelecMoeda', component_property='value'),
    State(component_id='AnoAlvo', component_property='value'),
    State(component_id='inputQuant', component_property='value')]
    )
def click(clique,moeda,ano,quantia):
    conv_edit,moeda_final,cifra=converter(moeda,float(quantia),ano)
    return "A quantia de {} unidades de {} corresponderia a {} unidades de {}({}) em {}."\
                                .format(quantia,moeda,conv_edit,moeda_final,cifra,ano)
    



if __name__ == '__main__':
    site.run_server(debug=True)