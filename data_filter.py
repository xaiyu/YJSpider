from hashlib import md5


def judge_exist(data):
    with open('./filter.txt', 'a+') as f:
        f.seek(0)
        if md5(data.encode('utf-8')).hexdigest()+'\n' in f.readlines():
            print("info:Exist")
            return True

def filter_data(data):
    with open('./filter.txt', 'a+') as f:
        f.write(str(md5(data.encode('utf-8')).hexdigest()+'\n'))
        print("info:update data")
        return 
            