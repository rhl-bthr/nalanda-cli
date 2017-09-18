import os
def make(folder_list):
    for folder_name in folder_list:
        if not os.path.exists('res/'+folder_name):
            os.makedirs('res/'+folder_name)
            
def subject_make(folder_list,path):
    for folder_name in folder_list:
        if not os.path.exists(path + 'Lectures/'+folder_name):
            os.makedirs(path + 'Lectures/'+folder_name)