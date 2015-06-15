__author__ = 'juliewe'
#15/6/15

import sys
from conf import configure

class Indexer:

    def __init__(self,parameters):
        self.parameters=parameters

    def initialiseIndices(self):
        entryfile=self.parameters["entryindex"]
        featurefile=self.parameters["featureindex"]
        self.entryindex=self.readIndex(entryfile)
        self.featureindex=self.readIndex(featurefile)



    def readIndex(self,filename):
        index={}
        if self.parameters["reiterate"]:
            try:
                with open(filename) as instream:
                    for line in instream:
                        line=line.rstrip()
                        fields=line.split("\t")
                        index[fields[0]]=float(fields[1])

            except:
                print "No existing index file "+filename+", defaulting to uniform initial index"

        return index

    def outputIndices(self):
        entryfile=self.parameters["entryindex"]
        featurefile=self.parameters["featureindex"]
        parts=entryfile.split(".")
        iteration=int(parts[-1])+1
        newentryfile=self.join(parts[:len(parts)-1],".")+"."+str(iteration)
        parts=featurefile.split(".")
        newfeaturefile=self.join(parts[:len(parts)-1],".")+"."+str(iteration)
        self.output(self.entryindex,newentryfile)
        self.output(self.featureindex,newfeaturefile)

    def join(self,alist,achar):
        if len(alist)>1:
            astring=alist[0]
            for value in alist[1:]:
                astring+=achar+value
            return astring
        elif len(alist)==1:
            return alist[0]
        else:
            return ""

    def output(self,index,filename):
        with open(filename,"w") as outstream:
            for entry in index.keys():
                outstream.write(entry+"\t"+str(index[entry])+"\n")

    def processEventFile(self):
        infile=self.parameters["thesdir"]+self.parameters["thesfile"]
        newentryindex={}
        newfeatureindex={}
        reversewidth={}
        reversefreq={}
        with open(infile) as instream:
            lines=0
            for line in instream:
                line=line.rstrip()
                if lines%100==0:print "Processed "+str(lines)+" lines"
                lines+=1
                fields=line.split("\t")
                entry=fields[0]
                gen_of_entry=0
                width=0
                totalfreq=0
                while len(fields[1:])>0:
                    freq=float(fields.pop())
                    feat=fields.pop()
                    width+=1
                    totalfreq+=freq
                    gen_of_feat=self.featureindex.get(feat,1)
                    gen_of_entry+=gen_of_feat
                    #now for reverse feature index
                    reversewidth[feat]=reversewidth.get(feat,0)+1
                    reversefreq[feat]=reversefreq.get(feat,0)+freq
                    newfeatureindex[feat]=newfeatureindex.get(feat,0)+self.entryindex.get(entry,1)
                newentryindex[entry]=gen_of_entry*width/totalfreq

        for feat in newfeatureindex.keys():
            newfeatureindex[feat]=newfeatureindex[feat]*reversewidth[feat]/reversefreq[feat]

        self.entryindex=newentryindex
        self.featureindex=newfeatureindex


    def run(self):
        self.initialiseIndices()
        self.processEventFile()
        self.outputIndices()

if __name__=="__main__":
    myIndex=Indexer(configure(sys.argv))
    myIndex.run()