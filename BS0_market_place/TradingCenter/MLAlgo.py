import TradingCenter.models as m

class BuildRelations:
    def __init__(self,rel_dist):
        self.rel = rel_dist
        self.process_data()
    def process_data(self):
        m.inventory_relations.objects.all().delete()
        m.software_relations.objects.all().delete()
        m.service_relations.objects.all().delete()
        self.make_inventory_rel()
        self.make_services_rel()
        self.make_software_rel()
    def remove_junk(self,st:str):
        st = st.replace(",","").replace("!","").replace('.',"").replace("?","").replace("is", "").replace("am","").replace("i","").replace("are", "").replace("was","").replace("were","").replace("the", "").replace("this","").replace("their","").replace("where","").replace("what", "").replace("how","").replace("\n"," ").split(" ")
        return st
    def make_software_rel(self):
        inv_lis = m.software_manager.objects.all()
        for first in range(len(inv_lis)-1):
            st = ""
            for first_fea in m.software_featurers.objects.filter(manager_id = inv_lis[first]):
                st += first_fea.description+" "
            st += inv_lis[first].description+" "
            st += inv_lis[first].long_description+" "
            first_lis = self.remove_junk(st)
            for second in range(first,len(inv_lis)):
                st = ""
                for second_fea in m.software_featurers.objects.filter(manager_id = inv_lis[second]):
                    st += second_fea.description+" "
                st += inv_lis[second].description+" "
                st += inv_lis[second].long_description+" "
                second_lis = self.remove_junk(st)

                if(self.rel <= self.relation_value(first_lis,second_lis)):
                    m.software_relations.objects.create(first = inv_lis[first],second = inv_lis[second])

    def make_inventory_rel(self):
        inv_lis = m.inventory_managment.objects.all()
        for first in range(len(inv_lis)-1):
                st = ""
                for first_fea in m.inventory_items_featurers.objects.filter(manager_id = inv_lis[first]):
                    st += first_fea.description+" "
                st += inv_lis[first].description+" "
                st += inv_lis[first].long_description+" "
                first_lis = self.remove_junk(st)
                for second in range(first,len(inv_lis)):
                    st = ""
                    for second_fea in m.inventory_items_featurers.objects.filter(manager_id = inv_lis[second]):
                        st += second_fea.description+" "
                st += inv_lis[second].description+" "
                st += inv_lis[second].long_description+" "
                second_lis = self.remove_junk(st)
                
                if(self.rel <= self.relation_value(first_lis,second_lis)):
                    m.inventory_relations.objects.create(first = inv_lis[first],second = inv_lis[second])

    def make_services_rel(self):
        inv_lis = m.services_manager.objects.all()
        for first in range(len(inv_lis)-1):
            st = ""
            for first_fea in m.service_featurers.objects.filter(manager_id = inv_lis[first]):
                    st += first_fea.description+" "
            st += inv_lis[first].description+" "
            st += inv_lis[first].long_description+" "
            first_lis = self.remove_junk(st)

            for second in range(first,len(inv_lis)):
                st = ""
                for second_fea in m.service_featurers.objects.filter(manager_id = inv_lis[second]):
                    st += second_fea.description+" "
                st += inv_lis[second].description+" "
                st += inv_lis[second].long_description+" "
                second_lis = self.remove_junk(st)
            if(self.rel <= self.relation_value(first_lis,second_lis)):
                    m.service_relations.objects.create(first = inv_lis[first],second = inv_lis[second])



    def relation_value(self,first,second):
        first_val = 0
        second_val = 0
        for f in set(first):
            first_val += second.count(f)
        if first_val != 0:
            first_val = (first_val/len(second))*100
        for s in set(second):
            second_val += first.count(s)
        if second_val != 0:
            second_val = (second_val/len(first))*100
        return (first_val+second_val)/2