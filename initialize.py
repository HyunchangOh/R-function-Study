import pickle
file_names = ["1.txt"]

db_file = open("database.pkl","wb")
sentences = []
user_data = []
chapters = []
chapter_names = ["R Untro"]  
books = []
book = "R Fundamentals"
chapter_number = 0
sentence_index = 0
for raw_csv in file_names:
    raw = open(raw_csv,"r",encoding="utf-16")
    sentence_indices = []
    for line in raw:
        sentence = [sentence_index]+line.split("\t")
        sentences.append(sentence)
        user_data.append([0,0])
        sentence_indices.append(sentence_index)
        sentence_index +=1
    chapter = chapter_names[chapter_number],sentence_indices
    chapters.append(chapter)
    chapter_number+=1
books.append([book,[0]])

db = {}
db['books'] = books
db['sentences'] = sentences
db['chapters'] = chapters
db['user_data'] = user_data
pickle.dump(db,db_file)        
db_file.close()
        
        
