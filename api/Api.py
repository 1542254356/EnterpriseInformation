import re

class Api:
    def getLocation(self,companyName):
        pass

    def same_company(self,a, b):
        if a == b:
            return True

        a = a.replace('股份有限公司', '公司')
        b = b.replace('股份有限公司', '公司')

        a = a.replace('有限公司', '公司')
        b = b.replace('有限公司', '公司')

        a = a.replace('股份公司', '公司')
        b = b.replace('股份公司', '公司')

        a = re.sub(u"\\(.*?\\)", "", a)
        b = re.sub(u"\\(.*?\\)", "", b)

        # if a.find(b) != -1 or b.find(a) != -1:
        #     return True

        if a == b:
            return True

        return False