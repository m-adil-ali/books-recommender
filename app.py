import streamlit as st
import pickle as pkl
import pandas as pd
import numpy as np

popular_df = pkl.load(open('data/popular.pkl','rb'))
pt = pkl.load(open('data/pt.pkl','rb'))
books = pkl.load(open('data/books.pkl','rb'))
similarity_scores = pkl.load(open('data/similarity_scores.pkl','rb'))

st.sidebar.title("Navigation")
page= st.sidebar.radio("Go to", ["Top 50 Books","Recommended Books",])

if page=="Top 50 Books":
    st.title("Top 50 Books")
    st.markdown("---")
    
    
    # Number of images per row
    images_per_row = 5

    # Loop through the DataFrame in chunks
    for start in range(0, len(popular_df), images_per_row):
        end = start + images_per_row
        row_data = popular_df.iloc[start:end]

        # Create columns for the current row
        cols = st.columns(images_per_row)

        for col, (index, row) in zip(cols, row_data.iterrows()):
            image_url = row['Image-URL-M']
            col.image(image_url, caption=f"{row['Book-Title']} \nAuthor: {row['Book-Author']}\nRatings: {row['num_ratings']}, \nAvg Rating: {round(row['avg_rating'],1)}", width=100)
        st.markdown("---")
    
if page=="Recommended Books":
    st.title("Recommended Books")
    st.markdown("---")
    
    with st.form(key= 'my_form'):
        input = st.text_input("Enter any book name you are interested in like (The Handmaid's Tale, Animal Farm, 1984, etc)")
        submit_button = st.form_submit_button(label='Submit')
    
        if submit_button:
            similar_items = []
                    # Check if input is empty
            if not input:
                st.warning("Please write a book name.")
            else:
                user_input = input  
                # Check if the user input exists in the index
                if user_input not in pt.index:
                    st.warning("Book not found. Please enter a valid book name.")
                else:
                    index = np.where(pt.index == user_input)[0][0]
                    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

                    # Create a layout for displaying similar items
                    st.markdown("---")
                    cols = st.columns(5)  # Create 5 columns for the images
                    for i, col in zip(similar_items, cols):
                        item_index = i[0]
                        temp_df = books[books['Book-Title'] == pt.index[item_index]]

                        # Extracting the necessary information
                        image_url = temp_df['Image-URL-M'].values[0]  # Assuming there's only one unique image URL per book
                        book_title = temp_df['Book-Title'].values[0]
                        book_author = temp_df['Book-Author'].values[0]

                        # Display the image and details in the column
                        col.image(image_url, caption=f"{book_title} by {book_author}", width=100)