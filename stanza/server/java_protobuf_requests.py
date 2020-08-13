import subprocess

from stanza.server.client import resolve_classpath

def send_request(request, response_type, java_main):
    """
    Use subprocess to run a Java protobuf processor on the given request

    Returns the protobuf response
    """
    pipe = subprocess.run(["java", "-cp", resolve_classpath(), java_main],
                          input=request.SerializeToString(),
                          stdout=subprocess.PIPE)
    response = response_type()
    response.ParseFromString(pipe.stdout)
    return response

def add_token(token_list, word, token):
    """
    Add a token to a proto request.

    CoreNLP tokens have components of both word and token from stanza.
    """
    query_token = token_list.add()
    query_token.word = word.text
    query_token.value = word.text
    if word.lemma is not None:
        query_token.lemma = word.lemma
    if word.xpos is not None:
        query_token.pos = word.xpos
    if word.upos is not None:
        query_token.coarseTag = word.upos
    if token.ner is not None:
        query_token.ner = token.ner

def add_word_to_graph(graph, word, sent_idx, word_idx):
    """
    Add a node and possibly an edge for a word in a basic dependency graph.
    """
    node = graph.node.add()
    node.sentenceIndex = sent_idx+1
    node.index = word_idx+1

    if word.head != 0:
        edge = graph.edge.add()
        edge.source = word.head
        edge.target = word_idx+1
        edge.dep = word.deprel
