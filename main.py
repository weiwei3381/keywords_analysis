# coding:utf-8
import jieba
import csv
from PIL import Image
import numpy as np
from wordcloud import WordCloud


def get_stop_words():
    """
    获得中文停用词表
    :return: 停用词列表, List格式
    """
    stop_list = []
    with open("./asset/stopwords.txt", encoding="utf-8") as stop_words_file:
        for line in stop_words_file:
            stop_list.append(line.strip())
    return stop_list


def process_data():
    """
    读取数据文件
    :return: 
    """
    words_count_map = {}  # 词语统计
    with open("./data_funding.csv", encoding="utf-8") as csv_file:
        # 获得迭代器
        reader = csv.reader(csv_file)
        # 取出第一位
        next(reader)
        # 循环获得所有的项目名称
        for row in reader:
            project_title = row[5].strip()
            words_list = cut_words(project_title)
            for word in words_list:
                count_item_by_dict(words_count_map, word)
    with open("./关键词分析结果.csv", encoding="gbk", mode="w+", newline="") as result_file:
        fieldnames = ("序号", "关键词", "频次")
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        writer.writeheader()
        i = 1  # 序号,每次自增1
        # 根据词典的值进行逆序排序
        for key in sorted(words_count_map, key=words_count_map.__getitem__, reverse=True):
            # 根据词典构造一行
            row = {
                "序号": i,
                "关键词": key,
                "频次": words_count_map.get(key)
            }
            writer.writerow(row)
            i += 1


def count_item_by_dict(count_dict, item):
    """
    使用词典统计项目
    :param count_dict: 词典
    :param item: 项目
    :return: 
    """
    if item not in count_dict:
        count_dict[item] = 1
    else:
        count_dict[item] += 1


def cut_words(content):
    """
    分词
    :param content: 待分词内容
    :return: 
    """
    # 获得分词迭代器
    seg_itor = jieba.cut(content, cut_all=False)
    # 获得停用词表
    stop_list = get_stop_words()
    # 将不在停用词表中的词段返回
    return [seg for seg in seg_itor if seg not in stop_list]


def get_plain_txt(filter_list=None):
    """
    去掉过滤词, 获得以空格分词的纯文本
    :return: 
    """
    whole_txt = ""
    with open("./data_funding.csv", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            project_title = row[5].strip()
            words_list = cut_words(project_title)
            # 去掉过滤词
            if filter_list is not None:
                words_list = [word for word in words_list if word not in filter_list]
            whole_txt += " ".join(words_list)
    return whole_txt


def generate_word_cloud(filter_list=None):
    # 设置字体位置
    font = "./asset/simhei.ttf"
    # 设置生成图形
    image = np.array(Image.open('./asset/tooth.png'))
    whole_text = get_plain_txt(filter_list)
    word_cloud = WordCloud(scale=5, font_path=font, mask=image, background_color='white', max_words=100,
                           max_font_size=30, random_state=10).generate(whole_text)
    image = word_cloud.to_image()
    image.save("词云展示.png")
    image.show()


if __name__ == "__main__":
    process_data()
    filter_list = ["作用", "机制", "研究", "调控", "过程", "发生", "发展", "试验", "能力", "影响", "相关"]
    generate_word_cloud(filter_list=filter_list)
