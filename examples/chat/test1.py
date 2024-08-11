import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163
ai = AIChat(api_key="sk-Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163", model="gpt-3.5-turbo-0125",params={"temperature": 0.7},system="Write a fancy GitHub README based on the user-provided project name.")
ai("simpleaichat")