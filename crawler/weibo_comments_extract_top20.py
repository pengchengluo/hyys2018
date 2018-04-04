import csv


if __name__=='__main__':
    file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/2018_热门.csv'
    top_file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/2018_热门_top20.csv'
    with open(file_path, mode='r', encoding='GBK') as input_file,\
            open(top_file_path, mode='w', encoding='GBK', newline='') as output_file:
        reader = csv.reader(input_file)
        head = reader.__next__()
        data = []
        all = set()
        for row in reader:
            if row[0]+'_'+row[1] not in all:
                data.append(row)
                all.add(row[0]+'_'+row[1])
        data.sort(key=lambda x:(x[0], -int(x[4])))
        count = 0
        writer = csv.writer(output_file)
        writer.writerow(head)
        keyword = ''
        for row in data:
            if keyword != row[0]:
                count = 0
                keyword = row[0]
            count += 1
            if count <= 20 and int(row[4]) > 0:
                writer.writerow(row)
