# from typing import Tuple, List
# from prolog.prolog import PrologKB
# import aiml
# import os

# def initialize(aiml_files: List[str], prolog_file: str, brain_file: str = "bot.brn") -> Tuple[aiml.Kernel, 'PrologKB']:
#     """
#     Initialize AIML kernel (loading a brain file if it exists, otherwise learning multiple AIML files
#     and saving the resulting brain) and return it alongside a PrologKB instance.
#     """
#     kernel = aiml.Kernel()
#     # If a compiled brain file exists, load it for faster startup
#     if os.path.exists(brain_file):
#         print("Loading from brain file: " + brain_file)
#         kernel.loadBrain(brain_file)
#     else:
#         print("Parsing aiml files")
#         kernel.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
#         print("Saving brain file: " + brain_file)
#         kernel.saveBrain(brain_file)

#     # Initialize Prolog knowledge base
#     kb = PrologKB(prolog_file)
#     return kernel, kb


# def process_question(q: str, kernel: aiml.Kernel, kb: PrologKB) -> str:
#     """
#     Process a single question: updates AIML predicates based on Prolog logic,
#     then returns the AIML response string.
#     """
#     q_stripped = q.strip().rstrip('?')
#     kernel.respond(q_stripped)  # prime predicates from AIML patterns

#     relation = kernel.getPredicate("relation")
#     person = kernel.getPredicate("person")
#     possible_relative = kernel.getPredicate("possible_relative")
#     qtype = kernel.getPredicate("type")

#     result = ''
#     if qtype == 'type1' and relation and person:
#         result = kb.get_relation(relation, person) or 'unknown'
#     elif qtype == 'type2' and possible_relative and person and relation:
#         status = kb.check_relation(relation, possible_relative, person)
#         kernel.setPredicate("status", 'yes' if status else 'no')
#         result = 'yes' if status else 'no'
#     else:
#         result = ''

#     kernel.setPredicate("relative", result)
#     kernel.setPredicate("person_name", person)

#     return kernel.respond(q_stripped)


# # Example standalone usage
# if __name__ == '__main__':
#     kernel, kb = initialize('family.aiml', 'prolog/family_relationship.pl')
#     print("Type 'quit' to exit.")
#     while True:
#         question = input("You: ")
#         if question.lower() in ('quit', 'exit'):
#             break
#         answer = process_question(question, kernel, kb)
#         print("Bot:", answer)


# #################################################
#      UPDATE CODE V-1 (AGE ADDITION)
# ##################################################

from typing import Tuple, List
from prolog.prolog import PrologKB
import aiml
import os
from datetime import datetime


def initialize(aiml_files: List[str], prolog_file: str, brain_file: str = "bot.brn") -> Tuple[aiml.Kernel, 'PrologKB']:
    """
    Initialize AIML kernel (loading a brain file if it exists, otherwise learning multiple AIML files
    and saving the resulting brain) and return it alongside a PrologKB instance.
    """
    kernel = aiml.Kernel()
    # If a compiled brain file exists, load it for faster startup
    if os.path.exists(brain_file):
        print("Loading from brain file: " + brain_file)
        kernel.loadBrain(brain_file)
    else:
        print("Parsing aiml files")
        kernel.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
        print("Saving brain file: " + brain_file)
        kernel.saveBrain(brain_file)

    # Initialize Prolog knowledge base
    kb = PrologKB(prolog_file)
    return kernel, kb


def process_question(q: str, kernel: aiml.Kernel, kb: PrologKB) -> str:
    """
    Process a single question: updates AIML predicates based on Prolog logic,
    then returns the AIML response string.
    """
    q_stripped = q.strip().rstrip('?')
    kernel.respond(q_stripped)  # prime predicates from AIML patterns

    relation = kernel.getPredicate("relation")
    person = kernel.getPredicate("person")
    possible_relative = kernel.getPredicate("possible_relative")
    qtype = kernel.getPredicate("type")
    
    print(qtype)

    result = ''
    if qtype == 'type1' and relation and person:
        result = kb.get_relation(relation, person) or 'unknown'
    elif qtype == 'type2' and possible_relative and person and relation:
        status = kb.check_relation(relation, possible_relative, person)
        kernel.setPredicate("status", 'yes' if status else 'no')
        result = 'yes' if status else 'no'
    elif qtype == 'age_type' and person:
        # Get the age from the PrologKB and set the relevant predicate in AIML
        result = kb.get_age(person)
        print(f"DEBUG: RESULT {result}")
        if result:
            age, birth_year = result
            print(age)
            kernel.setPredicate("age", age)
            kernel.setPredicate("birth_year", birth_year)
            kernel.setPredicate("current_year", current_year = datetime.now().year )
        else:
            return None
        
    else:
        result = ''

    kernel.setPredicate("relative", result)
    kernel.setPredicate("person_name", person)

    return kernel.respond(q_stripped)


# Example standalone usage
if __name__ == '__main__':
    kernel, kb = initialize('family.aiml', 'prolog/family_relationship.pl')
    print("Type 'quit' to exit.")
    while True:
        question = input("You: ")
        if question.lower() in ('quit', 'exit'):
            break
        answer = process_question(question, kernel, kb)
        print("Bot:", answer)
