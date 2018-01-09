import wikipedia
import spacy

# from spacy.token import Doc

nlp_model = spacy.load('en')
page = wikipedia.page('Brad Pitt').content
analyzed_page = nlp_model(page)


def extractor_by_pos():
    pass


def extractor_by_dependency_tree():
    pass


def evaluation():
    pass


def main():
    print("hello world")
    # extractor_by_pos()
    # extractor_by_dependency_tree()
    # evaluation()


if __name__ == '__main__':
    main()
