import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
      
except URLError as e:
    streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchall()
#streamlit.text("the fruit load container")
#streamlit.text(my_data_row)

#fruit_choice = streamlit.text_input('What fruit would you like to add','jackfruit')
#streamlit.write('Thanks for adding ', fruit_choice)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function = insert_row_snowflake(ass_my_fruit)
     streamlit.text(back_from_function)
    

streamlit.header("The fruit load list contains:")
#snowflake-realted functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
#add a button 
if streamlit.button('Get fruit load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


