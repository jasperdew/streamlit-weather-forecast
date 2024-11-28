import streamlit as st
import requests
from datetime import datetime

st.title("Politie API Zoeken")

# Input velden
query = st.text_input("Zoekterm", value="amsterdam")

# Checkboxes voor type
st.subheader("Type selectie")
types = ["gezocht", "vermist", "onderwerp", "blog", "overig"]
selected_types = []
for type_option in types:
    if st.checkbox(type_option, value=True):
        selected_types.append(type_option)

# Overige parameters
sort = st.selectbox("Sortering", ["relevance", "date"], index=0)
language = st.selectbox("Taal", ["nl", "en"], index=0)
offset = st.number_input("Offset", min_value=0, value=0)

def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M")
    return "Geen datum"

if st.button("Zoeken"):
    params = {
        "query": query,
        "type": ",".join(selected_types),
        "sort": sort,
        "language": language,
        "offset": offset
    }
    
    url = "https://api.politie.nl/politie/search/v1"
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Toon zoekresultaten info
            total = data['iterator']['total']
            st.info(f"Totaal aantal resultaten: {total}")
            
            # Toon items in cards
            for item in data['items']:
                with st.container():
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### [{item['titel']}]({item['url']})")
                        st.markdown(f"*{item['type']}*")
                        st.write(item['introductie'])
                    
                    with col2:
                        st.write(f"📅 {format_date(item['publicatiedatum'])}")
                        if item.get('displayName'):
                            st.write(f"📌 {item['displayName']}")
            
            # Pagination info
            st.markdown("---")
            current_page = (offset // 10) + 1
            total_pages = (total + 9) // 10
            st.write(f"Pagina {current_page} van {total_pages}")
            
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
