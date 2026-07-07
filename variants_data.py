# Genere automatiquement par compare_variants.py
# Convergence de trois variantes de CFR, en fonction du nombre
# de noeuds de jeu visites (cout de calcul).
NODE_BUDGET = 22000000
VARIANTS = {
 "CFR classique (moyenne)": [
  {
   "nodes": 28353,
   "exploitability": 0.9719700385708961
  },
  {
   "nodes": 37804,
   "exploitability": 0.7823498157515038
  },
  {
   "nodes": 47255,
   "exploitability": 0.6056967331578215
  },
  {
   "nodes": 66157,
   "exploitability": 0.45425459917463207
  },
  {
   "nodes": 85059,
   "exploitability": 0.3873968783663473
  },
  {
   "nodes": 113412,
   "exploitability": 0.2787599921827491
  },
  {
   "nodes": 141765,
   "exploitability": 0.2323995430828031
  },
  {
   "nodes": 179569,
   "exploitability": 0.19415489114682294
  },
  {
   "nodes": 236275,
   "exploitability": 0.17651901157954977
  },
  {
   "nodes": 311883,
   "exploitability": 0.12334152322344948
  },
  {
   "nodes": 406393,
   "exploitability": 0.10578123390805244
  },
  {
   "nodes": 529256,
   "exploitability": 0.09129376914641825
  },
  {
   "nodes": 689923,
   "exploitability": 0.07167491143134426
  },
  {
   "nodes": 897845,
   "exploitability": 0.06847004722210873
  },
  {
   "nodes": 1162473,
   "exploitability": 0.04666509202913137
  },
  {
   "nodes": 1521611,
   "exploitability": 0.045596433051179025
  },
  {
   "nodes": 1984710,
   "exploitability": 0.036332406261041644
  },
  {
   "nodes": 2599025,
   "exploitability": 0.031284851686458254
  },
  {
   "nodes": 3392909,
   "exploitability": 0.026583267409302606
  },
  {
   "nodes": 4423068,
   "exploitability": 0.023291037461397837
  },
  {
   "nodes": 5784012,
   "exploitability": 0.022790151190899912
  },
  {
   "nodes": 7551349,
   "exploitability": 0.018872962102754312
  },
  {
   "nodes": 9866844,
   "exploitability": 0.015844234053279123
  },
  {
   "nodes": 12891164,
   "exploitability": 0.01337481640389579
  },
  {
   "nodes": 16841682,
   "exploitability": 0.01219411392396471
  },
  {
   "nodes": 22001928,
   "exploitability": 0.010347829687171989
  }
 ],
 "CFR+ (strategie courante)": [
  {
   "nodes": 28353,
   "exploitability": 2.6160316154080836
  },
  {
   "nodes": 37804,
   "exploitability": 3.065144860984272
  },
  {
   "nodes": 47255,
   "exploitability": 2.159854403675773
  },
  {
   "nodes": 66157,
   "exploitability": 1.4748933778972217
  },
  {
   "nodes": 85059,
   "exploitability": 1.97557226259643
  },
  {
   "nodes": 113412,
   "exploitability": 1.0398774037184282
  },
  {
   "nodes": 141765,
   "exploitability": 0.6056774589905931
  },
  {
   "nodes": 179569,
   "exploitability": 0.35503958887095133
  },
  {
   "nodes": 236275,
   "exploitability": 0.25997262811732713
  },
  {
   "nodes": 311883,
   "exploitability": 0.1980878836292449
  },
  {
   "nodes": 406393,
   "exploitability": 0.2787235079273993
  },
  {
   "nodes": 529256,
   "exploitability": 0.18736497564804078
  },
  {
   "nodes": 689923,
   "exploitability": 0.13445532237848914
  },
  {
   "nodes": 897845,
   "exploitability": 0.14354236408208387
  },
  {
   "nodes": 1162473,
   "exploitability": 0.08923536142639435
  },
  {
   "nodes": 1521611,
   "exploitability": 0.04960365903141899
  },
  {
   "nodes": 1984710,
   "exploitability": 0.04058902547683322
  },
  {
   "nodes": 2599025,
   "exploitability": 0.03513041024350625
  },
  {
   "nodes": 3392909,
   "exploitability": 0.02499387130119462
  },
  {
   "nodes": 4423068,
   "exploitability": 0.04110136747795889
  },
  {
   "nodes": 5784012,
   "exploitability": 0.016631960967091484
  },
  {
   "nodes": 7551349,
   "exploitability": 0.012642864066661486
  },
  {
   "nodes": 9866844,
   "exploitability": 0.011419354711733817
  },
  {
   "nodes": 12891164,
   "exploitability": 0.008916022409576181
  },
  {
   "nodes": 16841682,
   "exploitability": 0.007484419574782283
  },
  {
   "nodes": 22001928,
   "exploitability": 0.007251693884455276
  }
 ],
 "CFR+ (moyenne)": [
  {
   "nodes": 28353,
   "exploitability": 1.9898147396031622
  },
  {
   "nodes": 37804,
   "exploitability": 1.9322293674931723
  },
  {
   "nodes": 47255,
   "exploitability": 1.5255395839800125
  },
  {
   "nodes": 66157,
   "exploitability": 1.167287563322069
  },
  {
   "nodes": 85059,
   "exploitability": 0.8959323802301256
  },
  {
   "nodes": 113412,
   "exploitability": 0.8490701211854552
  },
  {
   "nodes": 141765,
   "exploitability": 0.6827900420128361
  },
  {
   "nodes": 179569,
   "exploitability": 0.5389138210962705
  },
  {
   "nodes": 236275,
   "exploitability": 0.3601188948587916
  },
  {
   "nodes": 311883,
   "exploitability": 0.267920181426894
  },
  {
   "nodes": 406393,
   "exploitability": 0.22190092998616856
  },
  {
   "nodes": 529256,
   "exploitability": 0.18786765190021343
  },
  {
   "nodes": 689923,
   "exploitability": 0.1655521729632867
  },
  {
   "nodes": 897845,
   "exploitability": 0.1467748838580148
  },
  {
   "nodes": 1162473,
   "exploitability": 0.13737896628935095
  },
  {
   "nodes": 1521611,
   "exploitability": 0.12737126526319145
  },
  {
   "nodes": 1984710,
   "exploitability": 0.11546795851883492
  },
  {
   "nodes": 2599025,
   "exploitability": 0.10550580293214265
  },
  {
   "nodes": 3392909,
   "exploitability": 0.09696438105855704
  },
  {
   "nodes": 4423068,
   "exploitability": 0.08793496089581973
  },
  {
   "nodes": 5784012,
   "exploitability": 0.07942632654401702
  },
  {
   "nodes": 7551349,
   "exploitability": 0.07286000354584547
  },
  {
   "nodes": 9866844,
   "exploitability": 0.06515731841780545
  },
  {
   "nodes": 12891164,
   "exploitability": 0.05876304301884344
  },
  {
   "nodes": 16841682,
   "exploitability": 0.05350706662761759
  },
  {
   "nodes": 22001928,
   "exploitability": 0.049101956412011566
  }
 ],
 "MCCFR (moyenne)": [
  {
   "nodes": 27532,
   "exploitability": 0.9749119766313197
  },
  {
   "nodes": 35930,
   "exploitability": 0.7993102442354663
  },
  {
   "nodes": 46959,
   "exploitability": 0.7246373288156378
  },
  {
   "nodes": 61337,
   "exploitability": 0.6133983784138158
  },
  {
   "nodes": 80176,
   "exploitability": 0.4817083045792777
  },
  {
   "nodes": 104739,
   "exploitability": 0.39703185345161995
  },
  {
   "nodes": 136818,
   "exploitability": 0.34246991829026974
  },
  {
   "nodes": 178745,
   "exploitability": 0.2776553046270621
  },
  {
   "nodes": 233541,
   "exploitability": 0.26322345621911486
  },
  {
   "nodes": 305132,
   "exploitability": 0.1880363522910463
  },
  {
   "nodes": 398664,
   "exploitability": 0.1693369398607844
  },
  {
   "nodes": 520855,
   "exploitability": 0.13089414696502674
  },
  {
   "nodes": 680507,
   "exploitability": 0.11772196500668626
  },
  {
   "nodes": 889111,
   "exploitability": 0.10445746209871411
  },
  {
   "nodes": 1161654,
   "exploitability": 0.08684598715866104
  },
  {
   "nodes": 1517717,
   "exploitability": 0.06482123736524306
  },
  {
   "nodes": 1982985,
   "exploitability": 0.05960336814223083
  },
  {
   "nodes": 2590839,
   "exploitability": 0.04701884986176073
  },
  {
   "nodes": 3385016,
   "exploitability": 0.044625492421160894
  },
  {
   "nodes": 4422641,
   "exploitability": 0.040274795126925424
  },
  {
   "nodes": 5778382,
   "exploitability": 0.03161490617597825
  },
  {
   "nodes": 7549701,
   "exploitability": 0.03047716539085702
  },
  {
   "nodes": 9864012,
   "exploitability": 0.02713211068351248
  },
  {
   "nodes": 12887709,
   "exploitability": 0.025267099652845855
  },
  {
   "nodes": 16838338,
   "exploitability": 0.02108768394312989
  },
  {
   "nodes": 22000009,
   "exploitability": 0.0178272633437283
  }
 ]
}
