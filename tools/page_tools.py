import streamlit as st
import base64


#########################################################################################################################
# Layout and Previse look and feel

# getting the image file for the logo - encoding it ourselves because streamlit is really blurring it too much...
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def streamlit_previsify(png_file = "./logo_title.png"):
    """ makes the streamlit app look like a Previse app.
    """
# Load the CSS from the file
    with open("./mystyle.css") as myfile:
        st.markdown(f"<style>{myfile.read()}</style>", unsafe_allow_html=True)

    bin_str = get_base64_of_bin_file(png_file)
    footer_bg_img = """
                <style>
                .css-1dp5vir { 
                    position: absolute;
                    top: 0px;
                    right: 0px;
                    left: 0px;
                    height: 0.125rem;
                    background-image: linear-gradient(90deg, #fedb00, #fedb00);
                    z-index: 999990;
                }
                footer { 
                   visibility: hidden;
                }
                header{ 
                    padding: 0.5rem;
                }
                header:after {
                    display: block;
                    content: "";
                    width: 94%%;
                    height: 80%%;
                    position: absolute;
                    background-image: url("data:image/png;base64,%s");
                    background-position-x: 95%%;
                    background-position-y: 0%%;
                    background-repeat: no-repeat;
                    background-size: contain;
                    background_attachment: fixed;
                    }
                </style>
                """ % bin_str
    st.markdown(footer_bg_img, unsafe_allow_html=True)
