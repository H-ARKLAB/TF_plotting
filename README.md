# TF_plotting
## Made by Jiwon Kim (Update date: 25.10.28)

***Explanation***

This code is to plot the TFs according to their PWM scores.

***Things to do***

To run the code, you need two csv or txt files (txt files are recommended)
* occupancy
* sites

Kindly teach you how to get the files ㅎ
* unfold --occupancy --gene LDLR_washington -i your_file_name.txn --invert > occupancy.txt
* unfold --sites -i your_file_name.txt --invert > sites.txt

You can send the files from Ubuntu to your local laptop or vice versa (Chat GPT can kindly explain, but I am also kind)
* If Ubuntu --> Local laptop
  * scp /path/to/Ubuntu username@remote_IP:/path/to/Local
  * ex) scp ./occupancy.txt jiwonkim@192.168.36.12:/Users/jiwonkim/Downloads

* If Local laptop --> Ubuntu
  * scp /path/to/Local username@remote_IP:/path/to/Ubuntu
  * ex) scp Downloads/sites.txt jwkim@192.168.36.10:/NAS/home/jwkim

The IP address of local can be found in the wifi setting or entering 'ipconfig getifaddr en0' in terminal

The IP address of Ubuntu is easily found by entering 'ip a'


