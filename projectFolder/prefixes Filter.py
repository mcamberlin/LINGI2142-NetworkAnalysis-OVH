# -*- coding: utf-8 -*-
"""
Routes selector
"""
import pandas as pd

dataCgtIPv4 = pd.read_csv("prefixes_cogent_IPv4.csv",sep=';' );
dataCgtIPv6 = pd.read_csv("prefixes_cogent_IPv6.csv",sep=';' );

dataGglIPv4 = pd.read_csv("prefixes_google_IPv4.csv",sep=';' );
dataGglIPv6 = pd.read_csv("prefixes_google_IPv6.csv",sep=';' );

dataLvlIPv4 = pd.read_csv("prefixes_level3_IPv4.csv",sep=';' );
dataLvlIPv6 = pd.read_csv("prefixes_level3_IPv6.csv",sep=';' );

dataTelIPv4 = pd.read_csv("prefixes_telia_IPv4.csv",sep=';' );
dataTelIPv6 = pd.read_csv("prefixes_telia_IPv6.csv",sep=';' );


prefixesCgtIPv4 = dataCgtIPv4['Announced Prefix'].values
prefixesCgtIPv6 = dataCgtIPv6['Announced Prefix'].values


prefixesGglIPv4 = dataGglIPv4['Announced Prefix'].values
prefixesGglIPv6 = dataGglIPv6['Announced Prefix'].values


prefixesLvlIPv4 = dataLvlIPv4['Announced Prefix'].values
prefixesLvlIPv6 = dataLvlIPv6['Announced Prefix'].values


prefixesTelIPv4 = dataTelIPv4['Announced Prefix'].values
prefixesTelIPv6 = dataTelIPv6['Announced Prefix'].values


# ========== IPv4 ==========

Myfile = open('IPv4 prefixes selected.txt','w');
 
for cgtPrefix in prefixesCgtIPv4:
    
    for gglPrefix in prefixesGglIPv4:
        if(cgtPrefix == gglPrefix):
            Myfile.write(cgtPrefix + " - Cogent-Google \n");
            
    for lvlPrefix in prefixesLvlIPv4:
        if(cgtPrefix == lvlPrefix):
            Myfile.write(cgtPrefix + " - Cogent-Level3 \n");
            
    for telPrefix in prefixesTelIPv4:
        if(cgtPrefix == telPrefix):
            Myfile.write(cgtPrefix + " - Cogent-Telia \n");   
            
            
            
for gglPrefix in prefixesGglIPv4:
            
    for lvlPrefix in prefixesLvlIPv4:
        if(gglPrefix == lvlPrefix):
            Myfile.write(gglPrefix + " - Google-Level3 \n");
            
    for telPrefix in prefixesTelIPv4:
        if(gglPrefix == telPrefix):
            Myfile.write(gglPrefix + " - Google-Telia \n"); 
            
        
for lvlPrefix in prefixesLvlIPv4:
                
    for telPrefix in prefixesTelIPv4:
        if(lvlPrefix == telPrefix):
            Myfile.write(lvlPrefix + " - Level3-Telia \n"); 
          
Myfile.close();
print("========== Finished for IPv4 ==========")


# ========== IPv6 ==========

Myfile2 = open('IPv6 prefixes selected.txt','w'); 

for cgtPrefix in prefixesCgtIPv6:
    
    for gglPrefix in prefixesGglIPv6:
        if(cgtPrefix == gglPrefix):
            Myfile2.write(cgtPrefix + " - Cogent-Google \n");
            
    for lvlPrefix in prefixesLvlIPv6:
        if(cgtPrefix == lvlPrefix):
            Myfile2.write(cgtPrefix + " - Cogent-Level3 \n");
            
    for telPrefix in prefixesTelIPv6:
        if(cgtPrefix == telPrefix):
            Myfile2.write(cgtPrefix + " - Cogent-Telia \n");   
            
            
            
for gglPrefix in prefixesGglIPv6:
            
    for lvlPrefix in prefixesLvlIPv6:
        if(gglPrefix == lvlPrefix):
            Myfile2.write(gglPrefix + " - Google-Level3 \n");
            
    for telPrefix in prefixesTelIPv6:
        if(gglPrefix == telPrefix):
            Myfile2.write(gglPrefix + " - Google-Telia \n"); 
            
        
for lvlPrefix in prefixesLvlIPv6:
                
    for telPrefix in prefixesTelIPv6:
        if(lvlPrefix == telPrefix):
            Myfile2.write(lvlPrefix + " - Level3-Telia \n"); 
          
Myfile2.close();


print("========== Finished for IPv6 ==========")

"""
print(prefixesCgtIPv4);
print(prefixesGglIPv4);
print(prefixesLvlIPv4);
print(prefixesTelIPv4);
"""
print(prefixesCgtIPv6);
print(prefixesGglIPv6);
print(prefixesLvlIPv6);
print(prefixesTelIPv6);