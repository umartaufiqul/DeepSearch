# Copyright 2020 Max Planck Institute for Software Systems

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from imgntWrapper import *
from QLNES import *
from pickle import dump,load
import sys
from sys import argv
from datetime import datetime
from os import mkdir
from os.path import exists
if not exists("QLNES"):
    mkdir("QLNES")
path="QLNES/"+argv[1]+"_"+str(datetime.now())+"/"
mkdir(path)
sys.stdout=open(path+"log.txt","w")
Data={}
succ=0
tot=0
for j in range(0,1000,10):
    tot+=10
    print("Starting attack on batch", j//10)
    corr=np.argmax(mymodel.predict(x_test[j:j+10]),1)==y_test.reshape(-1)[j:j+10]
    ret=attack(mymodel,x_test[j:j+10],100,0.01,0.0001,0.0001,5,1,0.9,8/255,ongoing=corr,max_queries=10000)
    dump(ret[0].reshape(10,256,256,3),open(path+"image_"+str(j)+"_to_"+str(j+9)+".pkl","wb"))
    for k in range(10):
        Data[j+k]=(ret[2][k],ret[1][k])
    succ+=sum(ret[2])
    print("Success rate is",100*succ/tot)
    dump(Data,open(path+"QLNES_data.pkl","wb"))
