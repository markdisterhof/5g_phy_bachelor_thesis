# 5G NR (New Radio) (The 3rd Generation Partnership Project 3GPP)
## Use Cases:
* Modi:
    * Enhanced Mobile Broadband (eMBB)
        * High troughput
    * Massive Machine Communication (mMTC)
        * High Number of served devices
    * Ultra Reliability and Low Latency (URLLC)
        * Low Latency
* Ermöglichen Anpassung ans Problem
    * Ausdehnung Zeit-/Frequenzbereich
        * Out-of-Band Interferenzen
        * Latency


___
## Frame Structure
* http://nomor.de/wp-content/uploads/2018/04/2017-08-WhitePaperNomor-5G-Frame-Structure-v1-2.pdf

### SCS (subcarrier spacing)

Werden Signale über modulierte Unterträger übertragen, dann müssen die Frequenzbänder der Unterträger einen bestimmten Frequenzabstand voneinander haben.
Liegen die Unterträger zu dicht nebeneinander und überlappen sich deren Frequenzbänder, dann beeinflussen sich die modulierten Unterträger gegenseitig und es entstehen Interferenzen. Um dies auf jeden Fall zu vermeiden ist in aller Regel zwischen den Unterfrequenzbändern noch ein Sicherheits-Frequenzband. Der Frequenzabstand der Unterträger heißt im Englischen Subcarrier Spacing (SCS) und entspricht annähernd der Bandbreite des Unterträgerkanals.
* SCS sind bei NR 2er Potenzen-Vielfache von 15kHz (2^µ * 15kHz)
    ![SCS](./img/Screenshot_20201017_173352.png)
    * (_Meist ohne m=-2?_)

* 15kHz LTE Standard

### NR Frame Hierarchie
* Unterschiedliche Use Cases erfordern neue Frame Structures (Aufbau) um Services wie URLLC zu ermöglichen 
* Unterschiedliche Strukturen müssen immernoch synchronisiert werden, um Flexibilität zu ermöglichen 

* Timing je nach:
    * data block transmission 
    * symbol transmission
    * synchronisation 

* 5G  frame  structures  provide  a  fixed  overall structure for defining data block transmission timing.  Radio  frames  and  subframes  are  of fixed lengths (figure 1). They are chosen to be the same as in LTE, thereby allowing for better LTE-NR co-existence
![](./img/Screenshot_20201017_173830.png)

* In case of co-site deployment,  slot-  and  frame  structures  may be  aligned  to  simplify  cell  search  and  inter-frequency  measurements


### Numerology
* In  order  to  support  multiple  numerologies independent  of  data  block  transmission timing,  5G  frame  structures  also  provide flexible  substructures  for  defining  symbol transmission timing. 
* Slots and symbols are of flexible lengths and depend  on  subcarrier  spacing  (figure  1). Synchronisation timing is defined in terms of fixed  frame  structures  and  in  terms  of synchronisation  signal  bursts  and  burst  sets

### Mini-Slots
Mini-Slots 5G defines a subslot structure called a mini-slot. Mini-slots can be used for: 
* low latency applications such as Ultra Reliable Low Latency Communications (URLLC) 
* operation in unlicensed bands (e.g. to start  transmission  directly  after  a successful listen-before-talk procedure without waiting for the slot boundary)
