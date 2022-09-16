import random, os, pickle
from time import time
from math import sqrt
from datetime import datetime, timedelta

def main_menu(db):
    intro = '''
######  
#     #  
######  
#     #   
#     #    

Welcome to R learning machine 2.0
What do you want to do now?

1. Learn 10 Random Sentences
2. Learn By Thema
3. View My Knowledge Status
4. Add a new chapter

            '''
    while True:
        mode = input(intro)
        os.system('cls')
        if mode == "1":
            updated_user_data = learn_random(db,10)
            db["user_data"] = updated_user_data
        elif mode == "2":
            updated_user_data = learn_chapters(db)
            db["user_data"] = updated_user_data
        elif mode == "3":
            view_knowledge(db)
        elif mode == "4":
            manage_add(db)
        save_database(db)

def load_database():
    f = open("database.pkl","rb")
    db = pickle.load(f)
    f.close()
    return db

def save_database(db):
    f = open("database.pkl","wb")
    pickle.dump(db,f)
    f.close()

def learn(db, sentences):
    USER_DATA = db['user_data']
    current = 0
    review_sentences = []
    for sentence in sentences:
        already_failed = False
        staged = False
        current+=1
        while True:
            print("%d/%d"%(current,len(sentences))) # Progress like 5/10
            print(sentence[2]) # Shows function description
            placeholder = print("What is the function described above? ")

            choices = []
            choices_objects = random.choices(sentences,k=4)
            for obj in choices_objects:
                choices.append(obj[1])

            choices.append(sentence[1])
            random.shuffle(choices)
            print(" 1. %s \n 2. %s \n 3. %s \n 4. %s \n 5. %s " %tuple(choices))

            s_id = sentence[0] #integer. sentence id(foreign key)
            prev_performance = USER_DATA[s_id] # (Valid for # minutes, Expiry_date)
            valid_minutes = prev_performance[0]
            expiry_date = prev_performance[1]

            while True: # Ask again if user input is invalid
                pf = input()
                user_answer = int(pf)-1
                if choices[user_answer]== sentence[1]:
                    print("Correct!")
                    if not already_failed:
                        if expiry_date == 0 or expiry_date < datetime.now():
                            new_valid_minutes = next_in_ebbinghaus(valid_minutes)
                            new_expiry_date = datetime.now() + timedelta(minutes=new_valid_minutes)
                        else:
                            new_valid_minutes = valid_minutes
                            new_expiry_date = expiry_date
                    already_failed = False
                    break
                else:
                    print("Wrong! The answer is: ",sentence[1])
                    new_valid_minutes = 0 
                    new_expiry_date = datetime.now() # Put it on Review immediately
                    already_failed = True
                    if not staged:
                        review_sentences.append(sentence)
                        staged=True
                    break

            new_data = [new_valid_minutes,new_expiry_date] #python variables scoped to innermost function/class/module
            USER_DATA[s_id] = new_data
            next = input("Press Enter to next question")
            os.system('cls')
            if not already_failed:
                break 
    if len(review_sentences)>0:
        placeholder = input("Congratulations. Now Starting Review Session with %d functions"%len(review_sentences))
        os.system('cls')
        db['user_data'] = USER_DATA
        USER_DATA = learn(db, review_sentences)
    return USER_DATA  


def next_in_ebbinghaus(valid_minutes):
    if valid_minutes == 0:
        return 1
    if valid_minutes == 1:
        return 2
    a = valid_minutes*(1 + sqrt(5))/2.0
    return round(a) 

def learn_random(db,num_of_sentences):
    expired_sentences = get_expired(db)
    if num_of_sentences > len(expired_sentences):
        sentences = expired_sentences
    else:
        sentences = expired_sentences[:num_of_sentences]
    return learn(db, sentences)

def get_expired(db):
    USER_DATA = db['user_data']
    SENTENCES = db['sentences']
    expired_sentences = []
    new_sentences = []
    now = datetime.now()
    for i in range(len(USER_DATA)):
        expiry_date = USER_DATA[i][1]
        if expiry_date == 0:
            new_sentences.append(SENTENCES[i])
        elif expiry_date <= now:
            expired_sentences.append(SENTENCES[i])
    random.shuffle(expired_sentences)
    random.shuffle(new_sentences)
    return expired_sentences + new_sentences #prioritize forgotten sentences

def learn_chapters(db):
    book = select_book(db)
    chapter = select_chapter(db,book)
    sentences = get_sentences(db,chapter)
    return learn(db, sentences)

def select_book(db):
    BOOKS = db["books"]
    os.system('cls')
    for i in range(len(BOOKS)):
        print("%d : %s" %(i+1, BOOKS[i][0]))
    book_number = int(input("Choose a book number:"))
    return BOOKS[book_number-1]

def select_chapter(db,book):
    os.system('cls')
    CHAPTERS = db['chapters']
    chapters = []
    for i in book[1]:
        chapter = CHAPTERS[i]
        chapters.append(chapter)
    for i in range(len(chapters)):
        print("%d. %s" %(i+1,chapters[i][0]))
    chapter_number = int(input("Choose a chapter number:"))
    
    return chapters[chapter_number-1]

def get_sentences(db,chapter):
    SENTENCES=db['sentences']
    sentences = []
    for i in chapter[1]:
        sentences.append(SENTENCES[i])
    return sentences

def view_knowledge(db):
    never_seen = 0
    forgot = 0
    know = 0
    USER_DATA = db['user_data']
    for sentence_data in USER_DATA:
        if sentence_data[1]==0:
            never_seen+=1
        elif sentence_data[1] < datetime.now():
            forgot+=1
        else:
            know +=1
    os.system('cls')
    print("You know %d sentences."%know)
    print("You forgot %d sentences"%forgot)
    print("You haven't seen %d sentences"%never_seen)
    placeholder = input("Press Enter to Return to Main Menu")

def manage_add(db):
    while True:
        os.system('cls')
        warning = input("The format must be unicode text(.txt) file. German has to come first and translation next, separated by tab.")
        directory = input("Enter the relative directory to the file. ")
        # try:
        f = open(directory,"r",encoding="utf-16")
        sentences = load_from_file(f)
        print("We found %d sentences in the file." %len(sentences))
        break
        # except:
            # placeholder = input("No such file or failed to read the file.")

    mode = input("(A)ppend to existing book. (C)reate a new book")
    if mode.lower()=="a":
        book = select_book(db)
        while True:
            chapter_mode = input("(A)ppend to existing chapter. (C)reate a new chapter")
            if chapter_mode.lower() == "a":
                chapter = select_chapter()
                break
            elif chapter_mode.lower() == "c":
                chapter_name = input("What will this chapter be called?")
                chapter = [chapter_name,[]]
                break
    if mode.lower()=="c":
        name = input("What will this book be called?")
        book = [name,[]]
        chapter_name = input("What will this chapter be called?") 
        chapter = [chapter_name,[]]
    
    SENTENCES = db['sentences']
    start_index = len(SENTENCES)
    end_index = len(SENTENCES)+len(sentences)
    for i in range(len(sentences)):
        SENTENCES.append([start_index+i]+sentences[i])
    chapter[1] = chapter[1]+list(range(start_index,end_index))
    CHAPTERS = db['chapters']
    book[1].append(len(CHAPTERS))
    CHAPTERS.append(chapter)

    BOOKS = db['books']
    if mode.lower() == "c":
        BOOKS.append(book)
    if mode.lower() == "a":
        key = -1
        for i in range(len(BOOKS)):
            if BOOKS[i][0] == book[0]:
                BOOKS[i] = book
                break
    
    USER_DATA = db['user_data']
    for i in range(len(sentences)):
        USER_DATA.append([0,0])


def load_from_file(f):
    sentences = []
    for line in f:
        sentence = line.split("\t")
        sentences.append(sentence)
    return sentences

db = load_database()
main_menu(db)