import pickle

with open("seat_dict/seat_numbers_1.pickle", "rb") as handle: 
    dic_1 = pickle.load(handle)

with open("seat_dict/seat_numbers_2.pickle", "rb") as handle: 
    dic_2 = pickle.load(handle)

with open("seat_dict/seat_numbers_3.pickle", "rb") as handle: 
    dic_3 = pickle.load(handle)

with open("seat_dict/seat_numbers_A1.pickle", "rb") as handle: 
    dic_A1 = pickle.load(handle)

with open("seat_dict/seat_numbers_A2.pickle", "rb") as handle: 
    dic_A2 = pickle.load(handle)

with open("seat_dict/seat_numbers_A3.pickle", "rb") as handle: 
    dic_A3 = pickle.load(handle)

with open("seat_dict/seat_numbers_A2E.pickle", "rb") as handle: 
    dic_A2E = pickle.load(handle)

with open("seat_dict/seat_numbers_AE.pickle", "rb") as handle: 
    dic_AE = pickle.load(handle)

shortcut = ["1", "2", "3", "A1", "A2", "A2E", "A3", "AE"]
room = ["1.OG KIT-BIB (LSW)", "2.OG KIT-BIB (LST)", "3.OG KIT-BIB (LSG)", "Altbau 1.OG KIT-BIB (LBS)", "Altbau 2.OG KIT-BIB (LSN)", "Altbau 2.OG KIT-BIB Empore", "Altbau 3. OG KIT-BIB (LSM)", "Altbau EG KIT-BIB (LBS)" ]
dicts = [dic_1, dic_2, dic_3, dic_A1, dic_A2, dic_A2E, dic_A3, dic_AE]
area = [20, 19, 21, 42, 34, 35, 44, 40]

new_dic = dict()
for i in range(len(shortcut)): 
    new_dic[shortcut[i]] = (dicts[i], room[i], area[i])




with open("seat_dict/seat_numbers.pickle", "wb") as handle: 
    pickle.dump(new_dic, handle)
