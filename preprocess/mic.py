# -*- coding: utf-8 -*-
            #感觉下面没有必要啊...
            rows = csv.reader(open("../data/user/"+uid+".csv","rb"))
            rows.next()           
            for row in rows:
                if row[0] == "2014-"+trDay and row[1] == key[1] and row[2] == "3":
                    result[key] = 1
                    break