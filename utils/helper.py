import re


class ScraperHelper(object):
    float_pattern = re.compile(r'\b\d+\.\d+\b')
    indexing_pattern = re.compile(r'(\d+)\.\s(.*?)(?=\n\d+\.|\Z)', re.DOTALL)

    @staticmethod
    def format_float(num_str: str) -> str:
        """num_str: 1.000 returns 1

        num_str: 1.100 returns 1.1
        """
        return str(int(float_value)) if (float_value := float(num_str)).is_integer() else str(float_value)

    def replace_numbers(self, texts: list | str) -> list:
        """texts: a list of strings

            returns:
             - prettified list of texts"""
        if isinstance(texts, str):
            texts = [texts]

        for i, text in enumerate(texts):
            c_text = self.float_pattern.sub(lambda match: self.format_float(match.group(0)), text)
            c_text = ' '.join(c_text.replace('\xa0', '').replace('\n', '').split())

            texts[i] = c_text

        return texts

    def index_steps(self, steps_text: str) -> list[tuple[int, str] | None]:
        """indexes steps in the text

            returns:
                >>> list[tuple[int, str]]
        """
        matches = self.indexing_pattern.findall(steps_text)

        return [(int(step), description.strip()) for step, description in matches]
