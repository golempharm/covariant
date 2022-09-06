import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pandas_bokeh
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource

#st.title('Variant analysis')
st.write("[Go to main](https://piotrkarabowicz.github.io/variantbase/)")
st.markdown("<h1 style='text-align: center; color: black;'>Variant counter</h1>", unsafe_allow_html=True)
st.write('')
#st.write('See, how to use the analyzer:')
#st.video("/home/piotr/Videos/output_last2.mp4")
st.write('')

try:
 st.markdown("<h3 style='text-align: center; color: black;'>Load data</h3>", unsafe_allow_html=True)
 data1 = st.file_uploader("Load data from GISAID", type=["tsv", "txt"]) 				#laduje dane

 df_iz2 = pd.read_csv(data1, sep = '\t') 			#konweruje na Dataframe

 df_iz = df_iz2[['strain', 'date', 'country', 'division','location', 'age', 'sex','pangolin_lineage','GISAID_clade', 'originating_lab', 'submitting_lab', 'date_submitted']] 			#wybiera odpowiednie kolumny

 db_iz = pd.DataFrame(df_iz.groupby(['pangolin_lineage', 'date']).size(), columns = ['count'])			#grupuje wg lini virusa i daty dodania
 db_iz.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny

 dat_final = db_iz.sort_values(by=['date'], ascending=True)	 #sortowanie wg daty

 dat_final = dat_final[dat_final['count'] >10]

 #wykres
 selection = alt.selection_multi(fields=['pangolin_lineage'], bind='legend')


 chart_waw = alt.Chart(dat_final).mark_line(point=True).encode(
    x ='date',
    y='count',
    color='pangolin_lineage',
    strokeDash='pangolin_lineage',
    order='date',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).interactive().properties(
    width=800,
    height=500
 ).add_selection(selection)
 st.markdown("<h3 style='text-align: center; color: black;'>Results</h3>", unsafe_allow_html=True)
 st.write('')
 st.write('Plot: variants count - date (variant count > 10)')
 chart_waw
 st.write('')
 st.write('Table: variants count - date (variant count > 10)')
 dat_final

 db_iz1 = pd.DataFrame(df_iz2.groupby(['country', 'pangolin_lineage', ]).size(), columns = ['count'])			#grupuje wg lini virusa i kraju
 db_iz1.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz1.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz1 = db_iz1[db_iz1['count']>10]

 st.write('')
 st.write('Plot: variants count - country (variant count > 10)')

 chart_c = alt.Chart(db_iz1).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
    ).encode(
    x='count',
    y='country',
    color='pangolin_lineage',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).properties( width=800,
    height=500).add_selection(selection)
 chart_c
 st.write('')
 st.write('Table: variants count - country (variant count > 10)')
 db_iz1
 st.write("[Go back](https://pkarabowicz.wixsite.com/golempharm)")
except:
 pass
