import wikipedia
import spacy

# from spacy.token import Doc

nlp_model = spacy.load('en')


def proper_nouns_for_sent(sent):
    nouns = list(sent.noun_chunks)
    if not nouns:
        return set()
    proper_nouns = set()
    for noun in nouns:
        to_add = True
        for token in noun:
            print (token)
            if token.pos_ != 'PROPN':
                to_add = False
                break
        if to_add:
            proper_nouns.add(noun)
    return proper_nouns


def pairs_for_sents(proper_nouns, doc):
    triplet = []
    for noun1 in proper_nouns:
        for noun2 in proper_nouns:
            # print(noun1, noun2)
            ind1 = noun1[-1].i
            ind2 = noun2[0].i

            found_verb = False
            found_punct = False

            relations = list()

            for i in range(ind1 + 1, ind2):
                token = doc[i]
                if token.pos_ == 'VERB':
                    relations.append(token)
                    found_verb = True
                elif token.pos_ == 'ADP':
                    relations.append(token)
                elif token.pos_ == 'PUNCT':
                    found_punct = True
                    break
            if not found_punct and found_verb:
                triplet.append((noun1, relations, noun2))
    return triplet


def extractor_by_pos(document):
    doc = nlp_model(document)
    sents = list(doc.sents)
    relations_dict = {}

    for i, sent in enumerate(sents):
        # PART A
        proper_nouns = proper_nouns_for_sent(sent)

        # Need at least 2 proper nouns to create pairs
        if len(proper_nouns) <= 1:
            continue

        # PART B
        triplet = pairs_for_sents(proper_nouns, doc)

        # Need at least 1 pair to create relations
        if len(triplet) < 1:
            continue

        relations_dict[i] = triplet

    return relations_dict


def extractor_by_dependency_tree():
    pass


def evaluation():
    pass


def main():
    page = wikipedia.page('Brad Pitt').content
    dict_by_pos = extractor_by_pos(document=page)
    print(dict_by_pos)

    # extractor_by_dependency_tree()
    # evaluation()


if __name__ == '__main__':
    main()
