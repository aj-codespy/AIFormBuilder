import streamlit as st
import pandas as pd
from main import formGenerator
import ast

st.title('AI Form Builder')

# Sidebar Navigation
page = st.sidebar.selectbox("Choose a page:", ["Generate Form", "Edit Questions"])

if "form_data" not in st.session_state:
    st.session_state.form_data = None
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Generate Form Page
if page == "Generate Form":
    purpose = st.text_input('Enter the form description: ')
    objective = st.text_input('Enter the form objective: ')
    target_aud = st.text_input('Enter the target audience: ')
    number = st.text_input('Enter the number of questions: ')
    inputtype = st.text_input('Enter the type of questions (e.g., Slider, Multi-choice, etc): ')

    if st.button('Generate', key="generate_button"):
        form = formGenerator(purpose, objective, target_aud, number, inputtype)
        st.session_state.form_data = ast.literal_eval(form[10:len(form) - 4].strip())
        st.session_state.responses = {f"q{i}": None for i in range(len(st.session_state.form_data))}

    if st.session_state.form_data:
        for i, arr in enumerate(st.session_state.form_data):
            unique_key = f"q{i}"
            question, input_type = arr[0], arr[1]

            if input_type == 'Slider' and len(arr) >= 4:
                st.session_state.responses[unique_key] = st.slider(
                    question,
                    min_value=arr[2],
                    max_value=arr[3],
                    key=f"{unique_key}_slider"
                )
            elif input_type == 'Likert Scale' or 'Likert' in input_type:
                st.session_state.responses[unique_key] = st.radio(
                    question,
                    options=[1, 2, 3, 4, 5],
                    key=f"{unique_key}_likert"
                )
            elif input_type == 'Multiple Choice' and len(arr) > 2:
                options = arr[2:]
                st.session_state.responses[unique_key] = st.multiselect(
                    question,
                    options,
                    key=f"{unique_key}_multichoice"
                )
            elif input_type == 'Textbox':
                st.session_state.responses[unique_key] = st.text_input(
                    question,
                    key=f"{unique_key}_textbox"
                )
            else:
                st.warning(f"Invalid input type or insufficient data for question {i + 1}. Defaulting to Textbox.")
                st.session_state.responses[unique_key] = st.text_input(
                    question,
                    key=f"{unique_key}_fallback"
                )

        if st.button("Download Responses as CSV", key="download_csv_button"):
            questions = [arr[0] for arr in st.session_state.form_data]
            answers = [st.session_state.responses[f"q{i}"] for i in range(len(st.session_state.form_data))]
            csv_data = pd.DataFrame({"Question": questions, "Answer": answers})
            csv_file = csv_data.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download CSV",
                data=csv_file,
                file_name="responses.csv",
                mime="text/csv",
                key="csv_download_button"
            )

# Edit Questions Page
elif page == "Edit Questions":
    if st.session_state.form_data:
        question_numbers = list(range(1, len(st.session_state.form_data) + 1))
        selected_question = st.selectbox("Select Question Number to Edit:", question_numbers, key="edit_selectbox")

        if selected_question:
            question_index = selected_question - 1
            question_data = st.session_state.form_data[question_index]

            updated_question = st.text_input("Edit Question:", value=question_data[0], key="edit_question_input")

            input_types = ["Slider", "Likert Scale", "Multiple Choice", "Textbox"]
            cleaned_input_type = question_data[1].strip() if isinstance(question_data[1], str) else ""
            if cleaned_input_type not in input_types:
                cleaned_input_type = input_types[0]

            updated_input_type = st.selectbox(
                "Edit Input Type:",
                input_types,
                index=input_types.index(cleaned_input_type),
                key="edit_input_type_selectbox"
            )

            additional_data = []
            if updated_input_type == "Slider":
                min_value = st.number_input("Minimum Value:", value=question_data[2], key="edit_slider_min")
                max_value = st.number_input("Maximum Value:", value=question_data[3], key="edit_slider_max")
                additional_data = [min_value, max_value]
            elif updated_input_type == "Multiple Choice":
                choices = st.text_area("Enter Choices (comma-separated):", value=", ".join(question_data[2:]), key="edit_choices_textarea")
                additional_data = choices.split(", ")

            if st.button("Update Question", key="update_question_button"):
                new_question_data = [updated_question, updated_input_type] + additional_data
                st.session_state.form_data[question_index] = new_question_data
                st.success("Question updated successfully!")
    else:
        st.warning("No form data found. Please generate a form first.")

print(st.session_state.form_data)
