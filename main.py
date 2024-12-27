import streamlit as st
import os
from utils import *


def main():
    st.set_page_config(page_title="PDF Summarizer")

    st.title("PDF Summarizer App 📂💱")

    st.write("Summarize your pdf files in just a few seconds")

    # st.divider()
    st.markdown("---")  # This creates a horizontal line

    pdf = st.file_uploader("Upload your pdf document", type="pdf")

    submit = st.button("Generate summary")

    response = None

    os.environ['OPENAI_API_KEY'] = ('sk-proj'
                                    '-WW4acmCcheiUjpJE3AcW6_MVW7pzqj5FS7yHKcHHIkNUNhpdxhRLF3DFHQi0MdNTrNZhrsTs2ST3BlbkFJokjWGWoSm29z07OAPYhz6VLSM7YLq0mZD4MqLrh3wmL2S37AUhXH408I1kuY-hyazn6KcHoCcA')

    if submit and pdf:
        try:
            response = summarizer(pdf)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # if submit:
    # response = summarizer(pdf)

    st.subheader("Summary of File:")

    if response:
        st.write(response)
    else:
        st.write("Upload a file and click 'Generate Summary' to see the results.")
    # st.write(response)


if __name__ == '__main__':
    main()
