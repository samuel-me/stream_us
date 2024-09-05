import streamlit as st  # pip install streamlit

st.header(":mailbox: Get In Touch With Me!")


contact_form = """
<form action="https://formsubmit.co/DAILOAYOMIDE@GMAIL.COM" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)


#st.download_button('DOwnload button',data = 'h.csv', file_name = 'Summary.csv', mime ="text/docx")
# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")
