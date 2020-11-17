#%%

import cv2
import os
import numpy as np
import shutil

def wrong_name():
    """
    fixed label
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    chun
    """
    src_text = ['15', '16', '17','18','19', '20', '21', '22', '23', '24', '25']
    re_text = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    labels_path = r'D:\WorkSpace\cavedu_article\10910\1090923_yolo5\custom\labels'
    t = 1
    for i in os.listdir(labels_path):
        train_val_path = os.path.join(labels_path, i)
        for f in os.listdir(train_val_path):
            t = t+1
            trg_file = os.path.join(train_val_path, f)
            a=[]
            fin = open(trg_file, 'rt')
            for line in fin:
                if line.split(' ')[0] in src_text:
                    idx = src_text.index(line.split(' ')[0]) 
                    a.append(line.replace(src_text[idx], re_text[idx]))
            fin.close()
            fout = open(trg_file, 'wt')
            for v in a:
                fout.writelines(v)
            fout.close

    print('finish')

"""  拍照蒐集資料  """

def take_pic():
    
    ############## save data ##############
    def save(trg_path, idx, frame):
        global label
        save_path = os.path.join(trg_path, rf'{idx}_{label[idx]}.jpg')
        print(save_path)
        cv2.imwrite(save_path, frame)
        label[idx] = label[idx]+1

    ############## set target path ##############
    trg_path = 'data'
    if os.path.exists(trg_path)==False: os.mkdir(trg_path)

    ############## get camera & set size ##############
    #w_size, h_size = 512, 512
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_size)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_size)

    ############## set parameters ##############
    label = np.zeros([10], dtype=int)
    print(f'label len : {len(label)}')


    ############## open camera % save data ##############
    while(True):

        ret, frame = cap.read()
        overlay = frame.copy()
        ############## show info ##############
        text =  '{}{}{}{}{}'.format(f'Label\n0: {label[0]}\n1: {label[1]}\n', 
            f'2: {label[2]}\n3: {label[3]}\n' ,
            f'4: {label[4]}\n5: {label[5]}\n' ,
            f'6: {label[6]}\n7: {label[7]}\n' ,
            f'8: {label[8]}\n9: {label[9]}\n' )
        for i, txt in enumerate(text.split('\n')):
            cv2.putText(overlay, txt,(20,25*i+20), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), 1 )

        cv2.imshow('Create_Your_Own_Datasets', overlay)

        key = cv2.waitKey(1)
        
        if key== ord('q'): break
        
        for i in range(10):
            if key == ord(f'{i}'):
                save(trg_path, i, frame)

    cap.release()
    cv2.destroyAllWindows()
# %%

"""  取得客製化資料  """

def make_custom_data():

    ############## Check dir ##############

    dataset_dir ='data'
    label_dir = 'label'
    dataset = os.listdir(dataset_dir)
    label = os.listdir(label_dir)

    images = []
    labels = []

    custom_dir = 'custom'
    data_root = os.path.join(custom_dir, 'images')
    label_root = os.path.join(custom_dir, 'labels')

    data_train_dir = os.path.join(data_root, 'train')
    data_val_dir = os.path.join(data_root, 'val')
    label_train_dir = os.path.join(label_root, 'train')
    label_val_dir = os.path.join(label_root, 'val')

    dir_list = [data_train_dir, data_val_dir, label_train_dir, label_val_dir]

    for dir in dir_list:
        if os.path.exists(dir)==False:
            print(f"Create dir : {dir}")
            os.makedirs(dir) 

    ############## Get val data ##############

    #打亂數據
    def shuffle(data):
        
        arr = np.array(data)
        np.random.shuffle(arr)
        return arr.tolist()

    #拼接檔名
    def get_path(src, name, ftype):
        
        return f'{src}\{name}.{ftype}'


    val_num = 5
    pure_name = [ i.split('.')[0] for i in dataset ]
    val_data = shuffle(pure_name)[:val_num]

    print('Total Data length: ', len(pure_name))
    print('Validation Data: ', val_data)

    for d in val_data:

        src_data = get_path(dataset_dir, d, 'jpg')
        src_label = get_path(label_dir, d, 'txt')
        trg_data = get_path(data_val_dir, d, 'jpg')
        trg_label = get_path(label_val_dir, d, 'txt')

        shutil.copy(src_data, trg_data)
        shutil.copy(src_label, trg_label)

        pure_name.remove(d)

    ############## Split data ##############

    print("="*50)
    print('New Data length: ', len(pure_name))

    for d in pure_name:

        src_data = get_path(dataset_dir, d, 'jpg')
        src_label = get_path(label_dir, d, 'txt')
        trg_data = get_path(data_train_dir, d, 'jpg')
        trg_label = get_path(label_train_dir, d, 'txt')

        shutil.copy(src_data, trg_data)
        shutil.copy(src_label, trg_label) 

    print("Finish！")