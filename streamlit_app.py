# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smotthie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie
    """)

cnx = st.connection("snowflake")

name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredientes:'
    , my_dataframe
    , max_selections=5
    )

if ingredients_list:
    ingredients_string = ""    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
    
    #st.write(ingredients_string)
    my_insert_stmt = f"""INSERT INTO smoothies.public.ORDERS(name_on_order, ingredients) 
            values ('{name_on_order}', '{ingredients_string}')"""

    time_to_insert = st.button('Submit Order')

    if ingredients_list and time_to_insert and name_on_order:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
