import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime
import pandas as pd
#url = "https://docs.google.com/spreadsheets/d/1S7zTgFp66suc3J583pTQJXKcNUgRfzvJC5XG45DXbxs/edit?gid=0#gid=0"
st.title("Payments-Tracker")
st.markdown("Rayyan's personal account keeper!")

conn=st.connection("gsheets", type=GSheetsConnection)

existing_data=conn.read(worksheet="daily", usecols=list(range(5)), ttl=5)


Mode = [
    "UPI",
    "CASH",
    "CARD",
]

def clear_fields():
    st.session_state['mode_payment']=' '
    st.session_state['amount_payment']=' '
    st.session_state['reason_payment']=' '
    st.session_state['comments_payment']=' '

with st.form(key="payments_tracker"):
    selected_date =st.date_input(label="Select a Date")
    mode_payment=st.selectbox("Mode of Payment",options=Mode, index=None)
    amount_payment=st.text_area(label="Amount")
    reason_payment=st.text_area(label="Reason")
    comments_payment=st.text_area(label="Comments")
    
    submit_button = st.form_submit_button("Add Payment")
    clear_button = st.form_submit_button(label='Clear all fields')
    if clear_button:
        clear_fields()
        st.rerun()
    if submit_button:
        
        if not mode_payment or not Mode:
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
