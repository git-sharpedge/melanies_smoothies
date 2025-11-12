# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie")
st.write(
  """Choose your fruit you want in your custom Smoothie
  """
)

con = st.connection("snowflake")
session = con.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_order = st.text_input('Name on Smoothie')
st.write('The name mon your Smoothie will be: ', name_on_order)

ingredients_list = st.multiselect('Choose up to five ingredients', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
