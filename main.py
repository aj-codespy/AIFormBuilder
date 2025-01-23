from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv
import ast
import json

load_dotenv()

def structConverter(questions):
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        temperature=0,
        api_key='AIzaSyDk27PsOo83ck8c15ql80R1xXwmK2-NG_s',
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''Your task is to strictly return output as a 2D array following these rules:
Each sub-array represents one question.
The first element of each sub-array is the question text.
The second element is the input type:
If the question is multiple choice, the subsequent items in this array are the available options.
If the question is not multiple choice, the array contains only the input type.
The output must be formatted as a 2D array, and there should be no variable names, explanations, or additional text.
Ensure the output is a valid Python 2D array that can be directly parsed.'''),
        ("human", "{Question}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({'Question': questions})
    
    return result.content


def formGenerator(purpose, target, audience, number, quetionType, tone='Normal'):
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        temperature=0,
        api_key=os.getenv("AIzaSyDk27PsOo83ck8c15ql80R1xXwmK2-NG_s"),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a form builder for a great corportae company, your task is to generate a form for this {aud} where the purpose is {pur} and we want to achive this {tar}. The questions should've {ton} tone. {num} should be the maximum number of questions. The questions should have {type} type of input. After each question include the type of the input like slider for age, textbox for name, etc and for multi-choice answers include choices in bracket after question."),
        ("human", "{Question}")
    ])
    chain = prompt | llm
    result = chain.invoke({"Question": 'Generate a form based on the given data', "aud":audience, "pur": purpose, "tar": target, "ton":tone, "num":number, "type":quetionType })
    data = result.content 
    output = structConverter(data)
    
    return output


purpose = "A survey to evaluate customer satisfaction for our mobile app. The app focuses on health tracking and meal planning. We want to understand user satisfaction with the features and usability."
target = "Gather feedback on app usability, key pain points, and feature suggestions."
audience = "Active users who have used the app for at least one month."
number = 20
questiontype = "Include a mix of multiple-choice and Likert scale questions, with 2 open-ended questions."

form = formGenerator(purpose, target, audience, number, questiontype)


print('\n\n\n')
output = structConverter(form)

print(output)



