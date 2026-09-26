import streamlit as st
from agent import research
st.set_page_config(
    page_title="AI Research Agent",
    layout="centered"
)
st.title("AI Reseaech Agent")
st.write("Ask a research question and get an AI-generated answer grounded in web sources.")
question = st.text_area(
    "Enter your research question: ",
    placeholder="Example: What is retrieval augmented generation?"
)
research_button = st.button(
    "Research",
    type="primary"
)
if research_button:
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        try:
            with st.spinner("Researching the web..."):
                answer, sources = research(question)
            st.subheader("Answer")
            st.markdown(answer)
            st.subheader("Sources")
            for source in sources:
                st.markdown(
                    f"**[{source["id"]}]** "
                    f"[{source["title"]}]({source["url"]})"
                )
        except Exception as error:
            st.error(str(error))