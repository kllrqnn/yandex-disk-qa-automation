from faker import Faker


class DiskFaker:
    def __init__(self):
        self.fake = Faker()

    def random_folder_name(self):
        return f"folder_{self.fake.word()}_{self.fake.random_int(1, 999)}"

    def random_text_content(self):
        return self.fake.paragraph(nb_sentences=3)
