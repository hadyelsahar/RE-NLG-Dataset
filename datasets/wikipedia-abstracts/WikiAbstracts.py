
# coding: utf-8

# In[1]:

from __future__ import print_function
import re
import sys
import cPickle as pickle


# In[2]:

datasetDirectory = './Wikipedia Abstracts/Data/'
hashDirectory = './Wikipedia Abstracts/hashTable.p'
def generateCheckpoint(hashedDataset, dataset, fileNumber, end):
    print('\r{} items have been processed... '.format((fileNumber - 1) * 500000 + len(dataset)), end='')
    if end is False and len(dataset) % 500000 == 0 and len(dataset) > 0:
        fileLocation = datasetDirectory + ('%d.p' % (fileNumber))
        # Comment-out for better performance.
        # pickle.dump(hashedDataset, open( hashDirectory, "wb" ) )
        pickle.dump(dataset, open(fileLocation, "wb" ) )
        print('Checkpoint file has been successfully stored at: %s...' % (fileLocation))
        del dataset [:]
        fileNumber += 1
    elif end is True:
        fileLocation = datasetDirectory + ('%d.p' % (fileNumber))
        pickle.dump(hashedDataset, open( hashDirectory, "wb" ) )
        pickle.dump(dataset, open(fileLocation, "wb" ) )
        print('Last checkpoint file has been successfully stored at: %s...' % (fileLocation))
        del dataset [:]
    return fileNumber


# In[3]:

abstractsDirectory = './Wikipedia Abstracts/long_abstracts_en.tql' 
items = []
item2pos = {}
fileNumber = 1
with open(abstractsDirectory) as abstractsFile:
    linePageTitle = ''
    for line in abstractsFile:
        line = line.split()
        tempSubject = line[0]
        tempUrl = line[-2]
        
        line[0] = ''
        line[-2] = ''
        line = ' '.join(line)
        tempObject = re.findall(r"(?<=\")(.*)(?=\"@en)", line)
        if len(tempObject) == 0: tempObject = re.findall(r"(?<=\")(.*)(?=\"\^\^)", line)


        if len(tempObject) > 0:
            tempPageTitle = re.findall(r"(?<=en\.wikipedia\.org\/wiki\/)(.*)(?=\?oldid=)", tempUrl)[0]
            if linePageTitle != tempPageTitle:
                fileNumber = generateCheckpoint(item2pos, items, fileNumber, False)
                

                items.append({'formalPageTitle': tempPageTitle})
                items[len(items) - 1]['summary'] = tempObject[0]
                items[len(items) - 1]['url'] = re.sub(r'\?oldid=.*$', '', tempUrl[1:-1])
                item2pos[tempPageTitle] = [('%d.p' % (fileNumber)), len(items) - 1]
                linePageTitle = tempPageTitle
        else:
            print (line)
    generateCheckpoint(item2pos, items, fileNumber, True)


# In[ ]:



