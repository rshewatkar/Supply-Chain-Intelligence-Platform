from app.preprocessing.text_cleaner import TextCleaner


def test_clean_text():

    raw = """



    Apple      Inc.


        manufactures      iPhones.






    """

    cleaned = TextCleaner.clean_text(raw)

    assert "Apple Inc." in cleaned

    assert "manufactures iPhones." in cleaned