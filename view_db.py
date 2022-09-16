import pickle

f = open("database.pkl","rb")
db = pickle.load(f)
print(db['sentences'])