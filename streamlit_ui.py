import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to call the backend for sending emails
def send_email_via_api(to, cc, bcc, subject, body):
    data = {
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "subject": subject,
        "body": body
    }
    response = requests.post("http://localhost:5000/send_email", json=data)
    return response.json()

# Function to get email status from the backend
def get_email_status():
    response = requests.get("http://localhost:5000/get_email_status")
    return response.json()

# Streamlit UI
st.title("Mass Mailing Application")

menu = ["Login", "Register", "Send Email", "Dashboard"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Register":
    st.subheader("Create a new account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")

    if password == password_confirm:
        if st.button("Register"):
            response = requests.post("http://localhost:5000/register", json={
                "username": username,
                "email": email,
                "password": password
            })
            st.success(response.json().get("message"))
    else:
        st.error("Passwords do not match.")

elif choice == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post("http://localhost:5000/login", json={
            "username": username,
            "password": password
        })
        if response.json().get("message") == "Login successful!":
            st.success(response.json().get("message"))
        else:
            st.error(response.json().get("message"))

elif choice == "Send Email":
    st.subheader("Send Email")
    to = st.text_input("To (Recipient Email)")
    cc = st.text_input("CC (Comma-separated emails)")
    bcc = st.text_input("BCC (Comma-separated emails)")
    subject = st.text_input("Subject")
    body = st.text_area("Body")

    if st.button("Send Email"):
        if to and subject and body:
            result = send_email_via_api(to, cc, bcc, subject, body)
            st.success(result["message"])
        else:
            st.error("Please fill in all required fields.")

elif choice == "Dashboard":
    st.subheader("Email Delivery Dashboard")
    status_filter = st.selectbox("Filter by Status", ["All", "Sent", "Delivered", "Landed in Inbox", "Landed in Spam"])

    # Fetch email status data
    emails = get_email_status()

    if status_filter != "All":
        emails = [email for email in emails if email['status'] == status_filter]

    # Create a DataFrame for easier visualization
    email_df = pd.DataFrame(emails)

    # Display email status table
    st.dataframe(email_df)

    # Display statistics
    st.subheader("Email Status Statistics")
    status_counts = email_df['status'].value_counts()

    # Pie chart for email status
    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Display total counts
    total_sent = len(email_df)
    delivered_count = len(email_df[email_df['status'] == 'Delivered'])
    inbox_count = len(email_df[email_df['status'] == 'Landed in Inbox'])
    spam_count = len(email_df[email_df['status'] == 'Landed in Spam'])

    st.write(f"Total Emails Sent: {total_sent}")
    st.write(f"Delivered: {delivered_count}")
    st.write(f"Landed in Inbox: {inbox_count}")
    st.write(f"Landed in Spam: {spam_count}")
