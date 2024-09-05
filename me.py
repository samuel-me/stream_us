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

import streamlit as st
import os

def download_pdf(pdf_path):
    """Downloads a PDF from the specified path."""
    if not os.path.exists(pdf_path):
        st.error(f"PDF file '{pdf_path}' not found.")
        return

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=os.path.basename(pdf_path),
        mime="application/pdf"
    )

# Replace 'path/to/your/pdf.pdf' with the actual path to your PDF file
pdf_path = "h.pdf"

# Create a Streamlit button to trigger the download
if st.button("fonwload"):
    download_pdf(pdf_path)


#st.download_button('DOwnload button',data = 'h.csv', file_name = 'Summary.csv', mime ="text/docx")
# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")
