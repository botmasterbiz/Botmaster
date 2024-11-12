#!/usr/bin/env python
import sys
import warnings

from crew import PdfSearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    user_input = input("Enter your search query: ")

    inputs = {
        'input': user_input
    }
    PdfSearch().crew().kickoff(inputs=inputs)

run()
