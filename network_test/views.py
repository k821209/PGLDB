from django.shortcuts import render
from .models import AI1
import numpy as np
from django import forms

class NameForm_gene(forms.Form):
#    gene_name = forms.CharField(label='gene name', max_length=1000)
    gene_names = forms.CharField(widget=forms.Textarea)


def edge2json(test):
    test = np.array(test)
    elements = list(set(np.ravel(test)))

    nodes = ''
    for n,e in enumerate(elements):
        group = '"group" : %d'%n
        name  = '"name" : "%s"'%e 
        nodes += "{%s, %s},\n"%(group,name)
    nodes = nodes.rstrip().rstrip(',')    

    links = ''
    for e in test:
        source = '"source" : %d'%elements.index(e[0])
        target = '"target" : %d'%elements.index(e[1])
        value  = '"value" : 1'
        links += "{%s ,%s, %s},\n"%(source,target,value)
    links = links.rstrip().rstrip(',')
    final = '{"links" : [%s] ,"nodes" : [%s]}'%(links,nodes)
    return final

def index(request):
    #DBex    = DBmodel.objects.order_by('?')[0:2] # 렌덤으로 클레스를 가져온다.

    if request.method=='POST':
        form = NameForm_gene(request.POST)
        if form.is_valid():
            genes         = form.cleaned_data['gene_names'].split(',')
            print(genes)
            form          = NameForm_gene()
            edges = []
            for gene in genes: 
                network1 = AI1.objects.filter(source=gene) 
                edges1   = [[x.source, x.target] for x in network1]
                edges += edges1
            json     = edge2json(edges)
            #print(json)
            jsonfilename = './network_test/static/%s.json'%'.'.join(genes)
            with open(jsonfilename,'w') as f:
                print(json,file=f)
#           return render(request, 'network_test/index.html',{'form': form,'query':','.join(genes)}) # 렌덤으로 가져온 클레스를 html로 보낸다. 
            return render(request, 'network_test/index.html',{'jsonf':jsonfilename.split('/')[-1],'form':form,'query':','.join(genes)})
#           return render(request, 'network_test/index.html',{'json':json,'form':form,'query':','.join(genes)})

    else:
        form = NameForm_gene()
        return render(request, 'network_test/index.html',{'jsonf':'temp.json','form': form,'query':"AT5G52470,AT5G43080,AT1G71230,AT1G22920"})

