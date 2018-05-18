import pymongo

class IP_Count(object):
    dic = {}
    show_dic = {}
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['cixi_proxy']
        self.collection = self.db.ProxyItem

    def __del__(self):
        self.client.close()
        print('database closed')

    def count(self):
        cursor = self.collection.aggregate(
            [
                {"$group": {"_id": "$port", "count": {"$sum": 1}}}
            ]
        )
        for doc in cursor:
            self.dic[doc['_id'][0]]=int(doc['count'])

        list = sorted(self.dic.items(), key=lambda x: x[1], reverse=True)
        count = 0
        for i in list:
            if i[1] > 1:
                self.show_dic[i[0]] = i[1]
            else:
                count += 1
        self.show_dic['其他'] = count

        print(self.show_dic.keys())
        print(self.show_dic.values())


ct = IP_Count()
ct.count()