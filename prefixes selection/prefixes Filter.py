# -*- coding: utf-8 -*-
"""
Routes selector that select routes that occurs several times in the announced prefixes 
by the selected operators.
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


operators = [prefixesCgtIPv4,prefixesCgtIPv6,prefixesGglIPv4,prefixesGglIPv6,prefixesLvlIPv4,prefixesLvlIPv6,prefixesTelIPv4,prefixesTelIPv6];
             
             

prefixes = set();
doublePrefixes = set();

for operator in operators:
    for pf in operator:
        prefixe = pf.replace(" ","");
        if prefixe not in prefixes:
            prefixes.add(prefixe);
        else:
            doublePrefixes.add(prefixe);
        
result = open("Double prefixes.txt",'w');
for doublePrefixe in doublePrefixes:
    result.write(doublePrefixe + "\n");
    print(doublePrefixe);
    
result.close();