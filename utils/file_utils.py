
def save(content, data_dir, name):
    """将内容以name命名保存在data_dir目录中"""
    file = open(data_dir + '/' + name, 'w+b')
    file.write(content)
    file.close()