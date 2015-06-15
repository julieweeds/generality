__author__ = 'juliewe'
#15/6/15

def configure(arguments):

    parameters={}
    parameters["thesdir"]="/home/j/ju/juliewe/Documents/workspace/ThesEval/data/wikiPOS_t100f100_nouns_deps/"
    parameters["thesfile"]="wikiPOS.nouns.events"
    parameters["entryindex"]="wikiPOS.nouns.entryIndex.0"
    parameters["featureindex"]="wikiPOS.nouns.featureIndex.0"

    parameters["reiterate"]=False

    for arg in arguments:
        if arg=="reiterate":
            parameters["reiterate"]=True

    return parameters