
# 2019.02.10 enhance logic counting mode, and demo also the time-tagging mode
# 2019.02.12 TJ: use the UQD logic to perform frequency analysis using the two modes

# demo to connect to .NET assembly for tagger from Python.
# used the pythonnet package for 3.6 32 bit, from here:
# https://pypi.org/project/pythonnet/#files
# and more info:  https://pythonnet.github.io/


#the main .NET syntax to call the library also works with IronPython, 2.7.9


#It turns out that even though the path was added:
#sys.path.insert(0,"C:\\dev\\proj_1\\")
#it  couldn't load the library because Windows was not allowing it to load from "external sources".

#To fix this:
#Right-click on the .dll file
#go to "Properties", Under "General", click "Unblock"


import time
import sys
import os 
import clr

#please change paths to the location of ttInterface.dll
dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'bin', 'ttInterface.dll'))
print("Loading DLL from:", dll_path)

clr.AddReference(dll_path)

from TimeTag import TTInterface, Logic
from System import Array, Byte, Int16, Int32, Int64, UInt32, UInt16
from TimeTag import TTInterface, Logic, UsbException


MyTagger=TTInterface()
MyTagger.Open()
#MyTagger.Open(1) # to open a specific number

result = MyTagger.GetFpgaVersion()
print("FPGA Version: " + str(result))

resolution = MyTagger.GetResolution()
print("Resolution: " + str(resolution))

NoInputs = MyTagger.GetNoInputs()
print("NO Inputs: " + str(NoInputs))


#set which channel to measure 1 ... 16  (156ps Firmware) or 1...8 for (78ps Firmware).
test_channel = 8

MyTagger.SetInputThreshold(test_channel, 0.5)

print("\n **************** Measure Frequency On Channel 2 **************** ")
print("connect onlye one signal on Channel %d (max 100 KHz, depends on your computer). Signal level > 1.0V \n" %(test_channel))
print("\n  ****************  Using TimeTag Mode  **************** ")

#Demo the Time Tagging mode to measure a freuency on a Channel:


MyTagger.StartTimetags()

#preallocate large buffer for channels and times, must be large enough to capture
#the expected number of events per read cycle (time between MyTagger.ReadTags)
chans = Array.CreateInstance(Byte, 10000000)
times = Array.CreateInstance(Int64, 10000000)

#run quick cycle to clear buffer
for i in range(0,5):
    time.sleep(0.1)
    (num_tags,chans,times)=MyTagger.ReadTags(chans,times)
    
for i in range(1,30):
    time.sleep(0.2)
    (num_tags,chans,times)=MyTagger.ReadTags(chans,times)
    tag_text=("Tags received: %d, " %(num_tags))
    if num_tags>1:
        diff=0;
        for k in range(1,num_tags-1):
            diff=(times[k]-times[k-1])+diff

        diff=diff/(num_tags-1)
        print(tag_text+ "Average periode [TTUnit]= %d, Avg. Per. [s]= %f s, Freq [Hz] = %.2f"\
              %(resolution, diff*resolution,1/(diff*resolution)))
    
MyTagger.StopTimetags()

print("\n **************** Using Logic Mode  **************** ")

#Activate the Logic Mode:
MyLogic =  Logic(MyTagger)
MyLogic.SwitchLogicMode()

TimerCounter1 = Int32

MyLogic.ReadLogic()

#measure channel k
k=test_channel

for i in range (1,20):
    time.sleep(1)
    MyLogic.ReadLogic()
    TimeCounter1 = MyLogic.GetTimeCounter()
    counts=MyLogic.CalcCountPos(2**(k-1))
    delta_t=(TimeCounter1)*5e-9
    delta_t_text = "Delta-T [s] = %.4f, " %(delta_t)
    counter_text = " Ch%d Events = %d," %(k,counts)
    freq_text = " Freq [Hz] = %.2f, " %(counts/delta_t)
    print(delta_t_text +counter_text + freq_text)
    

MyTagger.Close()
