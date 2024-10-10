import json, os, time, random
import tkinter as tk
from PIL import ImageTk, Image


num_of_questions = 20
time_limit = 75 * 60

# It is said that the TMUA will be running as WILDCARD mode from now on.
WILDCARD_TMUA_PAPER1_THRESHOLDS = {"0":1,"1":1,"2":1,"3":1,"4":1.9,"5":2.7,"6":3.4,"7":4,"8":4.6,"9":5.2,"10":5.8,"11":6.3,"12":6.6,"13":6.9,"14":7.1,"15":7.3,"16":7.6,"17":7.9,"18":8.3,"19":9,"20":9}
WILDCARD_TMUA_PAPER2_THRESHOLDS = {"0":1,"1":1,"2":1,"3":1,"4":1.3,"5":2.1,"6":2.8,"7":3.4,"8":4,"9":4.6,"10":5.2,"11":5.8,"12":6.4,"13":6.7,"14":6.9,"15":7.2,"16":7.4,"17":7.8,"18":8.2,"19":8.9,"20":9}
WILDCARD_TMUA_SET_THRESHOLDS = {"0":1,"1":1,"2":1,"3":1,"4":1,"5":1,"6":1.2,"7":1.6,"8":2.1,"9":2.5,"10":2.9,"11":3.2,"12":3.6,"13":3.9,"14":4.2,"15":4.5,"16":4.8,"17":5.1,"18":5.4,"19":5.7,"20":5.9,"21":6.2,"22":6.5,"23":6.6,"24":6.7,"25":6.8,"26":6.9,"27":7,"28":7.1,"29":7.2,"30":7.4,"31":7.5,"32":7.6,"33":7.8,"34":8,"35":8.1,"36":8.4,"37":8.6,"38":9,"39":9,"40":9}
# These are the PRE-SET TMUA WILDCARD THRESHOLDS.

showQuestionsAfterFinished = True

modes = {
    "YEAR": "ALLOWS YOU TO PRACTISE A CERTAIN YEAR OF TMUA.",
    "PAPER": "ALLOWS YOU TO PRACTISE A CERTAIN PAPER OF TMUA.",
    "WILDCARD": "GENERATES A RANDOM TMUA PAPER FROM OTHER PAST PAPER QUESTIONS.",
}

def pause():
    if os.name in ['nt', 'dos', 'win9x']:
        os.system("pause")
    else:
        input("\n\nPRESS [ENTER] TO CONTINUE.")

def show_question_image(path):
    image_window = tk.Tk()
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(image_window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    image_window.title("TMUA PRACTISE")
    image_window.mainloop()

def clearScreen():
    print(str(os.system("cls" if os.name in ['nt', 'dos', 'win9x'] else "clear"))[0:0],end="")

def printTitle(title):
    if os.name in ["nt", "dos", "win9x"]:
        os.system("title " + str(title).replace("&","^&"))
    print("="*10+str(title)+"="*10)
    print();print()

question_bank = json.loads(open("question_bank.json", "r", encoding="UTF-8").read())

def get_time_left(end_time):
    secs_left = int(end_time - time.time())
    return (secs_left // 60, secs_left % 60)

def answer_question(paper_id, question_num, image_bank, my_answers, end_time):
    if time.time() > end_time:
        return False
    clearScreen()
    question_num1=question_num+1
    printTitle(f"ANSWERING PAPER {paper_id} QUESTION {question_num1}")
    time_left = get_time_left(end_time)
    print("YOU HAVE", time_left[0], "MINUTES AND", time_left[1], "SECONDS LEFT")
    print();print()
    print("NO CALCULATOR PERMITTED\n")
    show_question_image(image_bank[question_num])
    my_answer = None
    while my_answer == None:
        my_answer = input("WHAT IS YOUR ANSWER (A-H)? :")
        my_answer = my_answer.upper()
        if (len(my_answer) != 1) or my_answer not in "ABCDEFGH":
            print("THAT IS INVALID. ")
            my_answer = None
    if time.time() > end_time:
        return False
    my_answers[question_num] = my_answer 
    return True

def mark_paper(my_answers, correct_answers):
    global num_of_questions
    correct_answers_num = 0
    my_corr_anses = ["i"] * num_of_questions
    for i in range(num_of_questions):
        if my_answers[i]==correct_answers[i]:
            my_corr_anses[i] = "c"
            correct_answers_num += 1
    return (correct_answers_num, num_of_questions, my_corr_anses)



def execute_paper(paper_id, image_bank, correct_answers, grade_thresholds):
    global question_bank
    global num_of_questions
    global showQuestionsAfterFinished

    end_time = time.time() + time_limit
    my_answers = ["INCOMPLETE"] * num_of_questions

    time_up = False
    for question_num in range(num_of_questions):
        if time.time() > end_time:
            time_up = True 
            break
        if not answer_question(paper_id, question_num, image_bank, my_answers, end_time):
            time_up = True
            break

    if time.time() > end_time:
        time_up = True
    isSubmitFinal = None
    while isSubmitFinal==None:
        clearScreen()
        printTitle(f"YOUR PROGRESS (PAPER {paper_id})")
        time_left = get_time_left(end_time)
        print("YOU HAVE", time_left[0], "MINUTES AND", time_left[1], "SECONDS LEFT")
        print();print()    
        if time.time() > end_time:
            time_up = True
        for question_num in range(num_of_questions):
            print( ("QUESTION " + str((question_num+1))+":"), my_answers[question_num])
        print()

        while True:
            if time_up != True:
                isSubmitFinal = input("WHICH QUESTION DO YOU WANT TO EDIT? (ENTER \"F\" FOR FINAL SUBMISSION): ")
            else:
                isSubmitFinal = "F"
            if isSubmitFinal.upper() == "F":
                break
            else:
                try:
                    isSubmitFinal = int(isSubmitFinal)
                    if isSubmitFinal >= 1 and isSubmitFinal <= 20:
                        isSubmitFinal-=1
                        if time.time() > end_time:
                            time_up = True
                            continue
                        answer_question(paper_id, isSubmitFinal, image_bank, my_answers, end_time)
                        isSubmitFinal = None
                        break
                    else:
                        raise Exception("QUESTION NOT IN RANGE")
                except:
                    print("INVALID QUESTION.")
                    continue


    clearScreen()
    if time_up:
        print("TIME'S UP.")
    printTitle(f"FINAL SCORE (PAPER {paper_id})")
    my_score = mark_paper(my_answers, correct_answers)
    qn_x=1
    for my_correct_answer_q in my_score[2]:
        aisc = "CORRECT" if my_correct_answer_q=="c" else "INCORRECT"
        qn_x2=qn_x-1
        print(f"QUESTION {qn_x}: {aisc}, CORRECT ANSWER: {correct_answers[qn_x2]}, YOU ANSWERED: {my_answers[qn_x2]}")
        if showQuestionsAfterFinished:
            print(f"QUESTION IMAGE PATH: {image_bank[qn_x2]}")
        qn_x+=1
    print("YOUR SCORE:", my_score[0],"/",my_score[1])
    my_grade = grade_thresholds[str(my_score[0])]
    print("YOUR GRADE:","{:.1f}".format(my_grade))
    pause()
    return {"component":paper_id, "score":list(my_score),"grade":my_grade}


modeInvalid = False
mode = None
while True:
    clearScreen()
    if modeInvalid:
        print("INVALID MODE ENTERED.\n")
    printTitle("SELECT PRACTISE MODE")
    print("AVAILABLE MODES")
    for mode in modes.keys():
        print(f"{mode} MODE - {modes[mode]}")
    mode = input("\n\nWHICH MODE? (ENTER \"E\" TO EXIT THE PROGRAM):").upper()
    if mode == "E":
        modeInvalid = False
        break
    if mode not in modes.keys():
        modeInvalid = True
        continue

    if mode=="YEAR":
        modeInvalid = False
        yearInvalid = False
        year_id = None
        while True:
            clearScreen()
            if yearInvalid:
                print("INVALID YEAR ENTERED.\n")
            printTitle("YEAR PRACTISE")
            print("AVAILABLE YEARS:")
            for year in question_bank["years"].keys():
                print(year)
            print()
            year_id = input("WHICH YEAR? (ENTER \"Q\" TO QUIT):")
            if year_id.upper() == "Q":
                yearInvalid = False
                break
            if not (year_id in question_bank["years"].keys() and f"{year_id}_paper1" in question_bank["papers"] and f"{year_id}_paper2" in question_bank["papers"]):
                yearInvalid = True
                year_id = None 
                continue
            yearInvalid = False

            yearpaper1 = f"{year_id}_paper1"
            paper_bank = question_bank["papers"][yearpaper1]
            image_bank = paper_bank["images"]
            correct_answers = paper_bank["correct_answers"]
            grade_thresholds = paper_bank["grades"]
            paper_1 = execute_paper(yearpaper1, image_bank, correct_answers, grade_thresholds)

            
            yearpaper2 = f"{year_id}_paper2"
            paper_bank = question_bank["papers"][yearpaper2]
            image_bank = paper_bank["images"]
            correct_answers = paper_bank["correct_answers"]
            grade_thresholds = paper_bank["grades"]
            paper_2 = execute_paper(yearpaper2, image_bank, correct_answers, grade_thresholds)

            clearScreen()
            printTitle(f"FINAL SCORE ON TMUA (YEAR {year_id})")

            year_scores = question_bank["years"][year_id]["grades"]
            my_total_score = paper_1["score"][0] + paper_2["score"][0]
            max_total_score = paper_1["score"][1] + paper_2["score"][1]
            print("YOUR SCORE:", my_total_score,"/",max_total_score)
            my_grade = year_scores[str(my_total_score)]
            print("YOUR GRADE:","{:.1f}".format(my_grade))
            pause()
            year_id = None
    elif mode == "PAPER":
        modeInvalid = False
        paperInvalid = False
        paper_id = None
        while True:
            clearScreen()
            if paperInvalid:
                print("INVALID PAPER ENTERED.\n")
            printTitle("PAPER PRACTISE")
            print("AVAILABLE PAPERS:")
            for paper in question_bank["papers"].keys():
                print(paper)
            print()
            paper_id = input("WHICH PAPER ID? (ENTER \"Q\" TO QUIT):")
            if paper_id.upper() == "Q":
                paperInvalid = False
                break
            if paper_id not in question_bank["papers"].keys():
                paperInvalid = True 
                continue
            
            paper_bank = question_bank["papers"][paper_id]
            image_bank = paper_bank["images"]
            correct_answers = paper_bank["correct_answers"]
            grade_thresholds = paper_bank["grades"]
            execute_paper(paper_id, image_bank, correct_answers, grade_thresholds)

            paper_id = None
    elif mode=="WILDCARD":
        modeInvalid=False
        optionInvalid = False
        option = None
        while True:
            clearScreen()
            printTitle("GENERATING PAPERS FOR WILDCARD MODE")
            
            p1_ppq_images = []
            p2_ppq_images = []
            p1_ppq_correctanswers = []
            p2_ppq_correctanswers = []
            for past_paper in question_bank["papers"].keys():
                if past_paper.endswith("_paper1"):
                    p1_ppq_images += question_bank["papers"][past_paper]["images"]
                    p1_ppq_correctanswers += question_bank["papers"][past_paper]["correct_answers"]
                elif past_paper.endswith("_paper2"):
                    p2_ppq_images += question_bank["papers"][past_paper]["images"]
                    p2_ppq_correctanswers += question_bank["papers"][past_paper]["correct_answers"] 

            random_paper_p1_questions = random.sample(range(len(p1_ppq_images)), k=num_of_questions)
            random_paper_p1_images = [p1_ppq_images[question] for question in random_paper_p1_questions]
            random_paper_p1_correctanswers = [p1_ppq_correctanswers[question] for question in random_paper_p1_questions]

            random_paper_p2_questions = random.sample(range(len(p2_ppq_images)), k=num_of_questions)
            random_paper_p2_images = [p2_ppq_images[question] for question in random_paper_p2_questions]
            random_paper_p2_correctanswers = [p2_ppq_correctanswers[question] for question in random_paper_p2_questions]

            print(str(time.sleep(0.5))[0:0]+"DONE GENERATING PAPERS.\n")

            time.sleep(0.5)
            clearScreen()
            if optionInvalid:
                print("INVALID OPTION.")
            printTitle("WILDCARD MODE")
            print("""
            PICK AN OPTION.
            1. FULL SET - GENERATE A FULL TMUA PAPER SET
            2. PAPER 1 - GENERATE JUST A PAPER 1
            3. PAPER 2 - GENERATE JUST A PAPER 2
            
            """)
            
            option = input("WHICH OPTION? (ENTER \"Q\" TO QUIT):")
            if option.upper() == "Q":
                optionInvalid = False
                break
            if option not in ["1","2","3"]:
                optionInvalid = True 
                continue
            
            optionInvalid = False 
            
            paper_1_wc = None 
            paper_2_wc = None
            if option=="1" or option=="2":
                random_paper1_id = "1 TMUA WILDCARD"

                image_bank = random_paper_p1_images
                correct_answers = random_paper_p1_correctanswers
                grade_thresholds = WILDCARD_TMUA_PAPER1_THRESHOLDS

                paper_1_wc = execute_paper(random_paper1_id, image_bank, correct_answers, grade_thresholds)
            if option=="1" or option=="3":
                random_paper2_id = "2 TMUA WILDCARD"
                image_bank = random_paper_p2_images
                correct_answers = random_paper_p2_correctanswers
                grade_thresholds = WILDCARD_TMUA_PAPER2_THRESHOLDS

                paper_2_wc = execute_paper(random_paper2_id, image_bank, correct_answers, grade_thresholds)
            
            if option == "1":
                clearScreen()
                printTitle(f"FINAL SCORE ON TMUA (WILDCARD SET)")

                wildcard_set_scores = WILDCARD_TMUA_SET_THRESHOLDS
                my_total_score = paper_1_wc["score"][0] + paper_2_wc["score"][0]
                max_total_score = paper_1_wc["score"][1] + paper_2_wc["score"][1]
                print("YOUR SCORE:", my_total_score,"/",max_total_score)
                my_grade = wildcard_set_scores[str(my_total_score)]
                print("YOUR GRADE:","{:.1f}".format(my_grade))
                pause()
            
            option = None
    mode=None