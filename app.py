import streamlit as st
import sqlite3

# Page configuration
st.set_page_config(
    page_title="Student Feedback App",
    page_icon="📝",
    layout="centered"
)

# Database connection
conn = sqlite3.connect("feedback.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
message TEXT
)
""")

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Submit Feedback", "View Feedback", "Admin"]
)

# App title
st.title("📝 Student Feedback App")

# ------------------------
# Submit Feedback Page
# ------------------------
if page == "Submit Feedback":

    st.header("Submit Your Feedback")

    with st.form("feedback_form"):

        name = st.text_input("👤 Your Name")
        message = st.text_area("💬 Your Feedback")

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if name.strip() == "" or message.strip() == "":
                st.warning("⚠️ Please fill in both fields before submitting.")
            else:
                cursor.execute(
                    "INSERT INTO feedback (name, message) VALUES (?, ?)",
                    (name, message)
                )
                conn.commit()
                st.success("✅ Feedback submitted successfully!")

# ------------------------
# View Feedback Page
# ------------------------
elif page == "View Feedback":

    st.header("📢 All Feedback")

    cursor.execute("SELECT * FROM feedback")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            st.markdown(f"**👤 {row[1]}**")
            st.write(f"💬 {row[2]}")
            st.markdown("---")
    else:
        st.info("No feedback yet. Be the first!")

# ------------------------
# Admin Panel
# ------------------------
elif page == "Admin":

    st.header("🔒 Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "Sau_123":

        cursor.execute("SELECT * FROM feedback")
        rows = cursor.fetchall()

        if rows:
            for row in rows:

                col1, col2 = st.columns([4,1])

                with col1:
                    st.markdown(f"**👤 {row[1]}**")
                    st.write(f"💬 {row[2]}")

                with col2:
                    if st.button("Delete", key=row[0]):
                        cursor.execute(
                            "DELETE FROM feedback WHERE id=?",
                            (row[0],)
                        )
                        conn.commit()
                        st.rerun()

                st.markdown("---")

        else:
            st.info("No feedback available.")

    elif password != "":
        st.error("❌ Incorrect password")