automated drift test for LoRa device using Rohde&Schwarz spectrum analyser

This test program use 3 python scripts to, respectively: 
1) turn on the device calling a firmware command
2) read the measurement obtained in R&S spectrum analyser saving it to a csv file 
3) plot the resulted data.

The other python file is used to call these 3 scripts.

We choosed to execute 5 diferent measurements for each device to analyse the data, so, in each plot, we have 5 diferent curves for the same device with approximately 3min bethween them.

The data obtained with the tests are stored in the archive folder and we (manualy) separated the data for each device putting it in another folder inside archive with the name of the device.

So, when the plotting code ask wich folder contains the data you want to plot, you specify the one with cotains the data of the device you want to analyse. 