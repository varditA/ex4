import wikipedia
import spacy

# from spacy.token import Doc

nlp_model = spacy.load('en')


# ----------------------------- Part A ---------------------------------------
def proper_nouns_for_sent_by_pos(sent):
    tokens = list(sent)
    proper_nouns = []
    curr_set = []
    for token in tokens:
        if token.pos_ == 'PROPN':
            curr_set.append(token)
        elif curr_set and token.pos_ != 'PROPN':
            proper_nouns.append(curr_set)
            curr_set = []
    return proper_nouns


def pairs_for_sents(proper_nouns, doc):
    triplet = []
    for noun1 in proper_nouns:
        for noun2 in proper_nouns:
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
        proper_nouns = proper_nouns_for_sent_by_pos(sent)

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


# ----------------------------- Part B ---------------------------------------

def proper_nouns_for_sent_by_tree(sent):
    proper_nouns = []
    tokens = list(sent)
    for token in tokens:
        print(token, token.pos_)
        if token.pos_ == 'PROPN' and token.dep_ != 'compound':
            token_list = [token]
            for child in token.children:
                if child.dep_ == 'compound':
                    token_list.append(child)
            proper_nouns.append(token_list)

    return proper_nouns


def extractor_by_dependency_tree(document):
    doc = nlp_model(document)
    sents = list(doc.sents)
    relations_dict = {}

    for i, sent in enumerate(sents):
        print(sent, "===================")
        # PART A
        proper_nouns = proper_nouns_for_sent_by_tree(sent)
        proper_nouns2 = proper_nouns_for_sent_by_pos(sent)
        print(proper_nouns, proper_nouns2)
        # Need at least 2 proper nouns to create pairs
        if len(proper_nouns) <= 1:
            continue

            # PART B
            # triplet = pairs_for_sents(proper_nouns, doc)

            # Need at least 1 pair to create relations
            # if len(triplet) < 1:
            #     continue

            # relations_dict[i] = triplet

    return relations_dict

# ----------------------------- Part C ---------------------------------------


def evaluation():
    pass


def main():
    page = wikipedia.page('Brad Pitt').content
    dict_by_pos = extractor_by_pos(document=page)
    print(dict_by_pos)

    dict_by_tree = extractor_by_dependency_tree(document=page)
    # evaluation()


if __name__ == '__main__':
    main()
