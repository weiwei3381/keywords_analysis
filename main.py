# coding:utf-8
import jieba
import csv
from PIL import Image
import numpy as np
from wordcloud import WordCloud


def get_chinese_stop_words():
    """
    获得中文停用词表
    :return: 停用词列表, List格式
    """
    stop_list = []
    with open("./asset/chinese_stopwords.txt", encoding="utf-8") as stop_words_file:
        for line in stop_words_file:
            stop_list.append(line.strip())
    return stop_list


def get_english_stop_words():
    """
    获得英文停用词表
    :return: 停用词列表, List格式
    """
    stop_list = []
    with open("./asset/english_stopwords.txt", encoding="utf-8") as stop_words_file:
        for line in stop_words_file:
            stop_list.append(line.strip())
    return stop_list


def cal_chinese_statistics_data(data_path):
    """
    计算中文的统计数据
    :param data_path: 数据路径
    :return:
    """
    words_count_map = {}  # 词语统计
    with open(data_path, encoding="utf-8") as csv_file:
        # 获得迭代器
        reader = csv.reader(csv_file)
        # 取出第一位
        next(reader)
        # 循环获得所有的项目名称
        for row in reader:
            project_title = row[5].strip()
            words_list = cut_chinese_words(project_title)
            for word in words_list:
                count_item_by_dict(words_count_map, word)
    with open("./result/关键词分析结果.csv", encoding="gbk", mode="w+", newline="") as result_file:
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


def cal_english_statistics_data(data_path, column_num=0, separator=" ", save_name="关键词分析结果"):
    """
    计算英文的统计数据
    :param data_path: 数据路径, 需要是csv格式, 逗号分割
    :param column_num: 分析的字段序号, 第一列为0, 默认为第一列
    :param separator: 分词使用的分隔符, 默认为" "
    :param save_name: 保存文件名称, 默认为"关键词分析结果", 将保存在"./result/[保存名称].csv"下
    :return:
    """
    words_count_map = {}  # 词语统计
    with open(data_path, encoding="utf-8") as csv_file:
        # 获得迭代器
        reader = csv.reader(csv_file)
        # 取出第一位
        next(reader)
        # 循环获得所有的数据名称
        for row in reader:
            data_title = row[column_num].strip()  # 数据标题
            words_list = cut_english_words(data_title, separator)
            for word in words_list:
                count_item_by_dict(words_count_map, word)
    with open("./result/%s.csv" % (save_name,), encoding="gbk", mode="w+", newline="") as result_file:
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


def cut_chinese_words(content):
    """
    中文分词
    :param content: 待分词内容
    :return: 词语的数组, 每个项目为一个词
    """
    # 获得分词迭代器
    seg_itor = jieba.cut(content, cut_all=False)
    # 获得停用词表
    stop_list = get_chinese_stop_words()
    # 将不在停用词表中的词段返回
    return [seg for seg in seg_itor if seg not in stop_list]


def cut_english_words(content, separator=" "):
    """
    英文分词，按照分隔符进行分割
    :param content: 英文内容
    :param separator: 分词的分隔符， 默认为空格
    :return:
    """
    # 获得停用词表
    stop_list = get_english_stop_words()
    # 将内容全部转成小写之后进行划分
    all_words = content.lower().split(separator)
    # 将不在停用词表中的词段返回
    return [word.strip() for word in all_words if word and word not in stop_list]


def get_plain_txt(data_path, filter_list=None):
    """
    去掉过滤词, 获得以空格分词的纯文本
    :return: 
    """
    whole_txt = ""
    with open(data_path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            project_title = row[5].strip()
            words_list = cut_chinese_words(project_title)
            # 去掉过滤词
            if filter_list is not None:
                words_list = [word for word in words_list if word not in filter_list]
            whole_txt += " ".join(words_list)
    return whole_txt


def generate_word_cloud(data_path, save_name="词云展示", filter_list=None):
    # 设置字体位置
    font = "./asset/simhei.ttf"
    # 设置生成图形
    image = np.array(Image.open('./asset/tooth.png'))
    whole_text = get_plain_txt(data_path, filter_list)
    word_cloud = WordCloud(scale=5, font_path=font, mask=image, background_color='white', max_words=100,
                           max_font_size=30, random_state=10).generate(whole_text)
    image = word_cloud.to_image()
    image.save("./result/%s.png" % (save_name,))
    image.show()


if __name__ == "__main__":
    # cal_chinese_statistics_data("./database/中文基金.csv")
    # my_filter_list = ["作用", "机制", "研究", "调控", "过程", "发生", "发展", "试验", "能力", "影响", "相关"]
    # generate_word_cloud("./database/中文基金.csv", filter_list=my_filter_list)
    cal_english_statistics_data("./database/JOURNAL_OF_CLINICAL_PERIODONTOLOGY.csv", 0, " ",
                                "[标题分析]JOURNAL_OF_CLINICAL_PERIODONTOLOGY")
    cal_english_statistics_data("./database/JOURNAL_OF_CLINICAL_PERIODONTOLOGY.csv", 1, ";",
                                "[关键词分析]JOURNAL_OF_CLINICAL_PERIODONTOLOGY")
    cal_english_statistics_data("./database/periodontology_2000.csv", 0, " ",
                                "[标题分析]periodontology_2000")
    cal_english_statistics_data("./database/periodontology_2000.csv", 1, ";",
                                "[关键词分析]periodontology_2000")
    cal_english_statistics_data("./database/journal_of_periodontal_research.csv", 0, " ",
                                "[标题分析]journal_of_periodontal_research")
    cal_english_statistics_data("./database/journal_of_periodontal_research.csv", 1, ";",
                                "[关键词分析]journal_of_periodontal_research")
    cal_english_statistics_data("./database/JOURNAL_OF_PERIODONTOLOGY.csv", 0, " ",
                                "[标题分析]JOURNAL_OF_PERIODONTOLOGY")
    cal_english_statistics_data("./database/JOURNAL_OF_PERIODONTOLOGY.csv", 1, ";",
                                "[关键词分析]JOURNAL_OF_PERIODONTOLOGY")
    print("运行完毕")
