# Intro Streamlit Demo

import streamlit as st
import pandas as pd
import numpy as np

# Function to create a sample data frame and display it
def expanded_app():
    st.title("Welcome to a Streamlit Demo! 🎈")

    # ------- Displaying Text -------
    st.header("Text Presentation Showcase")

    st.subheader("Use `st.text()` for simple text:")
    st.text("This is a string of text displayed using st.text().")
    st.text("DS 3000 and CS 3200 are the best classes ever!")

    st.subheader("Using `st.markdown()` for rich text formatting:")
    st.markdown("""
        `st.markdown()` let's you embed markdown right in your output! 
        
        You can:
        * Make text **bold** or *italic*.
        * Create lists:
            * Unordered list item 1
            * Unordered list item 2
        * Or ordered lists:
            1.  Ordered list item 1
            2.  Ordered list item 2
        * Include [hyperlinks](https.streamlit.io).
        * Display images: ![Streamlit Logo](https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg)
        * Write blockquotes:
            > *To be, or not to be, that is the question.*
        * And even horizontal rules:
        ---
    """)

    st.subheader("Using `st.write()` with Markdown:")
    st.write("`st.write()` is a magic command and can also render Markdown!")
    st.write("### This is an H3 heading inside `st.write()`")
    st.write("You can **bold** text, use *italics*, and create lists:")
    st.write("- Item A from `st.write()`")
    st.write("- Item B from `st.write()`")
    st.write("1. Numbered item 1 from `st.write()`")
    st.write("2. Numbered item 2 from `st.write()`")
    st.write("Check out this link rendered by `st.write()`: [Streamlit Docs](https://docs.streamlit.io)")
    st.write("---")

    st.subheader("Displaying Headers and Subheaders:")
    st.header("This is an `st.header()`")
    st.subheader("This is an `st.subheader()`")
    st.caption("And this is `st.caption()`, useful for small text or image captions.")

    # Displaying properly syntax highlighted code is important for many 
    # apps. Notice that the code is stored in a string, and then
    # st.code is used to display it with the second param being the language. 
    st.subheader("Displaying Code Blocks with `st.code()`:")
    python_code = """
    
def greet(name):
    print(f"Hello, {name}!")

greet("Streamlit User")
    """
    st.code(python_code, language="python")

    # You can also render LaTeX in Streamlit. 
    # Notice the use of $$...$$ for block LaTeX or $...$ for inline LaTeX
    st.subheader("Displaying Mathematical Expressions with `st.latex()`:")
    st.latex(r'''
        e^{i\pi} + 1 = 0
    ''')
    st.write("""You can also include LaTeX in `st.markdown()` 
             or `st.write()` like this: $$\\frac{a}{b}$$ or 
             inline $a^2 + b^2 = c^2$.""")


    # ------ Other Data Display Elements -------
    st.header("More Data Display Options")

    # Using st.columns to display 3 metrics side by side.
    st.subheader("Use `st.metric()` to display key performance indicators (KPIs):")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Temperature", value="25 °C", delta="1.2 °C")
    col2.metric(label="Humidity", value="65%", delta="-2%")
    # Delta_color can be "normal", "inverse", or "off"
    col3.metric(label="Active Users", 
                value="1,203", 
                delta="102 since last week", 
                delta_color="off") 

    st.subheader("Using `st.json()` to display JSON data:")
    sample_json = {
        "name": "Streamlit App",
        "version": "1.2.0",
        "features": ["data display", "text formatting", "interactivity"],
        "is_awesome": True
    }
    st.json(sample_json)

    st.write("`st.json()` can also take a JSON string:")
    st.json('{"fruit": "apple", "size": "large", "color": "red"}')


    # ------ Markdown in st.write directly with variables ------
    st.header("Dynamic Markdown in `st.write`")
    st.write("""You can construct Markdown strings dynamically (adding 
             in vales from other variables) and pass them to `st.write()`.""")
    fruit_name = "Apple"
    fruit_color = "Red"
    fruit_quantity = 10

    # Notice the use of the formatted string f"""..."""
    markdown_string = f"""
    ### Fruit Inventory:

    We have **{fruit_quantity}** *{fruit_color}* _{fruit_name}_s.

    Here's a list:
    - **Name**: {fruit_name}
    - **Color**: {fruit_color}
    - **Quantity**: {fruit_quantity}
    """
    st.write(markdown_string)


# Call the expanded_app() function
if __name__ == "__main__":
    expanded_app()
