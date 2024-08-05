class VisualizationManager:
    def __init__(self, source_code=""):
        self.source_code = source_code
        self.processed_lines = self.process_code()
        self.depth = 1

    def process_code(self):
        # 줄 단위로 분리
        lines = self.source_code.split("\n")
        processed_lines = []

        for line in lines:
            # 줄의 시작 부분에서 공백 제거 (들여쓰기 제거)
            stripped_line = line.lstrip()
            # 공백이 아닌 내용이 있는 경우만 추가
            if stripped_line:
                processed_lines.append(stripped_line)
            else:
                processed_lines.append(None)

        return processed_lines

    def increase_depth(self):
        self.depth = self.depth + 1
        return self.depth

    def get_depth(self):
        return self.depth

    def decrease_depth(self):
        self.depth = self.depth - 1
        return self.depth

    def get_code_by_idx(self, idx):
        # idx에 해당하는 코드 라인 리턴
        return self.processed_lines[idx - 1]
