import streamlit as st
import polars as pl
from pathlib import Path

st.set_page_config(
    page_title='Data Dashboard',
    layout='wide'
)

DATA_PATH = Path(__file__).resolve().parents[1]/'data'/'processed_data.csv'

@st.cache_data
def load_data():
    return pl.read_csv(DATA_PATH)

df = load_data()

# =======================
# HEADER
# =======================
st.title('Life Expectancy Dashboard')
st.markdown('Analysis of life expectancy since 1950')

# =======================
# SIDEBAR
# =======================
st.sidebar.header('Filters')

countries = sorted(df['Country'].unique().to_list())
selected_country = st.sidebar.selectbox(
    'Select a Country',
    countries,
    index=countries.index('Brazil') if 'Brazil' in countries else 0
)

# =======================
# FILTERING
# =======================
df_country = df.filter(pl.col('Country') == selected_country)
df_country.with_columns(
    pl.col('Year').cast(str)
)

# =======================
# METRICS
# =======================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        'Average expectation',
        round(df_country['life_expectancy (Years)'].mean(), 2)
    )

with col2:
    st.metric(
        'Max',
        df_country['life_expectancy (Years)'].max()
    )

with col3:
    st.metric(
        'Min',
        df_country['life_expectancy (Years)'].min()
    )

# =======================
# GRAPHIC
# =======================
st.subheader(f'Evolution of life expectancy — {selected_country}')
st.line_chart(
    df_country.select(['Year', 'life_expectancy (Years)']).to_pandas(),
    x='Year',
    y='life_expectancy (Years)'
)

# =======================
# TABLE
# =======================
st.subheader('Historic Data')
st.dataframe(df_country.to_pandas(), use_container_width=True)