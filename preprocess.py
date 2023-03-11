import re


class Preprocess:
    """
    해당 클래스 정규표현식을 통해 zoom meeting chating 데이터를 파싱하는 클래스입니다
    """

    def __init__(self) -> None:
        self.split_pattern = r"\d{2}:\d{2}:\d{2}"
        self.parse_pattern = r"(?P<timeStamp>\d{2}:\d{2}:\d{2}) 시작 (?P<userName>.*?) (?P<target>[송신자|수신자]+) (?P<targetRange>\w+):(?P<userChatData>[\W|\w]+)"
        self.file_data = None

    def load_file(self, file_path: str):
        """
        파일을 읽어와 원하는 형태의 리스트 데이터로 적재합니다

        input :
            file_path(str): 읽어올 파일의 위치

        return :
            self.filed_data(list[str]): 특정 기준으로 잘려져 나온 list 데이터

        """
        with open(file_path, "r") as f:
            self.file_data = self.split_data(f.read())
        return self.file_data

    def split_data(self, file_data: str):
        """
        읽어온 데이터를 timestamp 단위로 자릅니다

        input :
            file_data: str

        return :
            outputs: list[str]
        """
        split_indices = [m.start(0) for m in re.finditer(self.split_pattern, file_data)]
        outputs = [
            file_data[i:j].strip()
            for i, j in zip(split_indices, split_indices[1:] + [None])
        ]
        return outputs

    def parse(self, original_data: str):
        """
        입력받은 데이터를 regex를 통해 파싱하여 필요데이터를 찾습니다

        input:
            original_data(str): 파싱할 원본 데이터

        return:
            parse_data(tuple(str)): regex에 의해서 파싱한 데이터들의 집합(tuple)
        """
        parse_obj = re.match(self.parse_pattern, original_data)
        parse_data = parse_obj.groups()
        return parse_data

    def preprocessing(self, file_path: str):
        """
        파일 데이터를 읽어와 정규표현식을 통해 데이터 전처리 작업을 진행합니다

        input:
            file_path(str): 전처리하고자하는 파일의 위치를 입력 받습니다

        return:
            preprocessing_data(list(tupe(str))): 전처리가되어 파싱된 데이터들의 집합 리스트를 return 합니다
        """
        self.load_file(file_path)
        preprocessing_data = list(map(self.parse, self.file_data))

        return preprocessing_data
