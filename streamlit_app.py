import streamlit as st
import sqlite3

@st.cache_resource
def get_connection():
    return sqlite3.connect("transaction.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT UNIQUE,
    age_group TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)

""")

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        items TEXT,
        total_amount INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
        )
""")

conn.commit()

st.title("Burger App :hamburger:")
st.markdown("### Best Burgers in Town, One Click Away 🍟😋")

phone = st.text_input("Phone Number ? ")

if phone:
    if not phone.isdigit() or len(phone) != 10:
        st.error("Please enter a valid 10 digit phone number")
    else:
        cursor.execute(
            """
            SELECT customer_id, name from customers WHERE phone=?
            """,(phone,)
        )

        customer = cursor.fetchone()

        if customer:
            st.write(f"Welcome Back! {customer[1]}")
        else:
            name = st.text_input("Your Name ?")
            age = st.selectbox("Age Group",[ "Under 13","13-17","18-25","26-35","36-50","50+"])

st.text("📋 Menu")

col1,col2,col3 = st.columns(3)

with col1:
    st.image("https://images.pexels.com/photos/33502810/pexels-photo-33502810.jpeg",width=200)
    Burger_count = st.number_input("Company Burger @120",min_value=0,max_value=10,step=1,key="burger")


with col2:
    st.image("https://images.pexels.com/photos/5695616/pexels-photo-5695616.jpeg",width=200)
    Fries_count = st.number_input("Frenchie Fries @100",min_value=0,max_value=10,step=1,key="fries")

with col3:
    st.image("https://images.pexels.com/photos/36782573/pexels-photo-36782573.jpeg",width=200)
    Nugget_count = st.number_input("Nuggets of Chicken @180",min_value=0,max_value=10,step=1,key="nuggets")

col4,col5,col6 = st.columns(3)

with col4:
    st.image("https://images.pexels.com/photos/15205136/pexels-photo-15205136.jpeg",width=200)
    Coke_count = st.number_input("Coke Ka Cola @100",min_value=0,max_value=10,step=1,key="coke")

with col5:
    st.image("https://images.pexels.com/photos/12635411/pexels-photo-12635411.jpeg",width=200)
    Softy_count = st.number_input("Soft C Softy @80",min_value=0,max_value=10,step=1,key="softy")

with col6:
    st.image("https://images.pexels.com/photos/15476368/pexels-photo-15476368.jpeg",width=200)
    VegBurg_count = st.number_input("Veggie Veg Burger@ 90",min_value=0,max_value=10,step=1,key="vegburger")

menu_items={
    "Company Burgers": Burger_count,
    "Frenchie Fries": Fries_count,
    "Nuggets of Chicken": Nugget_count,
    "Coke Ka Cola": Coke_count,
    "Soft C Softy": Softy_count,
    "Veggie Veg Burger": VegBurg_count
}

prices = {
    "Company Burgers": 120,
    "Frenchie Fries": 100,
    "Nuggets of Chicken": 180,
    "Coke Ka Cola": 100,
    "Soft C Softy": 80,
    "Veggie Veg Burger": 90
}

items = []

for item_name,count in menu_items.items():
    if count>=1:
        items.extend([item_name] * count)


st.write(f"🛒 Cart : ({len(items)} items :arrow_down: )",items)


st.markdown(" ##  :memo: Order Summary")
amt = 0
for item_name,count in menu_items.items():
    if count>=1:
        st.write(f"{count}x {item_name}")
        amt = amt + prices[item_name]*count


st.write(f"Total Amount: {amt} ")




st.button("Order Now")
