import json
import streamlit as st
import pandas as pd
from millify import millify
from streamlit_echarts import st_echarts
from streamlit_echarts import Map



st.set_page_config(page_title="Dashboard", layout ="wide")

@st.cache
def load_excel():
    df = pd.read_excel('data.xlsx',engine='openpyxl',sheet_name='Data',usecols='A:T')
    df['OrderDate']= pd.to_datetime(df['Order Date']).dt.strftime('%d-%b-%Y')
    df['year']= pd.to_datetime(df['OrderDate']).dt.strftime('%Y')
    df['month']= pd.to_datetime(df['OrderDate']).dt.strftime('%b')
    return df 

df = load_excel()



# SideBar
with st.sidebar:
    lg = st.container()
    lg.image("logo.png", width=150)
  

year = st.sidebar.multiselect(
    "Select the year", 
    options = df.year.unique(),
    default = df.year.unique()
)

#month = st.sidebar.multiselect(
#    "select the mounth", 
#    options = df.month.unique(),
#    default = df.month.unique()
#)
Category = st.sidebar.multiselect(
    "Select the Category", 
    options = df.Category.unique(),
    default = df.Category.unique()
)





df_selection = df.query('Category==@Category & year==@year')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image("1.png", width=60)
    st.metric("Chiffre d'affaire", millify(df_selection.Sales.sum(), precision=2))
with col2:
    st.image("2.png", width=60)
    st.metric("# commandes", millify(df_selection['Order ID'].nunique(), precision=2))
with col3:
    st.image("3.png", width=60)
    st.metric("Bénéfices", millify(df_selection['Profit'].sum(), precision=2))
with col4:
    st.image("4.png", width=60)
    st.metric("Produits", millify(df_selection['Product ID'].nunique(), precision=2))


cols1,cols2= st.columns([2,2])
with cols1:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_selection['month'] = pd.Categorical(df_selection['month'], categories=months, ordered=True)
    a = df_selection.groupby(['year','month'])['Order ID'].nunique().unstack()

    lines = []
    line = {}


    for i in a.index:
        line["name"] = i
        line["type"] = 'line'
        line["smooth"] = 'True'
        line["data"] = a.loc[i, :].values.tolist()
        lines.append(line.copy())
        
    option = {
        'title': {
        'text': '# Commandes Par Mois'
    },
    'tooltip': {
        'trigger': 'axis'
    },
    'legend': {
        'data': a.index.tolist(),
        'orient': 'vertical',
        'right': '3%',
        'top':'10%'
    },
    'grid': {
        'left': '0%',
        'right': '15%',
        'bottom': '3%',
        'containLabel': True
    },
        "xAxis": {
        "type": 'category',
        "data": ['Jan', 'Feb', 'Mar', 'May', 'Apr', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']
        },
        "yAxis": {
        "type": 'value'
        },
        "series": lines
        }
    st_echarts(options=option, key="chart")

with cols2:
    df_selection['month'] = pd.Categorical(df_selection['month'], categories=months, ordered=True)
    a = df_selection.groupby(['year','month'])['Profit'].sum().unstack()

    lines = []
    line = {}

    for i in a.index:
        line["name"] = i
        line["type"] = 'bar'
        line["stack"] = 'total'
        line["data"] = a.loc[i, :].values.tolist()
        lines.append(line.copy())
    
    option = {
    'title': {
    'text': 'Profit par mois'
    },
  'tooltip': {
    'trigger': 'axis'
  },
  'legend': {
    'data': a.index.tolist(),
    'orient': 'vertical',
        'right': '3%',
        'top':'10%'
  },
  'grid': {
    'left': '0%',
    'right': '15%',
    'bottom': '3%',
    'containLabel': True
  },
    "xAxis": {
    "type": 'category',
    "data": ['Jan', 'Feb', 'Mar', 'May', 'Apr', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']
    },
    "yAxis": {
    "type": 'value'
    },
    "series": lines
    }
    st_echarts(options=option,key="chart1")    

col1, col2,col3,col4 = st.columns(4)
with col1:
    counts  = df_selection.groupby('Category')['Order ID'].nunique().reset_index()
    counts.rename(columns = {'Category':'name', 'Order ID':'value'}, inplace = True)
    op = {
    "title": {
        "text": '# commande par category',
        'textStyle':{
            "fontSize": 14
        },   
        "top" :"10%",   
        "left": 'center'
    },
    "legend": {
        "bottom": 'bottom',
        "left": 'center',
        'data': counts.name.tolist()
    },
    "series": [
        {
      "name": "Segement",
      "type": 'pie',
      "radius": ['45%', '60%'],
      'avoidLabelOverlap' : True,
      "label": {
        'position': 'center',
        "show": False,
        "formatter": '{d}% \n \n  {b}'
      },
      "emphasis": {
        "label": {
          "show": True,
          "fontSize": '14',
          "fontWeight": 'bold'
        }
      },
      "labelLine": {
        "show": False
      }, 
            "data": counts.to_dict('records')}
        ],
    }
    st_echarts(options=op,key="chart2")

with col2:
    counts  = df_selection.groupby('Ship Mode')['Order ID'].nunique().reset_index()
    counts.rename(columns = {'Ship Mode':'name', 'Order ID':'value'}, inplace = True)
    op = {
    "title": {
        "text": '# commande par Ship Mode',
        'textStyle':{
            "fontSize": 14
        },   
        "top" :"10%",   
        "left": 'center'
    },
    "legend": {
        "bottom": 'bottom',
        "left": 'center'
    },
    "series": [
        {
      "name": "Segement",
      "type": 'pie',
      "radius": ['45%', '60%'],
      "avoidLabelOverlap": False,
      "label": {
        "show": False,
        "position": 'center',
        "formatter": '{d}% \n \n  {b}'
      },
      "emphasis": {
        "label": {
          "show": True,
          "fontSize": '14',
          "fontWeight": 'bold'
        }
      },
      "labelLine": {
        "show": False
      }, 
            "data": counts.to_dict('records')}
        ],
    }
    st_echarts(options=op,key="chart3")


with col3:
    counts  = df_selection.groupby('Segment')['Order ID'].nunique().reset_index() 
    counts.rename(columns = {'Segment':'name', 'Order ID':'value'}, inplace = True)
    options = {
    "title": {
        "text": '# commande par segement',
        'textStyle':{
            "fontSize": 14
        },   
        "top" :"10%",   
        "left": 'center'
    },
    "legend": {
        "bottom": 'bottom',
        "left": 'center'
    },
    "series": [
        {
      "name": "Segement",
      "type": 'pie',
      "radius": ['45%', '60%'],
      "avoidLabelOverlap": False,
      "label": {
        "show": False,
        "position": 'center',
        "formatter": '{d}% \n \n  {b}'
      },
      "emphasis": {
        "label": {
          "show": True,
          "fontSize": '14',
          "fontWeight": 'bold'
        }
      },
      "labelLine": {
        "show": False
      }, 
            "data": counts.to_dict('records')}
        ],
    }
    st_echarts(options=options,key="chart4")

with col4:
    counts  = df_selection.groupby('Region')['Order ID'].nunique().reset_index()
    counts.rename(columns = {'Region':'name', 'Order ID':'value'}, inplace = True)
    
    opp = {
    "title": {
        "text": '# commande par Region',
        'textStyle':{
            "fontSize": 14
        },   
        "top" :"10%",   
        "left": 'center'
    },
    "legend": {
        "bottom": 'bottom',
        "left": 'center',
        'data': counts.name.tolist()
    },
    "series": [
        {
      "name": "Segement",
      "type": 'pie',
      "radius": ['45%', '60%'],
      'avoidLabelOverlap' : True,
      "label": {
        'position': 'center',
        "show": False,
        "formatter": '{d}% \n \n  {b}'
      },
      "emphasis": {
        "label": {
          "show": True,
          "fontSize": '14',
          "fontWeight": 'bold'
        }
      },
      "labelLine": {
        "show": False
      }, 
            "data": counts.to_dict('records')}
        ],
    }
    st_echarts(options=opp,key="chart5")


cols1,cols2= st.columns([2,2])
with cols1:
    prf_state = df_selection.groupby(['State'])['Order ID'].nunique().reset_index()  
    prf_state.rename(columns = {'State':'name', 'Order ID':'value'}, inplace = True)          
    #st.bar_chart(prf_state)

    #fig = px.bar(prf_state, x='State', y='Profit',color='year',
    #            labels={'pop':'population of Canada'},width=900)
    #st.plotly_chart(fig)

    with open("./USA.json", "r") as f:
        map = Map(
            "USA",
            json.loads(f.read()),
            {
                "Alaska": {"left": -131, "top": 25, "width": 15},
                "Hawaii": {"left": -110, "top": 28, "width": 5},
                "Puerto Rico": {"left": -76, "top": 26, "width": 2},
            },
        )
    opt = {
    "title": {
      "text": '# commande par state',
      "left": '5%'
    },
    "tooltip": {
      "trigger": 'item',
      "showDelay": 0,
      "transitionDuration": 0.2
    },
    "visualMap": {
      "left": 'right',
      "inRange": {
        "color": [
          '#313695',
          '#4575b4',
          '#74add1',
          '#abd9e9',
          '#e0f3f8',
          '#ffffbf',
          '#fee090',
          '#fdae61',
          '#f46d43',
          '#d73027',
          '#a50026'
        ]
      },
      "text": ['High', 'Low'],
      "calculable": True
    },
    "toolbox": {
      "show": True,
      "orient": 'horizontal',
      "right": 'right',
      "top": 'top',
      "feature": {
        "dataView": { "readOnly": False },
        "restore": {},
        "saveAsImage": {}
      }
    },
    "series": [
      {
        "name": 'USA PopEstimates',
        "type": 'map',
        "map": 'USA',
        "emphasis": {
          "label": {
            "show": True
          }
        },
    "data":prf_state.to_dict('records')}
     ],
    }
    st_echarts(options=opt,map=map,width="300",key="chart6")

with cols2:
    counts  = df_selection.groupby('Sub-Category')['Order ID'].nunique().reset_index()
    counts.rename(columns = {'Sub-Category':'name', 'Order ID':'value'}, inplace = True)

    option = {
    "title": {
      "text": '# commande par sub category',
      "left": '5%'
    },
    'grid': {'left':"25%", 'right':"10%"},
    'xAxis': {
        'type': 'category',
        'data':counts.name.tolist(),
        'axisLabel': {
        'show': True,
        'interval': 0,
        'rotate': 90
      }
     },
    'yAxis': {
        'type': 'value',
        "show" :False     
    },
    'series': [
    {
      'data': counts.value.to_list(),
      'type': 'bar',
       'label': {
        'position': 'top',
        'show': True
      },
      'showBackground': True,
      'backgroundStyle': {
        'color': 'rgba(180, 180, 180, 0.2)'
      }
    }
    ]
    }
    st_echarts(options=option,key="chart7")





col1, col2= st.columns(2)

with col1:
    a= df_selection.groupby(['Customer ID','Customer Name'])['Order ID'].nunique().reset_index()  
    a.sort_values(by='Order ID', ascending=False,inplace=True)
    a.reset_index(drop=True, inplace=True)
    ys= a['Customer Name'].to_list()
    xs = a['Order ID'].to_list()

    option = {
    "title": {
      "text": 'TOP 5 custmer',
      "left": '5%'
    },
    'grid': {'left':"25%", 'right':"10%"},
    'xAxis': {
        'type': 'value'
     },
    'yAxis': {
        'type': 'category',
        'data': (ys[:5].copy())[::-1],
        'axisLabel': {
             'width': 200,
          }
    },
    'series': [
    {
      'data': (xs[:5].copy())[::-1],
      'type': 'bar',
       'label': {
        'position': 'right',
        'show': True
      },
      'showBackground': True,
      'backgroundStyle': {
        'color': 'rgba(180, 180, 180, 0.2)'
      }
    }
    ]
    }
    st_echarts(options=option,key="chart8")

    
with col2:
    a= df_selection.groupby(['Product ID','Product Name'])['Order ID'].nunique().reset_index()  
    a.sort_values(by='Order ID', ascending=False,inplace=True)
    a['Product Name'] = a['Product Name'].str[:20]
    a.reset_index(drop=True, inplace=True)
    
    ys= a['Product Name'].to_list()
    xs = a['Order ID'].to_list()

    option = {
    "title": {
      "text": 'Top 5 product',
      "left": '5%'
    },
    'grid': {'left':"25%", 'right':"10%"},
    'xAxis': {
        'type': 'value'
     },
    'yAxis': {
        'type': 'category',
        'data': (ys[:5].copy())[::-1],
        'axisLabel': {
             'width': 200,
          }
    },
    'series': [
    {
      'data': (xs[:5].copy())[::-1],
      'type': 'bar',
       'label': {
        'position': 'right',
        'show': True
      },
      'showBackground': True,
      'backgroundStyle': {
        'color': 'rgba(180, 180, 180, 0.2)'
      }
    }
    ]
    }
    st_echarts(options=option,key="chart9")



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css?family=Open+Sans');
div[data-testid="metric-container"] {
  margin: 0px auto;
  max-width: 300px;
  border-radius: 10px;
  border-width: 1px;
  border-style: solid;
  border-color="#777";
  overflow: hidden;
  background-clip: padding-box;
  padding: 15px 5px 15px 40%;
  text-align: left;
  font-weight: 400 !important;
  font-family: Open sans;
  color: #566a7f;
  
}


}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    font-family: Open sans;
    font-size:calc(1.2875rem + 0.45vw);
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
.css-1r6slb0{
  background-clip: padding-box;
  padding: 30px 15px;
  border-radius: 10px;
    background-color: #fff;
}

.css-1adrfps{
    width: 17rem;
    background-color: #fff;
    border-radius: 0.5rem;
}

.css-18e3th9 {
    background-color: #f5f5f9;
    padding-left: 1rem;
    padding-right: 1rem;
    padding: 3rem 1rem 3rem;
}
.e8zbici2{
    top: -50px;
}

.css-1kyxreq {
  padding-left: 50PX;
}

.css-1adrfps{
    padding-top: 50PX;
}



.css-6awftf ~ .css-1kyxreq {  position: absolute;
    top: 35px;
    left: -35px;}

</style>
"""
, unsafe_allow_html=True)

