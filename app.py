import streamlit as st
from agent import research

# Page configuration 

st.set_page_config(
    page_title="AI Research Agent",
    layout="centered"
)

# Header

st.title("AI Research Agent")
st.markdown(
"""
Research any topic and receive a source-grounded AI-generated answer with citations.
"""
)
st.caption("Powered by Tavily Search + Google Gemini"
)
st.divider()

# Research input
 
st.subheader("Research question")
question = st.text_area(
    "What would you like to research?",
    placeholder=("Example: What is retrieval augmented generation?"),
    height=120
)
research_button = st.button(
    "Research",
    type="primary",
    use_container_width=True
)

# Research process

if research_button:
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        try:
            with st.spinner("Searching the web and analyzing the sources..."):
                answer, sources = research(question)

            # Answer
             
            st.success(
                f"Research completed using "
                f"{len(sources)} web sources."
            )
            st.subheader("Answer")
            st.markdown(answer)

            # Sources 

            st.divider()
            st.subheader("Sources")
            st.caption("The answer above was generated using the following web sources.")
            for source in sources:
                st.markdown(
                    f"**[{source["id"]}]** "
                    f"[{source["title"]}]({source["url"]})"
                )

        # Error Handling
         
        except Exception as error:
            st.error(
                f"Research failed: {error}"
            )

# Footer

st.divider()
st.caption("AI Research agent | Web research powered by Tavily | Answer generation powered by Google Gemini")