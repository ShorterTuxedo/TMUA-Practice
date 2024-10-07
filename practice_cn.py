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

modes = {
    "YEAR": "練習自選的TMUA試卷套（自選年份）。試卷套由一份 第一卷 和 一份 第二卷試卷組成。",
    "PAPER": "練習自選的TMUA試卷。",
    "WILDCARD": "使用歷届試題隨機生成一套TMUA試卷。",
}

def pause():
    if os.name in ['nt', 'dos', 'win9x']:
        os.system("pause")
    else:
        input("\n\n按下 [回車] 鍵繼續。")

def show_question_image(path):
    image_window = tk.Tk()
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(image_window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    image_window.title("TMUA 練習")
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
    printTitle(f"正在填寫 {paper_id} 試卷的第 {question_num1} 道題")
    time_left = get_time_left(end_time)
    print("剩餘時間為 ", time_left[0], "分", time_left[1], "秒")
    print();print()
    print("禁止使用計數機！！\n")
    show_question_image(image_bank[question_num])
    my_answer = None
    while my_answer == None:
        my_answer = input("你的答案 (A-H)? :")
        my_answer = my_answer.upper()
        if (len(my_answer) != 1) or my_answer not in "ABCDEFGH":
            print("答案不存在。 ")
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
    
    end_time = time.time() + time_limit
    my_answers = ["未完成"] * num_of_questions

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
        printTitle(f"你的進度 (試卷 {paper_id})")
        time_left = get_time_left(end_time)
        print("剩餘時間為 ", time_left[0], "分", time_left[1], "秒")
        print();print()  
        if time.time() > end_time:
            time_up = True  
        for question_num in range(num_of_questions):
            print( ("第 " + str((question_num+1))+" 題:"), my_answers[question_num])
        print()

        while True:
            if time_up != True:
                isSubmitFinal = input("你想修改第幾道題的回答? (鍵入 \"F\" 提交試卷): ")
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
                        raise Exception("題目不存在。")
                except:
                    print("題目不存在。")
                    continue


    clearScreen()
    if time_up:
        print("時間到。")
    printTitle(f"分數 (試卷 {paper_id})")
    my_score = mark_paper(my_answers, correct_answers)
    qn_x=1
    for my_correct_answer_q in my_score[2]:
        aisc = "回答正確" if my_correct_answer_q=="c" else "回答錯誤"
        qn_x2=qn_x-1
        print(f"第 {qn_x} 題: {aisc}, 正確答案: {correct_answers[qn_x2]}, 你的回答: {my_answers[qn_x2]}")
        qn_x+=1
    print("你的分數:", my_score[0],"/",my_score[1])
    my_grade = grade_thresholds[str(my_score[0])]
    print("你的成績:","{:.1f}".format(my_grade))
    pause()
    return {"component":paper_id, "score":list(my_score),"grade":my_grade}


modeInvalid = False
mode = None
while True:
    clearScreen()
    if modeInvalid:
        print("模式不存在。\n")
    printTitle("選擇練習模式")
    print("可用模式")
    for mode in modes.keys():
        print(f"{mode} 模式 - {modes[mode]}")
    mode = input("\n\n選擇哪種模式? (鍵入 \"E\" 退出程式):").upper()
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
                print("年份不存在。\n")
            printTitle("試卷套練習")
            print("可用試卷套:")
            for year in question_bank["years"].keys():
                print(year)
            print()
            year_id = input("哪個試卷套? (鍵入 \"Q\" 返回):")
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
            printTitle(f"最終分數 (試卷套 {year_id})")

            year_scores = question_bank["years"][year_id]["grades"]
            my_total_score = paper_1["score"][0] + paper_2["score"][0]
            max_total_score = paper_1["score"][1] + paper_2["score"][1]
            print("你的總分:", my_total_score,"/",max_total_score)
            my_grade = year_scores[str(my_total_score)]
            print("你的總成績:","{:.1f}".format(my_grade))
            pause()
            year_id = None
    elif mode == "PAPER":
        modeInvalid = False
        paperInvalid = False
        paper_id = None
        while True:
            clearScreen()
            if paperInvalid:
                print("試卷不存在。\n")
            printTitle("試卷練習")
            print("可用試卷:")
            for paper in question_bank["papers"].keys():
                print(paper)
            print()
            paper_id = input("那份試卷? (鍵入 \"Q\" 返回):")
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
            printTitle("正在生成 (擲骰) 模式試卷套")
            
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

            print(str(time.sleep(0.5))[0:0]+"生成成功。\n")

            time.sleep(0.5)
            clearScreen()
            if optionInvalid:
                print("操作無效。")
            printTitle("WILDCARD (擲骰) 模式")
            print("""
            選擇一項操作：
            1. 整套 - 練習一整個 TMUA 試卷套
            2. 第一卷 - 練習一份 TMUA 第一卷
            3. 第二卷 - 練習一份 TMUA 第二卷
            
            """)
            
            option = input("哪項操作? (鍵入 \"Q\" 返回):")
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
                random_paper1_id = "1 TMUA WILDCARD (擲骰模式)"

                image_bank = random_paper_p1_images
                correct_answers = random_paper_p1_correctanswers
                grade_thresholds = WILDCARD_TMUA_PAPER1_THRESHOLDS

                paper_1_wc = execute_paper(random_paper1_id, image_bank, correct_answers, grade_thresholds)
            if option=="1" or option=="3":
                random_paper2_id = "2 TMUA WILDCARD (擲骰模式)"
                image_bank = random_paper_p2_images
                correct_answers = random_paper_p2_correctanswers
                grade_thresholds = WILDCARD_TMUA_PAPER2_THRESHOLDS

                paper_2_wc = execute_paper(random_paper2_id, image_bank, correct_answers, grade_thresholds)
            
            if option == "1":
                clearScreen()
                printTitle(f"WILDCARD (擲骰) 試卷套最終分數")

                wildcard_set_scores = WILDCARD_TMUA_SET_THRESHOLDS
                my_total_score = paper_1_wc["score"][0] + paper_2_wc["score"][0]
                max_total_score = paper_1_wc["score"][1] + paper_2_wc["score"][1]
                print("你的總分:", my_total_score,"/",max_total_score)
                my_grade = wildcard_set_scores[str(my_total_score)]
                print("你的總成績:","{:.1f}".format(my_grade))
                pause()
            
            option = None
    mode=None