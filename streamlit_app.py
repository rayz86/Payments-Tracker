import streamlit as st
from st_gsheets_connection import connect
import datetime
import pandas as pd
#url = "https://docs.google.com/spreadsheets/d/1S7zTgFp66suc3J583pTQJXKcNUgRfzvJC5XG45DXbxs/edit?gid=0#gid=0"
st.title("Payments-Tracker")
st.markdown("Rayyan's personal account keeper!")

if "mode_payment" not in st.session_state:
    st.session_state["mode_payment"] = "Select Mode"
conn=connect("gsheets")

existing_data=conn.read(worksheet="daily", usecols=list(range(5)), ttl=5)


Mode = [
    "Select Mode",
    "UPI",
    "CASH",
    "CARD",
]

def clear_fields():
    st.session_state['mode_payment']='Select Mode'
    st.session_state['amount_payment']=''
    st.session_state['reason_payment']=''
    st.session_state['comments_payment']=''

with st.form(key="payments_tracker"):
    selected_date = st.date_input("Select a Date", value=datetime.date.today())
    mode_payment = st.selectbox("Mode of Payment", options=Mode, index=Mode.index(st.session_state.get("mode_payment")))
    amount_payment = st.text_area("Amount", value=st.session_state.get("amount_payment", ""))
    reason_payment = st.text_area("Reason", value=st.session_state.get("reason_payment", ""))
    comments_payment = st.text_area("Comments", value=st.session_state.get("comments_payment", ""))
    
    submit_button = st.form_submit_button("Add Payment")
    clear_button = st.form_submit_button(label='Clear all fields')
    if clear_button:
        clear_fields()
        
    if submit_button:
        
        if mode_payment == "Select Mode" or not amount_payment.strip() or not reason_payment.strip():
            st.warning("Ensure all mandatory fields are filled!")
            st.stop()
            
        else:
            new_data = pd.DataFrame(
                [
                    {
                        "Date": selected_date,
                        "Mode of Payment": mode_payment,
                        "Amount": amount_payment,
                        "Reason": reason_payment,
                        "Comments": comments_payment,
                    }
                ]
            )
            update_df=pd.concat([existing_data, new_data], ignore_index=True)
            
            conn.update(worksheet="daily", data=update_df)
            
            st.success("New field added!")
