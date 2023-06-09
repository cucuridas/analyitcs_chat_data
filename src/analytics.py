from krwordrank.word import KRWordRank
from konlpy.tag import *
from collections import Counter
from wordcloud import WordCloud
from src.commonUtil import Common
from src.graph import *
import pandas as pd
import matplotlib.pyplot as plt
import itertools


class ConvertDataFrame:
    """
    입력받은 object를 dataframe 형태로 변환합니다
    """

    def convert(column_data: list, original_data: object):
        """
        입력받은 값을 dataframe 형태로 변환합니다

        input:
            column_data(list): dataframe에서 header가 될 목록
            original_data(object): 변환할 원본 데이터 오브젝트


        return:
            dataframe(DataFrame): 입력받은 값을 dataframe화 한 object
        """
        dataframe = pd.DataFrame(data=original_data, columns=column_data)
        return dataframe


class Report:
    pass


STOPWORDS = ["네", "완료", "혹시", "수고", "린지", "네네"]


class WordAnalytics:
    """
    단어를 통해 시각화하는 클래스이며 wordCloud를 통해 시각화를 checkFrequency를 통해 단어의 빈도를 확인합니다
    """

    def __init__(self, word_rank: bool = False) -> None:
        if word_rank:
            self.wordrank_extractor = KRWordRank(
                min_count=3,  # 단어의 최소 출현 빈도수 (그래프 생성 시)
                max_length=15,  # 단어의 최대 길이
                verbose=True,
            )
        self.okt_obj = Okt()

    def extractKrwordrank(self, dataframe: pd.DataFrame, text_filed_name: str):
        """
        Krwordrank 모듈을 통해 단어의 빈도수를 확인합니다
        해당 모듈에 사용되어진 알고리즘으로인해 형태소분석을 통한 단어의 원형을 기준으로 빈도를 삼는것이아님으로
        값의 형태가 달라질 수 있습니다

        input:
            dataframe: 빈도를 확인할 dataframe object

        returns:

        """
        texts = dataframe[text_filed_name].values.tolist()
        keywords, rank, graph = self.wordrank_extractor.extract(texts)

        for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
            print("%8s:\t%.4f" % (word, r))

    def extractKonlpy(self, dataframe: pd.DataFrame, text_filed_name: str):
        return_words_frequency = {}

        nouns = self.okt_obj.nouns(dataframe.to_string(columns=[text_filed_name]))
        # counter를 통한 전체 단어 빈도 집계
        all_words_frequency = Counter(nouns)

        # 단어의 길이가 띄어쓰기를 제외하고 1개인 단어 제외, 빈도의 갯수가 5이하인항목 제외
        for key, value in all_words_frequency.items():
            if len(key.strip()) > 1 and value > 5:
                return_words_frequency[key] = value

        # 정렬
        sort_value = sorted(return_words_frequency.items(), key=lambda x: x[1], reverse=True)
        # 출력 및 리턴
        print(sort_value)
        return return_words_frequency

    def wordcloudAnalysis(frequency_words: dict):
        MAC_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
        wc = WordCloud(width=1000, height=1000, scale=3.0, max_font_size=250, font_path=MAC_PATH)

        sort_data_dict = Common.excludeSort(frequency_words, STOPWORDS, True)
        slice_data = dict(itertools.islice(sort_data_dict.items(), 25))
        gen = wc.generate_from_frequencies(slice_data)

        plt.figure()
        plt.imshow(gen)

        report_path = Common.makeDir(WORKING_DIR)
        Graph.saveImage(gen, report_path)

    def barplotAnalysis(frequency_words: dict):
        """
        집계한 단어 데이터를 막대그래프를 통해 나타냅니다
        figure를 통해 화면에 띄운뒤 특정 디렉토리에 저장합니다

        Args:
            frequency_words (dict): 단어:빈도수의 dict의 집합
        """
        sort_data = Common.excludeSort(frequency_words, STOPWORDS)[:25]
        column_data = ["words", "count"]
        df = ConvertDataFrame.convert(column_data, sort_data)

        Graph().makeGraph(df, "bar")

    def pieplotAnalysis(frequency_words: dict):
        """
        집계한 단어 데이터를 파이그래프를 통해 나타냅니다
        figure를 통해 화면에 띄운뒤 특정 디렉토리에 저장합니다

        Args:
            frequency_words (dict): 단어:빈도수의 dict의 집합
        """
        sort_data = Common.excludeSort(frequency_words, STOPWORDS)[:25]
        column_data = ["words", "count"]
        df = ConvertDataFrame.convert(column_data, sort_data)

        Graph().makeGraph(df, "pie")
