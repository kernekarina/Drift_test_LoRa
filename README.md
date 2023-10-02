# Drift_test_LoRa
Automated drift test for LoRa device using Rohde and Schwarz spectrum analyzer

This test program uses 3 Python scripts to, respectively: 
1) turn on the device by calling a firmware command
2) read the measurement obtained in R&S spectrum analyzer and saves it to a CSV file 
3) plot the resulting data.

The other Python file is used to call these 3 scripts.

We chose to execute 5 different measurements for each device to analyze the data, so, in each plot, we have 5 different curves for the same device with approximately 3min between them.

The data obtained with the tests are stored in the archive folder and we (manually) separated the data for each device putting it in another folder inside the archive with the name of the device.

So, when the plotting code asks which folder contains the data you want to plot, you specify the one with contains the data of the device you want to analyze. 
