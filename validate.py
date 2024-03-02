class myvalidate:
    def required(self, myform):
        for entry in myform:
            if entry == "":
                return False
        return True
