l = [{"rate":6,"nom":"bidule"},{"rate":5,"nom":"machin"},{"rate":7,"nom":"truc"}]
l2 = sorted(l,key=lambda x:x["rate"])
print(l2)