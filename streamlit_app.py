import streamlit as st

st.title("Burger App :hamburger:")
st.markdown("### Best Burgers in Town, One Click Away 🍟😋")

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


st.button("Order Now")
