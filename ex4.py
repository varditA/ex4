import wikipedia
import spacy
import random

# from spacy.token import Doc

nlp_model = spacy.load('en')


# ----------------------------- Part A ---------------------------------------
def proper_nouns_for_sent_by_pos(doc):
    tokens = list(doc)
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


# def pairs_for_sents(proper_nouns, doc):
#     triplet = []
#     for i in range(len(proper_nouns) - 1):
#         noun1 = proper_nouns[i]
#         noun2 = proper_nouns[i+1]
#
#         ind1 = noun1[-1].i
#         ind2 = noun2[0].i
#
#         found_verb = False
#         found_punct = False
#
#         relations = list()
#
#         for i in range(ind1 + 1, ind2):
#             token = doc[i]
#             if token.pos_ == 'VERB':
#                 relations.append(token)
#                 found_verb = True
#             elif token.pos_ == 'ADP':
#                 relations.append(token)
#             elif token.pos_ == 'PUNCT':
#                 found_punct = True
#                 break
#         if not found_punct and found_verb:
#             triplet.append((noun1, relations, noun2))
#     return triplet


def extractor_by_pos(document):
    doc = nlp_model(document)
    relations_list = []

    # PART A
    proper_nouns = proper_nouns_for_sent_by_pos(doc)

    # Need at least 2 proper nouns to create pairs
    if len(proper_nouns) <= 1:
        return []

    # PART B
    triplet = pairs_for_sents(proper_nouns, doc)

    # Need at least 1 pair to create relations
    if len(triplet) < 1:
        return []

    for relation in triplet:
        relations_list.append(relation)

    return relations_list


# ----------------------------- Part B ---------------------------------------

def proper_nouns_for_sent_by_tree(doc):
    proper_nouns = []
    tokens = list(doc)
    for token in tokens:
        if token.pos_ == 'PROPN' and token.dep_ != 'compound':
            token_list = [token]
            for child in token.children:
                if child.dep_ == 'compound':
                    token_list.append(child)
            proper_nouns.append(token_list)

    return proper_nouns


def condition1(noun1, noun2):
    head1 = noun1[0]
    head2 = noun2[0]
    if head1.head != head2.head:
        return None
    if head1.dep_ == 'nsubj' and head2.dep_ == 'dobj':
        return noun1, head1.head, noun2
    return None


def condition2(noun1, noun2):
    head1 = noun1[0]
    head2 = noun2[0]
    if head1.head != head2.head.head:
        return None
    if head1.dep_ == 'nsubj' and head2.dep_ == 'pobj' and head2.head.dep_ == 'prep':
        if head2.head.i < head2.head.head.i:
            print("in1")
            # print(head2.head.i, head2.head.head.i)
            print(head2.head, head2.head.head)
            return noun1, head2.head.head.text + " " + head2.head.text, noun2
        else:
            print("in2")
            # print(head2.head.i, head2.head.head.i)
            print(head2.head, head2.head.head)
            return noun1, head2.head.head.text + " " + head2.head.text, noun2
    return None


def define_relations(proper_nouns):
    triplet = []
    for noun1 in proper_nouns:
        for noun2 in proper_nouns:
            relation = condition1(noun1, noun2)
            if relation:
                triplet.append(relation)
            else:
                relation = condition2(noun1, noun2)
                if relation:
                    triplet.append(relation)

    return triplet


def extractor_by_dependency_tree(document):
    doc = nlp_model(document)
    # sents = list(doc.sents)
    relations_list = []

    proper_nouns = proper_nouns_for_sent_by_tree(doc)

    # Need at least 2 proper nouns to create pairs
    if len(proper_nouns) <= 1:
        return []

    triplet = define_relations(proper_nouns)
    # Need at least 1 pair to create relations
    if len(triplet) < 1:
        return []

    for relation in triplet:
        sub = sorted(relation[0], key=lambda token_in: token_in.i)
        # rel = sorted(relation[1], key=lambda token_in: token_in.i)
        obj = sorted(relation[2], key=lambda token_in: token_in.i)
        relations_list.append([sub, relation[1], obj])

    return relations_list


# ----------------------------- Part C ---------------------------------------


def evaluation():
    page_pitt = wikipedia.page('Brad Pitt').content
    page_trump = wikipedia.page('Donald Trump').content
    page_jolie = wikipedia.page('Angelina Jolie').content

    # pages = [page_trump, page_pitt, page_jolie]
    pages = [page_trump]

    # evaluation for pos
    # for page in pages:
    #     pos_list = extractor_by_pos(document=page)
    #     print(len(pos_list))
    #     random.shuffle(pos_list)
    # print(pos_list[:30])

    # evaluation for tree
    for page in pages:
        tree_list = extractor_by_dependency_tree(document=page)
        print(len(tree_list))
        for sentence in tree_list:
            print(sentence)
        random.shuffle(tree_list)
    #     # print(tree_list[:30])


def main():
    evaluation()


if __name__ == '__main__':
    main()
