#import openpyxl
import fileinput
import time
import sys
import operator
import math

import requests
import json


from neo4j import GraphDatabase, basic_auth


#url = "bolt://175.121.89.176:8685"
url = "bolt://1.233.215.39:7687"
#url = "bolt://1.233.215.39:8687"

driver = GraphDatabase.driver(url,auth=basic_auth("kms0845","neo4j"))


class Nodes_Noe4j:
    def __init__(self, type=""):
        self.type = type
        self.nodes = {}
        #self.nodes = self.all_nodes()
        self.cnt = 1
        self.data = {}
        self.open_query_filter_cnt = 521817

        self.read_nodes_lables = ["Chemival", "Disease", "Gene", "Species", "Pro"]
        self.lable_web_dictionary = {"Query": 1, "Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6, "CellLine": 7,
                            "Hallmark": 8, "Pro" : 5, "Pro_Sub" : 5}
        self.lable_reverse_dictionary = {1: "Chemical", 2: "Disease", 3: "Mutation", 4: "Gene", 5: "Species", 6: "CellLine",
                                    7: "Hallmark", 8: "Pro"}
        self.lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
                            "Hallmark": 7, "Pro" : 8}
        # web layout
        self.m = [20, 140, 20, 100]
        self.w = 948 - self.m[1] - self.m[3]
        self.h = 600 - self.m[0] - self.m[2]
        self.center_x = self.w / 2 + self.m[1]
        self.center_y = self.h / 2 + self.m[0]
    def load_all_nodes(self):
        start_time = time.time()
        self.nodes = self.all_nodes()
        #print("all node loaded.")
        end_time = time.time()
        #print("Node Load Time: {} sec".format(end_time - start_time))
    def data_info_add(self):
        self.data['nodes'] = sorted(self.data['nodes'],key= lambda x: x['group'])

        import cx_Oracle as oci
        Oracle_url = "192.168.0.132"
        conn = oci.connect('neo4j/neo1234@192.168.0.132:1521/graph')
        #print(conn.version)
        cursor = conn.cursor()
        # self.lable_web_dictionary = {"Query": 1, "Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6,
        #                              "CellLine": 7,
        #                              "Hallmark": 8}
        for i in range(2,9):
            query_ID_temp = ""
            query_ID_temp2 = ""
            for j in self.data['nodes']:
                if(j['group'] == i) :
                    if(i == 5 and 'Gene' in j['cd']):
                        #query_ID_temp2 = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
                        query_ID_temp = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
                    query_ID_temp = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
            if(query_ID_temp == ""): continue
            if(i == 2):
                query_ID_temp = query_ID_temp.replace("NODEID","CHEMICALID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select CHEMICALID, DESCRIPTION from NEO4J_CHEMICAL_POPUP_MERGE2 where ' + query_ID_temp)
                cursor.execute('select CHEMICALID, DESCRIPTION from NEO4J_CHEMICAL_POPUP_MERGE where '+query_ID_temp)
            if (i == 3):
                query_ID_temp = query_ID_temp.replace("NODEID", "DISEASEID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select DISEASEID, DEFINITION from NEO4J_DISEASE_POPUP4 where ' + query_ID_temp)
                cursor.execute('select DISEASEID, DEFINITION from NEO4J_DISEASE_POPUP where ' + query_ID_temp)

            if (i == 5):
                query_ID_temp = query_ID_temp.replace("NODEID", "PROID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select PROID, DEFINITION from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
                cursor.execute('select PROID, DEFINITION from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
            if (i == 6):
                query_ID_temp = query_ID_temp.replace("NODEID", "SPECIESID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select SPECIESID, SPECIESPOPUP from NEO4J_SPECIES_POP_UP where ' + query_ID_temp)
                cursor.execute('select SPECIESID, SPECIESPOPUP from NEO4J_SPECIES_POP_UP where ' + query_ID_temp)
            #if(i == 5): continue
            for k in cursor.fetchall():
                for o, o_node in enumerate(self.data['nodes']):
                    if o_node['cd'] == k[0]:
                        o_node['tdesc'] = k[1]
                        self.data['nodes'][o]['tdesc'] = k[1]
                        break

        for j,j_node in enumerate(self.data['nodes']):
            if j_node['group'] == 1 :
                self.data['nodes'][j]['tdesc'] = "this is the target data"
            if 'tdesc' not in j_node:
                self.data['nodes'][j]['tdesc'] = 'Null'
                j_node['tdesc'] = 'Null'

        cursor.close()
        conn.close()
        #for i in a.data["nodes"]:

    def data_check(self):
        seach_check = False
        for cnt,i in enumerate(self.data["links"]):
            if('cnt' not in i):
                print("edge without cnt")
                print(i)
                #print(cnt)
            seach_check = False
            for j in self.data["nodes"]:
                if(j["nid"] == i["source"]):
                    seach_check = True
                    break
            if(seach_check == False):
                print("source error : ",i["source"])
            seach_check = False
            for j in self.data["nodes"]:
                if(j["nid"] == i["target"]):
                    seach_check = True
                    break
            if (seach_check == False):
                print("target error : ", i["target"])
    def conditional_start(self, arg):
        start_time = time.time()

        #a.load_all_nodes()
        #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

        #print(a.open_discovery())

        if(len(arg) >= 3) :

            if(str(arg[3]) == 'Gene'):
                query_ID_temp = str(arg[2])
                arg[2] = "GeneID:"+query_ID_temp.split(":")[1]

            if(str(arg[5]) == 'Gene'):
                query_ID_temp = str(arg[4])
                arg[4] = "GeneID:" + query_ID_temp.split(":")[1]

            if(arg[1]== str(1)):
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = int(arg[4])
                arg_end_year = int(arg[5])
                self.open_discovery_with_year(target_label_type = arg_target_domain, target_id = arg_target_id, open_query_filter_cnt = 20, start_years = arg_start_year, end_years = arg_end_year)
            elif(arg[1] == str(2)):
                arg_start_target_id = str(arg[2])
                arg_start_target_domain = str(arg[3])
                arg_end_target_id = str(arg[4])
                arg_end_target_domain = str(arg[5])
                arg_start_year = int(arg[6])
                arg_end_year = int(arg[7])
                self.close_discovery_with_year(start_target_label_type= arg_start_target_domain , start_target_id= arg_start_target_id,
                                            end_target_label_type= arg_end_target_domain , end_target_id= arg_end_target_id, start_years = arg_start_year, end_years = arg_end_year)
            elif(arg[1] == str(3)) :
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = int(arg[4])
                arg_end_year = int(arg[5])
                self.shortestpath_discovery_with_years(start_target_label_type= arg_target_domain, start_target_id= arg_target_id, start_years = arg_start_year, end_years = arg_end_year)
            elif (arg[1] == str(4)):
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = int(arg[4])
                arg_end_year = int(arg[5])
                self.neighbor_discovery_with_years(start_target_label_type=arg_target_domain,
                                                    start_target_id=arg_target_id, start_years = arg_start_year, end_years = arg_end_year)
            else:
                print("arg error  : ",arg[1])
                driver.close()
                sys.exit()
        else :
            self.open_discovery_with_year(target_label_type = "Gene", target_id = "GeneID:7157", open_query_filter_cnt = 20, start_years = 2000, end_years = 2010)


        #(target_label_type = "Gene", target_id = "PR:000003035")



        self.data_check()
        self.data_info_add()
        php_dump(self.data)
        end_time = time.time()
    def all_nodes(self):
        with driver.session() as session:
            return session.read_transaction(self.read_nodes)

    def read_nodes(self, tx):
        all_node = {}
        for record in tx.run("MATCH (A)"
                             "RETURN ID(A), A.ID, A.type"):
            if(record[2] in self.read_nodes_lables):
                all_node[record[1]] = record[0]
        return all_node

    def node_id(self, node1_name = "abc"):
        with driver.session() as session:
            return session.read_transaction(self.check_node_id, node1_name)
    @staticmethod
    def check_node_id(tx, node1_name: str = "abc"):
        temp001 = "MATCH (A {ID:\""+node1_name+"\"})\nRETURN ID(A)"
        try:
            return tx.run(temp001).single().value()
        except:
            #print("node id not found : "+node1_name)
            return -1
    def node_id_with_lable(self, node1_name: str = "abc", node1_domain: str = "Chemical"):
        if "Gene:" in node1_name:
            node1_name = "GeneID:"+node1_name.split(":")[1]
        with driver.session() as session:
            return session.read_transaction(self.check_node_id_with_lable, node1_name, node1_domain)
    @staticmethod
    def check_node_id_with_lable(tx, node1_name: str = "abc", node1_domain: str = "Chemical"):
        temp001 = "MATCH (A:"+node1_domain+" {ID:\""+node1_name+"\"})\nRETURN ID(A)"
        node = None
        try:
            for record in tx.run(temp001):
                for node in record:
                    return node
        except:
            print("node id not found : "+node1_name)
            return -1
        if(node == None):
            print("node id not found : " + node1_name)
            return -1
    def create_relationship(self, node1_name: str = "abc", node2_name: str = "abc", relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.nodes[node1_name]
        except:
            try : node1_id = self.node_id(node1_name)
            except:
                print(node1_name + " key error !")
                return
        try:
            node2_id = self.nodes[node2_name]
        except:
            try : node2_id = self.node_id(node2_name)
            except:
                print(node2_name + " key error !")
                return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_with_domain(self, node1_name: str = "MESH", node1_domain: str = "Chemical", node2_name: str = "TAXID", node2_domain: str = "Chemical",relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id_with_lable(node1_name, node1_domain)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id_with_lable(node2_name, node2_domain)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_by_id(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows", properties: dict = {}) :
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)
    @staticmethod
    def tx_relationship(tx, id1, id2, relationship_type="Genus_Species_pair",**properties):
        try:
            if(len(properties) > 0):
                temp_properties = " {"
                for key in properties.keys():
                    contents = str(key)
                    if(contents) == "TYPE":
                        continue
                    contents = contents.replace("'", "\'")
                    contents = contents.replace(",", "\,")
                    if(isinstance(properties[key],str)):
                        temp_properties = temp_properties + key + " : \"" + str(properties[key]) + "\", "
                    else:
                        temp_properties = temp_properties + key + " : " + str(properties[key]) + ", "

                temp_properties = temp_properties[:-2] + "}"
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1)+ " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + temp_properties + "]->(b)\n"
            else :
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1) + " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + "]->(b)\n"

            #print(temp)
            tx.run(temp)
            return

        except:
            print(id1 + " or " + id2 + " search failed")
            return

    def create_relationship_with_domain_with_direction(self, node1_name: str = "MESH", node1_domain: str = "Chemical", node2_name: str = "TAXID", node2_domain: str = "Chemical",relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id_with_lable(node1_name, node1_domain)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id_with_lable(node2_name, node2_domain)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship_with_direction, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_by_id_with_direction(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows", properties: dict = {}) :
        #only directed relationship is supported in neo4j currently.
        with driver.session() as session:
            session.read_transaction(self.tx_relationship_with_direction, node1_id, node2_id, relationship_type, **properties)
    def tx_relationship_with_direction(self, tx, id1, id2, relationship_type="Genus_Species_pair",**properties):
        try:
            if(len(properties) > 0):
                temp_properties = " {"
                for key in properties.keys():
                    contents = str(key)
                    if(contents) == "TYPE":
                        continue
                    contents = contents.replace("'", "\'")
                    contents = contents.replace(",", "\,")
                    temp_properties = temp_properties + key + " : " + str(properties[key]) + ", "
                temp_properties = temp_properties[:-2] + "}"
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1)+ " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + temp_properties + "]->(b)\n"
            else :
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1) + " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + "]->(b)\n"

            #print(temp)
            tx.run(temp)
            return

        except:
            print(id1 + " or " + id2 + " search failed")
            return

    def add_nodes(self, label_type, **properties):
        with driver.session() as session:
            self.nodes[properties['ID']] =  session.write_transaction(self.tx_nodes, label_type, **properties)
            return
    @staticmethod
    def tx_nodes(tx, label_type, **properties):
        try:

            temp = "CREATE(a:" + label_type+ " {"
            for key in properties.keys():
                contents = str(key)
                contents = contents.replace("'", "\'")
                contents = contents.replace(",", "\,")
                temp = temp + key + " : {" + contents + "}, "
            temp = temp[:-2] +"}) \n"+ "RETURN ID(a)"
            #print (temp)
            return tx.run(temp, **properties).single().value()


            # contents = ""
            # for key in properties.keys():
            #     contents = str(properties[key])
            #     contents = contents.replace("'", "\'")
            #     contents = contents.replace(",", "\,")
            #     temp = temp + key + " : '" + contents + "', "
            # temp = temp[:-2]+"})\n"
            # temp = temp +"RETURN ID(a)"
            #print(temp)


        except Exception as ex:
            print(properties['ID'] + ' : ' + label_type + " node add error")
            return -1


    def open_discovery(self, target_label_type = "Gene", target_id = "PR:000003035") :
        result = {}
        result2 = {}
        sorted_cnt = {}
        visit = []
        temp3 = 0
        with driver.session() as session:
            result = session.read_transaction(self.open_discovery_tx, target_label_type, target_id, self.open_query_filter_cnt)
            result2 = session.read_transaction(self.open_discovery_tx2, target_label_type, target_id)

            visit2 = False
            for i,i_id in enumerate(result.keys()):
                print(i)
                visit2 = False
                for j, j_id in enumerate(result2.values()):
                    temp3 = self.check_relationships_by_id(i_id, j_id)
                    if(temp3 > 0) : visit2 = True
                    break
                if(visit2 == True): visit.append(False)
                else : visit.append(True)
            for i,i_id in enumerate(result.keys()):
                cnt = 0
                if(visit[i] == False) :
                    result[i_id] = cnt
                    continue
                for j,j_id in enumerate(result2.values()):
                    if(j == 0): continue # j = 0 : start node
                    temp3 = self.check_relationships_by_id(i_id,j_id)
                    #print(temp3)
                    if(temp3 > 0) : cnt += 1
                result[i_id] = cnt

        print("MATCH(n)")
        print("WHERE ID(n) IN[")
        print(result2.values())
        print("]\nRETURN n")
        print("sorted results : ")
        sorted_cnt = sorted(result.items(),key=operator.itemgetter(1), reverse= True)
        for i, n in enumerate(sorted_cnt):
            if(i == 10): break
            print(str(n[0]),end=",")


        return 1
    @staticmethod
    def open_discovery_tx(tx, target_label_type="Gene", target_id="PR:000003035", query_filter_cnt = 0):
        result_nodes = {}
        #run_text = "Match (Gene00001: "+target_label_type+" {ID: \""+target_id+ "\" })-[s]-(Gene_web)-[r]-(n)\n"+"where toInteger(split(Gene_web.count, \";\")[-1]) > 521817\n"+"return ID(Gene_web)"


        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        run_text = run_text + "Order by toInteger(split(General_Node_web.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "Match (General_Node_web)-[r]-(n)\n"
        run_text = run_text + "where toInteger(split(n.count, \";\")[-1]) > "+str(query_filter_cnt)+" and (General_Node00001) <> (n) and not (General_Node00001)--(n)\n"
        run_text = run_text + "return distinct ID(n)"
        print(run_text)
        print("number of second layers : ")

        for record in tx.run(run_text):
            result_nodes[record[0]] = 1
        print(len(result_nodes))
        return result_nodes
    @staticmethod
    def open_discovery_tx2(tx, target_label_type="Gene", target_id="PR:000003035"):
        result_nodes = {}

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        run_text = run_text + "Order by toInteger(split(General_Node_web.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "with General_Node00001 + collect(General_Node_web) as temp_results\n"
        run_text = run_text + "unwind temp_results as out_results\n"
        run_text = run_text + "return id(out_results),out_results.ID"
        #run_text = run_text + "LIMIT 10"
        #apoc.node.degree(n,\"\")
        print(run_text)
        for record in tx.run(run_text):
            print(str(record[0]) + "<->" + str(record[1]))
            #print(record[1] + " count = " + str(result_counts[record[1]]))
            result_nodes[record[1]] = record[0]

        # sorted_cnt = sorted(result_nodes.items(),key=operator.itemgetter(1), reverse= True)
        # for i, n in enumerate(sorted_cnt):
        #     if(i == 10): break
        #     print(str(n[0]),end=",")
        return result_nodes

    def open_discovery_with_year(self, target_label_type = "Gene", target_id = "GeneID:7157", open_query_filter_cnt = 20, start_years = 2000, end_years = 2010) :
        result = {}
        result2 = {}
        sorted_cnt = {}
        visit = []
        temp3 = 0
        with driver.session() as session:
            result = session.read_transaction(self.open_discovery_tx_with_year, target_label_type, target_id, open_query_filter_cnt, start_years, end_years)

        for i in self.data['nodes']:
            if(i["cd"] == target_id):
                i["group"] = 1 # Query : 1
        return 1
    def open_discovery_tx_with_year(self, tx, target_label_type="Gene", target_id="GeneID:7157", query_filter_cnt = 0, start_years = 2000, end_years = 2010):

        result_nodes = {}
        #run_text = "Match (Gene00001: "+target_label_type+" {ID: \""+target_id+ "\" })-[s]-(Gene_web)-[r]-(n)\n"+"where toInteger(split(Gene_web.count, \";\")[-1]) > 521817\n"+"return ID(Gene_web)"

        #MATCH (General_Node00001: Gene {ID: "GeneID:7157"})-[s] - (General_Node_web)
        #WHERE exists(s.cnt_2009) or exists(s.cnt_2008) or exists(s.cnt_2007) or exists(s.cnt_2006) or exists(s.cnt_2005) or exists(s.cnt_2004) or exists(s.cnt_2003) or exists(s.cnt_2002) or exists(s.cnt_2001) or exists(s.cnt_2000)
        #WITH s, coalesce(s.cnt_2009,0) + coalesce(s.cnt_2008, 0) +  coalesce(s.cnt_2007, 0) +  coalesce(s.cnt_2006, 0) +  coalesce(s.cnt_2005, 0) +  coalesce(s.cnt_2004, 0) +  coalesce(s.cnt_2003, 0) +  coalesce(s.cnt_2002, 0) +  coalesce(s.cnt_2001, 0) +  coalesce(s.cnt_2000, 0) as cnt
        #order by cnt desc
        #return s,cnt
        #limit 10

        cnt_text = ""
        coalesce_text = ""
        cnt_property_text = ""
        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH General_Node00001, General_Node_web, s, "
        for i in range(start_years, end_years) :
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(s."+cnt_property_text+") or "
            coalesce_text = coalesce_text + "coalesce(s."+cnt_property_text+", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return s, cnt, General_Node00001, General_Node_web \n"
        run_text = run_text + "limit 100"
        #print(run_text)
        nodes = []
        links_temp = []
        for edge in tx.run(run_text):
            edges = edge[0]
            total_edge_cnt = edge[1]
            start_node = edge[2]
            end_node = edge[3]

            links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                               "cnt": total_edge_cnt, "group": 1})
            nodes.append({"nid":str(start_node.id),"cd":start_node._properties['ID'],"nm": start_node._properties['text'],"group":self.lable_web_dictionary[start_node._properties['type']]})
            nodes.append({"nid": str(end_node.id), "cd": end_node._properties['ID'],
                          "nm": end_node._properties['text'],
                          "group": self.lable_web_dictionary[end_node._properties['type']]})
        # print(links)
        links = []

        General_Node00001 = start_node
        #for starting point of open query

        sorted_links = sorted(links_temp, key=lambda k: k['cnt'], reverse=True)

        sorted_nodes = []
        for i in range(0, 20):
            links.append({'source' : sorted_links[i]['source'],'target' : sorted_links[i]['target'], 'cnt': sorted_links[i]['cnt'], 'group' : sorted_links[i]['group']})
            sorted_nodes.append(sorted_links[i]['source'])
            sorted_nodes.append(sorted_links[i]['target'])

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)

        final_nodes = []
        for i in ex_nodes:

            for j in nodes:
                if (j['nid'] == i):
                    final_nodes.append(j)
                    break



        first_layer_len = len(final_nodes)
        arcradius = 100
        circleradius = 10
        n = first_layer_len
        m = [20, 140, 20, 100]
        w = 948 - m[1] - m[3]
        h = 600 - m[0] - m[2]
        center_x = w / 2 + m[1]
        center_y = h / 2 + m[0]

        for i in range(0,first_layer_len):
            if(final_nodes[i]['cd'] == target_id):
                final_nodes[i]['fix_x'] = center_x
                final_nodes[i]['fix_y'] = center_y
            else:
                ang = (math.pi * 2 * i) / (first_layer_len-1)
                circle_x = arcradius * math.sin(ang) + center_x
                circle_y = arcradius * math.cos(ang) + center_y
                final_nodes[i]['fix_x'] = circle_x
                final_nodes[i]['fix_y'] = circle_y


        self.data['nodes'] = final_nodes
        self.data['links'] = links

        #MATCH (SSS)
        #Where ID(SSS) = 12359409
        #With SSS
        #Match (a)
        #Where ID(a) = 12359409 Or ID(a) = 132876 Or ID(a) = 144511 Or ID(a) = 142261 Or ID(a) = 126034 Or ID(a) = 144942 Or ID(a) = 125798 Or ID(a) = 144570 Or ID(a) = 131423 Or ID(a) = 143620 Or ID(a) = 136735 Or ID(a) = 143082 Or ID(a) = 125821 Or ID(a) = 205145 Or ID(a) = 129790 Or ID(a) = 79141798 Or ID(a) = 79133404 Or ID(a) = 79133405 Or ID(a) = 126000 Or ID(a) = 133595 Or ID(a) = 145655 With SSS, a
        #Match (a)-[r]-(b)
        #Where not (SSS)--(b)
        #return ID(b),count(*)
        #order by count(*) Desc
        #limit 100



        run_text = ""
        run_text = run_text + "MATCH (SSS)"+"\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "

        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        run_text = run_text + "Where not (SSS)--(b)\n"
        run_text = run_text + "with a,r,b\n"
        run_text = run_text + "return ID(b),count(*)\n"
        run_text = run_text + "order by count(*) Desc\n"
        run_text = run_text + "limit 10\n"


        #print("number of second layers : ")


        #-----------------------------------------------------------------------------------------------------------
        #second layer part
        # print(links)
        temp_links = []
        first_second_edges = []
        second_layer_nodes = []
        second_layer_cnt = 0
        for record in tx.run(run_text):
            second_layer_nodes.append(record[0])
            second_layer_cnt = record[1]


        run_text = ""
        run_text = run_text + "MATCH (SSS)" + "\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (b)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in second_layer_nodes:
            nodes_text = nodes_text + "ID(b) = " + str(i) + " Or "
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text +"\n"
        run_text = run_text + "With a, b\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH a, r, b, "
        for i in range(start_years, end_years) :
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(r." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(r." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return r, b, cnt \n"
        run_text = run_text + "limit 100"

        links_temp = []



        for edge in tx.run(run_text):
            edges = edge[0]
            end_node = edge[1]
            total_edge_cnt = edge[2]
            #a.data['links'].append({"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt": total_edge_cnt, "group": 1})
            self.data['links'].append(
                {"source": str(edges.start_node.id), "target": str(edges.end_node.id),'cnt': total_edge_cnt , "group": 2})
            self.data['nodes'].append(
                {"nid": str(end_node.id), "cd": end_node._properties['ID'], "nm": end_node._properties['text'],
                 "group": self.lable_web_dictionary[end_node._properties['type']]})
        nodes = []
        nodes = self.data['nodes']
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple([d["nid"]])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #
        self.data['nodes'].clear()

        second_layer_len = len(ex_nodes)-first_layer_len

        circleradius = 10

        ang_cnt = 0
        for i in ex_nodes:
            if('fix_x' in i and 'fix_y' in i):
                self.data['nodes'].append(i)
                continue
            ang_cnt = ang_cnt + 1
            ang = (math.pi * 2 * ang_cnt) / second_layer_len
            circle_x = (arcradius + 100) * math.sin(ang) + center_x
            circle_y = (arcradius + 100) * math.cos(ang) + center_y
            i['fix_x'] = circle_x
            i['fix_y'] = circle_y
            self.data['nodes'].append(i)


        return result_nodes

    def check_relationships(self, node1_name: str = "abc", node2_name: str = "abc", relationship_type: str = "Null01234"):
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id(node1_name)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id(node2_name)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship, node1_id, node2_id)
    def check_relationships_by_id(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows"):
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship, node1_id, node2_id, relationship_type)

    @staticmethod
    def tx_check_relationship(tx, id1, id2, relationship_type="Null01234"):
        if(relationship_type == "Null01234"): temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN id(r)\n"
        else : temp0002 = "MATCH (a)-[r:"+str(relationship_type)+"]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN id(r)\n"
        try:
            return tx.run(temp0002).single().value()
        except AttributeError:
            return -1
        else :
            print("예상치 못한 에러 발생_Relationship_Check")
            return -2

    def check_relationships_by_id_with_properties(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows"):
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship_with_properties, node1_id, node2_id, relationship_type)

    def tx_check_relationship_with_properties(self, tx, id1, id2, relationship_type="Null01234"):
        if(relationship_type == "Null01234"): temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN r\n"
        else : temp0002 = "MATCH (a)-[r:"+str(relationship_type)+"]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN r\n"
        try:
            temp = tx.run(temp0002)
            if(temp.session == None) : return -1
            else: return temp
        except AttributeError:
            return -1
        else :
            print("예상치 못한 에러 발생_Relationship_Check")
            return -2

    def update_relationships_cnt_by_id(self, node1_id: int = 0, node2_id = 0, relationship_id: int = 0):
        with driver.session() as session:
            session.read_transaction(self.tx_update_relationship_cnt, node1_id, node2_id, relationship_id)

    @staticmethod
    def tx_update_relationship_cnt(tx,node1_id=0,node2_id=0, Rel_id1=0):
        temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE id(a) = "+str(node1_id)+" AND id(b) = "+str(node2_id)+" and id(r) = {Rel_ID1}\n" + "SET r.cnt=r.cnt+1\n"
        try:
            tx.run(temp0002, Rel_ID1=Rel_id1)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else :
            print("예상치 못한 에러 발생_Relationship_Check")

    def update_relationships_cnt_by_id_with_year(self, node1_id: int = 0, node2_id = 0, relationship_id: int = 0, relationship_type="Null01234", year = 0, temp_year_cnt = 1):
        with driver.session() as session:
            session.read_transaction(self.tx_update_relationship_cnt_with_year, node1_id, node2_id, relationship_id, relationship_type, year, temp_year_cnt)


    @staticmethod
    def tx_update_relationship_cnt_with_year(tx,node1_id=0,node2_id=0, Rel_id1=0, relationship_type="Null01234", year = 0, temp_year_cnt = 1):
        # Match(n) - [r] - (m)
        # where
        # id(n) = 132426 and Id(m) = 144989 and id(r) = 551305
        # MERGE(n) - [rel: cnt_merged_cooccurnce_test]->(m)
        #   ON MATCH SET
        # rel += {cnt_2000: 1111, cnt_2002: 0}
        temp0002 = "MATCH (a)-[r:"+relationship_type+"]-(b)\n"
        temp0002 = temp0002 + "WHERE id(a) = "+str(node1_id)+" AND id(b) = "+str(node2_id)+" and id(r) = "+ str(Rel_id1) + "\n"
        temp0002 = temp0002 + "MERGE (a)-[rel:"+relationship_type+"]->(b)\n"
        temp0002 = temp0002 + "  ON MATCH SET rel += {"+"cnt_"+str(year)+":"+str(temp_year_cnt)+"}\n"
        try:
            tx.run(temp0002)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else :
            print("예상치 못한 에러 발생_Relationship_Check")


    #node1_id, node2_id, relationship_type, **properties
    def merge_relationships_cnt_by_id_with_year(self, node1_id: int = 0, node2_id=0, relationship_type: str = "cooccurnce", properties : dict = {}):
        with driver.session() as session:
            session.read_transaction(self.tx_merge_relationships_cnt_by_id_with_year, node1_id, node2_id, relationship_type,
                                     properties)
    def tx_merge_relationships_cnt_by_id_with_year(self, tx, node1_id: int = 0, node2_id=0, relationship_type: str = "cooccurnce", properties : dict = {}):

        temp3 = self.check_relationships_by_id_with_properties(node1_id,node2_id,"Disease_Tree")

        if (temp3 == -1 and temp3 == -2):
            #create edge
            temp0002 = "MATCH (a)-[r:" + relationship_type + "]-(b)\n"
        else:
            #empty relationship

            # copy cnt
            # for j in temp3._properties:
            #     i._properties += j

            temp0002 = "MATCH (a)-[r:" + relationship_type + "]-(b)\n"
            temp0002 = temp0002 + "WHERE id(a) = " + str(node1_id) + " AND id(b) = " + str(
                node2_id) + " and id(r) = " + str(Rel_id1) + "\n"
            temp0002 = temp0002 + "MERGE (a)-[rel:" + relationship_type + "]->(b)\n"
            temp0002 = temp0002 + "  ON MATCH SET rel += {" + "cnt_" + str(year) + ":" + str(temp_year_cnt) + "}\n"
        try:
            tx.run(temp0002)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else:
            print("예상치 못한 에러 발생_Relationship_Check")

    def close_discovery(self, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035"):

        #just formatting for close discovery

        search_start_temp = self.node_id(start_target_id)
        search_end_temp = self.node_id(end_target_id)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.close_discovery_tx, start_target_label_type, start_target_id, end_target_label_type, end_target_id)

        print("\n")
        print("MATCH (n)")
        print("WHERE id(n) IN [",end='')
        for i in result:
            print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        print(str(search_start_temp)+","+str(search_end_temp)+"]")
        print("Return n")
        return result

    def close_discovery_tx(self, tx, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035",):
        result_nodes = {}
        #with size((c)--()) as N, ID(c) as M
        #return M,N ORDER BY N DESC LIMIT 10

        # run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        # run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        # run_text = run_text + "Order by toInteger(split(c.count, \";\")[-1]) desc limit 10 \n"
        run_text = ""
        run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "with distinct c\n"
        run_text = run_text + "Order by toInteger(split(c.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "return id(c)"
        print(run_text)
        for record in tx.run(run_text):
            result_nodes[record[0]] = 1
        return result_nodes.keys()

    def close_discovery_with_year(self, start_target_label_type="Gene", start_target_id="PR:000003035",
                        end_target_label_type="Gene", end_target_id="PR:000003035", start_years = 1990, end_years = 2000):

        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id, start_target_label_type)
        search_end_temp = self.node_id_with_lable(end_target_id, end_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.close_discovery_tx_with_year, start_target_label_type, start_target_id,
                                               end_target_label_type, end_target_id, start_years, end_years)

        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
            if (i["cd"] == end_target_id):
                i["group"] = 1  # Query : 1
            # if ("fix_x" not in i and "fix_y" not in i):
            #     i["fix_x"] = self.center_x
            #     i["fix_y"] = self.center_y

        for i in self.data['links']:
            if (i["source"] == str(search_start_temp)): i["group"] = 1 # Direct_connection : 1
            if (i["source"] == str(search_end_temp)): i["group"] = 1  # Direct_connection : 1
            if (i["target"] == str(search_start_temp)): i["group"] = 1  # Direct_connection : 1
            if (i["target"] == str(search_end_temp)): i["group"] = 1  # Direct_connection : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        for i in result:
            #print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                #print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "," + str(search_end_temp) + "]")
        #print("Return n")
        return result


    def close_discovery_tx_with_year(self, tx, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035", start_years = 1990, end_years = 2000):


        result_nodes = {}

        nodes = []
        # lable_web_dictionary = {"Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6, "CellLine": 7,
        #                     "Hallmark": 8}

        # with size((c)--()) as N, ID(c) as M
        # return M,N ORDER BY N DESC LIMIT 10



        run_text = ""
        run_text = "MATCH (A:" + start_target_label_type + " {ID:\"" + start_target_id + "\"})\nRETURN A"
        try:
            for record in tx.run(run_text):
                for node in record:
                    nodes.append({"nid": str(node.id), "cd": node._properties['ID'], "nm": node._properties['text'],
                                  "group": self.lable_web_dictionary[node._properties['type']],"fix_x" : self.m[1], "fix_y" : self.center_y})
                    break
        except:
            print("node id not found : " +start_target_id)
            return -1


        #web layout examples
                # final_nodes[i]['x'] = center_x
                # final_nodes[i]['y'] = center_y


        run_text = ""
        run_text = "MATCH (A:" + end_target_label_type + " {ID:\"" + end_target_id + "\"})\nRETURN A"
        try:
            for record in tx.run(run_text):
                for node in record:
                    nodes.append({"nid": str(node.id), "cd": node._properties['ID'], "nm": node._properties['text'],
                                  "group": self.lable_web_dictionary[node._properties['type']],"fix_x" : self.w+self.m[3], "fix_y" : self.center_y})
                    break
        except:
            print("node id not found : " + end_target_id)
            return -1


        run_text = ""
        run_text = run_text + "Match p = (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "RETURN c"
        #print(run_text)
        # run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        # run_text = run_text + "with distinct c\n"
        # run_text = run_text + "WHERE ALL (r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998) or exists(r.cnt_1997) or exists(r.cnt_1996) or exists(r.cnt_1995) or exists(r.cnt_1994) or exists(r.cnt_1993) or exists(r.cnt_1992) or exists(r.cnt_1991) or exists(r.cnt_1990))" + "\n"
        # run_text = run_text + "UNWIND relationships(p) as results" + "\n"
        # run_text = run_text + "return id(results), id(startNode(results)),id(endNode(results)), results.cnt_1999, results.cnt_1998, results.cnt_1997, results.cnt_1996, results.cnt_1995, results.cnt_1994, results.cnt_1993, results.cnt_1992, results.cnt_1991, results.cnt_1990" + "\n"
        # run_text = run_text + "LIMIT 1000"


        for record in tx.run(run_text):
            for node in record:
                nodes.append({"nid":str(node.id),"cd":node._properties['ID'],"nm":node._properties['text'],"group":self.lable_web_dictionary[node._properties['type']]})
                #print(node)
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple(d.items())
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #print(ex_nodes)

        #print(a.data['nodes'])
        output_list = []
        links = []
        #],\"links\":[{\"source\":\"ds39\",\"target\":\"ge518\"},{\"source\":\"ds39\",\"target\":\"ge559\"}
        #match (n)-[r]-(m)
        #return id(startNode(r)),id(endNode(r))
        #limit 10

        run_text = ""
        run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })-[r1]-(c)-[r2]-(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "RETURN r1,r2"
        links_temp = []
        for record in tx.run(run_text):
            total_edge_cnt = 0
            for edges in record:
                for i in range(start_years,end_years):
                    cnt_property_text = "cnt_"+str(i)
                    try :
                        total_edge_cnt += edges._properties[cnt_property_text]
                    except:
                        continue
            for edges in record:
                links_temp.append({"source":str(edges.start_node.id),"target":str(edges.end_node.id), "cnt":total_edge_cnt, "group" : 1})
                output_list.append(edges)

        #print(links)
        links.clear()
        sorted_links = sorted(links_temp, key=lambda k:k['cnt'], reverse=True)


        sorted_nodes = []
        for i in range(0,50):
            links.append(sorted_links[i])
            sorted_nodes.append(sorted_links[i]['source'])
            sorted_nodes.append(sorted_links[i]['target'])

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)


        final_nodes = []
        for i in ex_nodes:
            for j in nodes:
                if(j['nid'] == i) :
                    final_nodes.append(j)
                    break

        run_text = ""
        run_text = run_text + "Match (FinalNodes) \n"
        nodes_text = "Where "
        for i in final_nodes:
            nodes_text = nodes_text + "ID(FinalNodes) = " + str(i["nid"]) + " Or "
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text +"\n"
        run_text = run_text + "WITH collect(FinalNodes) as nodes" + "\n"
        run_text = run_text + "UNWIND nodes as n" + "\n"
        run_text = run_text + "UNWIND nodes as m" + "\n"
        run_text = run_text + "Match (n)-[r1]-(m)\n"
        run_text = run_text + "RETURN r1"
        links_temp = []

        for record in tx.run(run_text):
            for edges in record:
                total_edge_cnt = 0
                for i in range(start_years, end_years):
                    cnt_property_text = "cnt_"+str(i)
                    try :
                        total_edge_cnt += edges._properties[cnt_property_text]
                    except:
                        continue
                if(total_edge_cnt == 0): continue

                links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                                   "cnt": total_edge_cnt, "group": 3})
                links.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                                   "cnt": total_edge_cnt, "group": 3})

        self.data['nodes'] = final_nodes


        self.data['links'] = links
        #print(a.data['links'])

        return output_list

    def shortestpath_discovery_with_years(self, start_target_label_type="Disease", start_target_id="MESH:D018784", years = 1990):
        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.shortestpath_discovery_with_years_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, years = years)

        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        for i in result:
            #print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                #print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "]")
        #print("Return n")
        return result


    def shortestpath_discovery_with_years_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", years=1990):
        #년도 별로 적용해야 될 필요성 있
        result_nodes = {}

        #MATCH(s: Disease)
        #where ID(s) = 124302
        #WITH s
        # MATCH
        # p = shortestpath((Disease00001:Disease {ID:"MESH:D018784"}) - [*0..3] - (disease_web:Disease))
        # WHERE ALL(r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998))
        # UNWIND relationships(p) as results
        # return id(results), results.cnt_1999, results.cnt_1998
        # LIMIT
        # 100

        run_text = ""
        run_text = run_text + "MATCH (s:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(s) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH s" + "\n"
        run_text = run_text + "MATCH p = shortestpath((s) - [*0..3] - (General_web:" + start_target_label_type +"))"+"\n"
        run_text = run_text + "WHERE ALL (r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998) or exists(r.cnt_1997) or exists(r.cnt_1996) or exists(r.cnt_1995) or exists(r.cnt_1994) or exists(r.cnt_1993) or exists(r.cnt_1992) or exists(r.cnt_1991) or exists(r.cnt_1990))"+"\n"
        run_text = run_text + "UNWIND relationships(p) as results"+"\n"
        run_text = run_text + "return id(results), id(startNode(results)),id(endNode(results)), results.cnt_1999, results.cnt_1998, results.cnt_1997, results.cnt_1996, results.cnt_1995, results.cnt_1994, results.cnt_1993, results.cnt_1992, results.cnt_1991, results.cnt_1990"+"\n"
        run_text = run_text + "LIMIT 1000"

        #print(run_text)
        result_list = []
        property_dic = {}
        sorted_cnt = []
        for record in tx.run(run_text):
            sum_value = 0
            for j,value in enumerate(record):
                if(j == 0 and j == 1 and j == 2) : continue
                elif (value == None): continue
                else : sum_value = sum_value + int(value)
            result_list.append([record[0],record[1],record[2],sum_value])
            #result_list.append(sum_value)
        sorted_cnt = sorted(result_list, key=operator.itemgetter(3), reverse=True)

        run_text = ""
        run_text = run_text + "MATCH (a)-[r]-(b)\n"
        run_text = run_text + "WHERE ID(r) IN[\n"
        # {"nodes": [{"nid":"ds39","cd":"H00031","nm":"Breast cancer","group":1}]
        len_sorted_cnt = len(sorted_cnt)
        for j in range(100):
            if(j == len_sorted_cnt): break
            run_text = run_text + str(sorted_cnt[j][0]) + ","
        run_text = run_text.rstrip(",")
        run_text = run_text + "]\nwith a,b as c \nRETURN c"

        nodes = []
        # lable_web_dictionary = {"Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6, "CellLine": 7,
        #                     "Hallmark": 8}
        for record in tx.run(run_text):
            for node in record:
                nodes.append({"nid":str(node.id),"cd":node._properties['ID'],"nm":node._properties['text'],"group":self.lable_web_dictionary[node._properties['type']]})
                #print(node)
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple(d.items())
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #print(ex_nodes)
        self.data['nodes'] = ex_nodes
        #print(a.data['nodes'])
        output_list = []
        links = []
        #],\"links\":[{\"source\":\"ds39\",\"target\":\"ge518\"},{\"source\":\"ds39\",\"target\":\"ge559\"}
        #match (n)-[r]-(m)
        #return id(startNode(r)),id(endNode(r))
        #limit 10
        node_seach_check = False
        for j in range(len(sorted_cnt)):
            node_seach_check = False
            for k in ex_nodes:
                if k["nid"] == str(sorted_cnt[j][1]) :
                    node_seach_check = True
                    break
            if(node_seach_check == False) : continue
            node_seach_check = False
            for k in ex_nodes:
                if k["nid"] == str(sorted_cnt[j][2]) :
                    node_seach_check = True
                    break
            if (node_seach_check == False): continue
            links.append({"source":str(sorted_cnt[j][1]),"target":str(sorted_cnt[j][2]), "group" : 1})
            output_list.append(sorted_cnt[j])

        #print(links)

        self.data['links'] = links
        #print(a.data['links'])
        return output_list


    def neighbor_discovery_with_years(self, start_target_label_type="Disease", start_target_id="MESH:D018784", start_years = 1990, end_years = 2000):
        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        if(search_start_temp == -1):
            print(str(start_target_label_type) + " " + str(start_target_id) + " Search Failed!! [no starting node in our neo4j server]")
            return 0
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.neighbor_discovery_with_years_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, start_years = start_years, end_years = end_years)

        if(result == 0):
            return 0
        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        #for i in result:
            #print(str(i), end=',')
         #   cnt += 1
          #  if (cnt == 15):
                #print("\n")
           #     cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "]")
        #print("Return n")
        return result


    def neighbor_discovery_with_years_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", start_years=1990, end_years=2000):

        result_nodes = {}

        #MATCH(s: Disease)
        #where ID(s) = 124302
        #WITH s
        # MATCH
        # p = shortestpath((Disease00001:Disease {ID:"MESH:D018784"}) - [*0..3] - (disease_web:Disease))
        # WHERE ALL(r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998))
        # UNWIND relationships(p) as results
        # return id(results), results.cnt_1999, results.cnt_1998
        # LIMIT
        # 100
        cnt_text = ""
        coalesce_text = ""
        cnt_property_text = ""
        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH p = (General_Node00001) - [s:cooccurnce] - (General_Node_web)"+"\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH General_Node00001, General_Node_web, s, "
        for i in range(start_years, end_years):
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(s." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(s." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return s, cnt, General_Node00001, General_Node_web \n"
        run_text = run_text + "limit 1000"

        nodes = []
        links_temp = []
        node_check = False
        for edge in tx.run(run_text):
            node_check = True
            edges = edge[0]
            total_edge_cnt = edge[1]
            start_node = edge[2]
            end_node = edge[3]

            links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                               "cnt": total_edge_cnt, "group": 1})
            try:
                nodes.append(
                    {"nid": str(start_node.id), "cd": start_node._properties['ID'], "nm": start_node._properties['text'],
                     "group": self.lable_web_dictionary[start_node._properties['type']]})

                nodes.append({"nid": str(end_node.id), "cd": end_node._properties['ID'],
                          "nm": end_node._properties['text'],
                          "group": self.lable_web_dictionary[end_node._properties['type']]})
            except:
                print("except")

        links = []
        if(node_check == False):
            print(str(start_target_label_type) + " "+ str(start_target_id)+" Search Failed!! [no connected edgein our neo4j server]")
            self.data['nodes'] = 0
            return 0
        General_Node00001 = start_node
        # for starting point of open query

        sorted_links = sorted(links_temp, key=lambda k: k['cnt'], reverse=True)

        sorted_nodes = []
        for i in range(0, 20):
            try:
                links.append({'source': sorted_links[i]['source'], 'target': sorted_links[i]['target'], 'cnt':sorted_links[i]['cnt'],
                              'group': sorted_links[i]['group']})
                sorted_nodes.append(sorted_links[i]['source'])
                sorted_nodes.append(sorted_links[i]['target'])
            except:
                break

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)

        final_nodes = []
        for i in ex_nodes:

            for j in nodes:
                if (j['nid'] == i):
                    final_nodes.append(j)
                    break

        self.data['nodes'] = final_nodes
        self.data['links'] = links

        run_text = ""
        run_text = run_text + "MATCH (SSS)" + "\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "

        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"

        run_text = run_text + "Match (b)\n"

        nodes_text = "Where "
        for i in final_nodes:
            nodes_text = nodes_text + "ID(b) = " + str(i["nid"]) + " Or "
        nodes_text = nodes_text[:-3]

        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a, b\n"
        run_text = run_text + "Match (a)-[r:cooccurnce]-(b)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH a, r, b, "
        for i in range(start_years, end_years):
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(r." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(r." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return r, a, b, cnt \n"
        #run_text = run_text + "limit 1000"

        links_temp = []
        nodes = []
        for edge in tx.run(run_text):
            edges = edge[0]
            start_node = edge[1]
            end_node = edge[2]
            total_edge_cnt = edge[3]
            if(start_node.id == General_Node00001.id or end_node.id == General_Node00001.id) : continue
            # a.data['links'].append({"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt": total_edge_cnt, "group": 1})
            self.data['links'].append(
                {"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt":total_edge_cnt, "group": 4})

        return result_nodes
    def neighbor_nodes_query(self, start_target_label_type="Disease", start_target_id="MESH:D018784", relationtype="Disease_Tree"):
        # just formatting for close discovery

        # MESH:C
        # 7410146

        start_target_label_type = "Disease_hierarchy"
        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.neighbor_nodes_query_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, relationtype=relationtype)


        return result


    def neighbor_nodes_query_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", relationtype="Disease_Tree"):

        #MESH:C
        #7410146
        start_target_id = "7410146"

        result_nodes = {}

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH (General_Node00001) - [s:" + str(relationtype) + "] - (General_Node_web)"+"\n"
        run_text = run_text + "Return General_Node_web"

        nodes = tx.run(run_text)

        return nodes

    def hierarchy_edge_update(self, start_target_label_type="Disease", start_target_id="MESH:D018784", relationtype="Disease_Tree"):
        # just formatting for close discovery

        # MESH:C
        # 7410146

        start_target_label_type = "Disease"
        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.hierarchy_edge_update_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, relationtype=relationtype)


        return result


    def hierarchy_edge_update_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", relationtype="Disease_Tree"):

        #MESH:C
        #7410146

        relationtype1 = "cooccurnce"

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH (General_Node00001) - [s:" + str(relationtype1) + "] - (General_Node_web)"+"\n"
        run_text = run_text + "Return s"


        for i in tx.run(run_text):
            #relationship_type: str = "cooccurnce", ** properties
            #update relationship
            temp3 = self.check_relationships_by_id_with_properties(i[0].start, i[0].end, "Disease_Tree")
            self.merge_relationships_cnt_by_id_with_year(i[0].start,i[0].end,"cooccurnce",i[0]._properties)
        return 1

def disease_hierarchy():
    global a
    f = open('./CTD_diseases.obo', 'r')
    content = f.read()
    terms = content.split('\n[Term]\n')

    organism_disease_info = {}
    organism_disease_rows = []
    disease_info = {}
    disease_rows = []

    rels = []

    for item in terms:
        for line in item.splitlines():
            if line.split(':')[0] == 'id':
                organism_disease_info['Disease_ID'] = line.lstrip('id: ')
            elif line.split(':')[0] == 'name':
                organism_disease_info['Name'] = line.lstrip('name: ')

        for line in item.splitlines():
            if (line.split(':')[0] == 'is_a'):
                rels.append([organism_disease_info['Disease_ID'], line.lstrip('is_a: ').split(' ! ')[0]])
                organism_disease_info['Parent_ID'] = line.lstrip('is_a: ').split(' ! ')[0]

        organism_disease_rows.append(organism_disease_info.copy())

#    check_node_id_with_lable
    for i in rels:

        if ( a.node_id_with_lable(node1_name = i[0], node1_domain = "Disease_hierarchy") == -1): a.add_nodes("Disease_hierarchy", ID = i[0])
        if ( a.node_id_with_lable(node1_name = i[1], node1_domain = "Disease_hierarchy") == -1): a.add_nodes("Disease_hierarchy", ID = i[1])
        a.create_relationship_with_domain(node1_name = i[0], node1_domain = "Disease_hierarchy", node2_name = i[1], node2_domain = "Disease_hierarchy", relationship_type = "Disease_Tree")
    f.close()

def csv_parser(temp_in):
    #for eliminationg , between double qutation
    temp_list = []
    temp_str = ""
    quote_cnt = 0
    for c in temp_in:
        if c == ',' and quote_cnt % 2 == 0:
            if(quote_cnt != 0 and temp_str[-1] != "\""):
                if c == "\"": quote_cnt += 1
                #if c == "\"" or c == "\'": quote_cnt += 1
                #5'-nucleotidase 때문에 안됨
                temp_str += c
                continue
            quote_cnt = 0
            temp_list.append(temp_str)
            temp_str = ""
        else:
            if c == "\"": quote_cnt += 1
            temp_str += c
    temp_list.append(temp_str)
    temp_str = ""
    return temp_list
def edge_input(input_file = "F://LionDB//complete_MESHD000544_MESHD004967.tar//complete_MESHD000544_MESHD004967//edges.csv"):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"
    node1_id = 0
    node2_id = 0

    csv_file = fileinput.input(input_file)
    csv_config = csv_file.readline().rstrip('\n').split(',')

    relationship_cnt = 1
    csv_dictionary = {}

    for i in range(0,len(csv_config)):
        if (csv_config[i][0] == ':'):
            csv_config[i] = csv_config[i][1:]
        elif (':' in csv_config[i]):
            csv_config[i] = csv_config[i].split(':')[0]
        csv_dictionary[csv_config[i]] = i
    print(csv_config)
    line_cnt = 1
    edge_input_dictionary = {}
    cnt3 = 1
    for line in csv_file:
        if (0 > cnt3):
            cnt3 = cnt3 + 1
            if (cnt3 % 10000 == 0): print(cnt3)
            continue
        line_temp = csv_parser(line.rstrip('\n'))

        type_of_relationship = line_temp[csv_dictionary["TYPE"]]
        node1_name = line_temp[csv_dictionary["START_ID"]]
        node2_name = line_temp[csv_dictionary["END_ID"]]
        relationship_cnt = relationship_cnt + 1

        for j in range(2,len(csv_config)):
            edge_input_dictionary[csv_config[j]] = line_temp[j]

        a.create_relationship(node1_name, node2_name, type_of_relationship, edge_input_dictionary)
        #create_relationship_with_domain
        if(relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt*10000)
            line_cnt += 1

    csv_file.close()
def edge_input_domain_fix(input_file = "F://LionDB//complete_MESHD000544_MESHD004967.tar//complete_MESHD000544_MESHD004967//edges.csv",domain1="Pro_Sub",domain2="Gene"):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"
    node1_id = 0
    node2_id = 0

    csv_file = fileinput.input(input_file)
    csv_config = csv_file.readline().rstrip('\n').split(',')

    relationship_cnt = 1
    csv_dictionary = {}

    for i in range(0,len(csv_config)):
        if (csv_config[i][0] == ':'):
            csv_config[i] = csv_config[i][1:]
        elif (':' in csv_config[i]):
            csv_config[i] = csv_config[i].split(':')[0]
        csv_dictionary[csv_config[i]] = i
    print(csv_config)
    line_cnt = 1
    edge_input_dictionary = {}
    cnt3 = 1
    for line in csv_file:
        if (0 > cnt3):
            cnt3 = cnt3 + 1
            if (cnt3 % 10000 == 0): print(cnt3)
            continue
        line_temp = csv_parser(line.rstrip('\n'))

        type_of_relationship = line_temp[csv_dictionary["TYPE"]]
        node1_name = line_temp[csv_dictionary["START_ID"]]
        node2_name = line_temp[csv_dictionary["END_ID"]]
        relationship_cnt = relationship_cnt + 1

        for j in range(2,len(csv_config)):
            edge_input_dictionary[csv_config[j]] = line_temp[j]

        a.create_relationship_with_domain(node1_name, domain1,node2_name, domain2, type_of_relationship, edge_input_dictionary)
        #node1_name: str = "MESH", node1_domain: str = "Chemical", node2_name: str = "TAXID", node2_domain: str = "Chemical",relationship_type: str = "knows", properties: dict = {}) :
        if(relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt*10000)
            line_cnt += 1

    csv_file.close()

def edge_year_input(input_file = "F://LionDB//complete_MESHD000544_MESHD004967.tar//complete_MESHD000544_MESHD004967//edges.csv"):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"
    node1_id = 0
    node2_id = 0
    lable_reverse_dictionary = {1:"Chemical", 2:"Disease", 3:"Mutation", 4:"Gene", 5:"Species", 6:"CellLine",
                                            7:"Hallmark", 8:"Pro"}
    #lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
    #                    "Hallmark": 7, "Pro" : 8}
    csv_file = fileinput.input(input_file,  openhook=fileinput.hook_encoded("utf-8-sig"))
    csv_config = csv_file.readline().rstrip('\n').split(',')

    relationship_cnt = 1
    csv_dictionary = {}

    for i in range(0,len(csv_config)):
        if (csv_config[i][0] == ':'):
            csv_config[i] = csv_config[i][1:]
        elif (':' in csv_config[i]):
            csv_config[i] = csv_config[i].split(':')[0]
        csv_dictionary[csv_config[i]] = i
    print(csv_config)
    line_cnt = 1
    edge_input_dictionary = {}
    cnt3 = 1
    for line in csv_file:
        if (0 > cnt3):
            cnt3 = cnt3 + 1
            if (cnt3 % 10000 == 0): print(cnt3)
            continue
        line_temp = csv_parser(line.rstrip('\n'))

        type_of_relationship = "cooccurnce"
        node1_name = line_temp[csv_dictionary["NODE1_ID"]].split(";")[0].rstrip(' ')

        try :
            node1_domain = lable_reverse_dictionary[int(line_temp[csv_dictionary["NODE1_DOMAIN"]])]
        except:
            print("Node1_DOMAIN Erorr!",cnt3)
            print(line)
        node2_name = line_temp[csv_dictionary["NODE2_ID"]].split(";")[0].rstrip(' ')
        #.split(";")[0] for Gene:3484;3485;3489
        # if("CHEBI" in node1_name or "CHEBI" in node2_name) :
        #     print("CHEBI skip :", node1_name,"&&", node2_name)
        #     continue
        try :
            node2_domain = lable_reverse_dictionary[int(line_temp[csv_dictionary["NODE2_DOMAIN"]])]
        except:
            print("Node1_DOMAIN Erorr!",cnt3)
            print(line)
        relationship_cnt = relationship_cnt + 1

        edge_input_dictionary = {}
        for j in range(0,len(csv_config)):
            if(csv_config[j] == "NODE1_ID" or csv_config[j] == "NODE1_DOMAIN" or csv_config[j] == "NODE2_ID" or csv_config[j] == "NODE2_DOMAIN" ): continue
            elif csv_config[j] == "YEAR" :
                temp_year = int(line_temp[j])
            elif csv_config[j] == "COUNT" :
                edge_input_dictionary["cnt_"+str(temp_year)]  = line_temp[j]
                temp_year_cnt = int(line_temp[j])
            else : edge_input_dictionary[csv_config[j]] = line_temp[j]

        try : temp_year = int(line_temp[csv_dictionary["YEAR"]])
        except :
            print("year error : ",temp_year)
            continue
        if(temp_year <= 1992) : continue

        temp_node1_id = a.node_id_with_lable(node1_name,node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name,node2_domain)

        if(temp_node1_id == -1 or temp_node2_id == -1): continue
        if (temp_node1_id == None or temp_node2_id == None): continue

        if(node2_name == "MESH:C051890"):
            node2_name = node2_name
        print(node1_name, node1_domain, node2_name, node2_domain, type_of_relationship, edge_input_dictionary)
        temp003 = a.check_relationships_by_id(temp_node1_id,temp_node2_id, type_of_relationship)
        # print(temp003)
        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id,temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif(temp003 == -2):
            print("unkown relationship error")
            print(node1_name,node1_domain,node2_name,node2_domain)
            continue
        else:
            a.update_relationships_cnt_by_id_with_year(temp_node1_id, temp_node2_id, temp003, type_of_relationship, temp_year, temp_year_cnt)

        if(relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt*10000)
            line_cnt += 1

    csv_file.close()
def edge_year_input_node_loaded(input_file = "F://LionDB//complete_MESHD000544_MESHD004967.tar//complete_MESHD000544_MESHD004967//edges.csv"):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"
    node1_id = 0
    node2_id = 0
    lable_reverse_dictionary = {1: "Chemical", 2: "Disease", 3: "Mutation", 4: "Gene", 5: "Species", 6: "CellLine",
                                7: "Hallmark", 8: "Pro"}
    # lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
    #                    "Hallmark": 7, "Pro" : 8}
    csv_file = fileinput.input(input_file,  openhook=fileinput.hook_encoded("utf-8-sig"))
#    csv_config = csv_file.readline().rstrip('\n').split(',')
    csv_config = "NODE1_ID,NODE1_DOMAIN,NODE2_ID,NODE2_DOMAIN,YEAR,COUNT".rstrip('\n').split(',')
    relationship_cnt = 1
    csv_dictionary = {}

    for i in range(0,len(csv_config)):
        if (csv_config[i][0] == ':'):
            csv_config[i] = csv_config[i][1:]
        elif (':' in csv_config[i]):
            csv_config[i] = csv_config[i].split(':')[0]
        csv_dictionary[csv_config[i]] = i
    print(csv_config)
    line_cnt = 1
    edge_input_dictionary = {}
    cnt3 = 1
    for line in csv_file:
        if (0 > cnt3):
            cnt3 = cnt3 + 1
            if (cnt3 % 10000 == 0): print(cnt3)
            continue
        line_temp = csv_parser(line.rstrip('\n'))

        type_of_relationship = "co_occurnce"
        node1_name = line_temp[csv_dictionary["NODE1_ID"]].split(";")[0].rstrip(' ')
        try:
            node1_domain = lable_reverse_dictionary[int(line_temp[csv_dictionary["NODE1_DOMAIN"]])]
        except:
            print("NODE1_DOMIAN ERROR!!",cnt3)
            print(line)
            continue
        node2_name = line_temp[csv_dictionary["NODE2_ID"]].split(";")[0].rstrip(' ')
        #.split(";")[0] for Gene:3484;3485;3489
        # if("CHEBI" in node1_name or "CHEBI" in node2_name) :
        #     print("CHEBI skip :", node1_name,"&&", node2_name)
        #     continue
        if ("rs" in node1_name  or "rs" in node2_name):
            print("Mutation skip :", node1_name, "&&", node2_name)
            continue
        try:
            node2_domain = lable_reverse_dictionary[int(line_temp[csv_dictionary["NODE2_DOMAIN"]])]
        except:
            print("NODE2_DOMAIN ERROR!!",cnt3)
            print(line)
            continue
        relationship_cnt = relationship_cnt + 1

        edge_input_dictionary = {}
        for j in range(0,len(csv_config)):
            if(csv_config[j] == "NODE1_ID" or csv_config[j] == "NODE1_DOMAIN" or csv_config[j] == "NODE2_ID" or csv_config[j] == "NODE2_DOMAIN" ): continue
            elif csv_config[j] == "YEAR" :
                temp_year = int(line_temp[j])
            elif csv_config[j] == "COUNT" :
                edge_input_dictionary["cnt_"+str(temp_year)]  = line_temp[j]
                temp_year_cnt = int(line_temp[j])
            else : edge_input_dictionary[csv_config[j]] = line_temp[j]

        #temp_node1_id = a.node_id_with_lable(node1_name,node1_domain)
        #temp_node2_id = a.node_id_with_lable(node2_name,node2_domain)
        if("Gene" in node1_name and "GeneID" not in node1_name) :
            node1_name = "GeneID:"+node1_name.split("Gene:")[-1]
        if ("Gene" in node2_name and "GeneID" not in node2_name):
            node2_name = "GeneID:" + node2_name.split("Gene:")[-1]
        print(node1_name,",", node2_name)
        temp_node1_id = a.nodes.get(node1_name, -1)
        temp_node2_id = a.nodes.get(node2_name, -1)


        if(temp_node1_id == -1 or temp_node2_id == -1): continue

        try : temp_year = int(line_temp[csv_dictionary["YEAR"]])
        except :
            print("year error : ",temp_year)
            continue
        #if(temp_year <= 1975) : continue
        #print(node1_name, node1_domain, node2_name, node2_domain, type_of_relationship, edge_input_dictionary)
        temp003 = a.check_relationships_by_id(temp_node1_id,temp_node2_id, type_of_relationship)
        # print(temp003)
        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id,temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif(temp003 == -2):
            print("unkown relationship error")
            print(node1_name,node1_domain,node2_name,node2_domain)
            continue
        else:
            a.update_relationships_cnt_by_id_with_year(temp_node1_id, temp_node2_id, temp003, type_of_relationship, temp_year, temp_year_cnt)

        if(relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt*10000)
            line_cnt += 1

    csv_file.close()
def edge_pmid_input_Bern(input_file = "./bern_edge_combination_sorted_merged2_.txt"):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"

    node1_id = 0
    node2_id = 0
    node1_domain = ""
    node2_domain = ""

    Bern_lable_reverse_dictionary = {"drug":"Drug", "disease":"Disease", "mutation":"Mutation", "gene":"Gene", "species":"Species", "miRNA":"miRNA",
                                            "pathway":"pathway"}
    lable_reverse_dictionary = {1:"Chemical", 2:"Disease", 3:"Mutation", 4:"Gene", 5:"Species", 6:"CellLine",
                                            7:"Hallmark", 8:"Pro"}

    #lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
    #                    "Hallmark": 7, "Pro" : 8}
    f = open(input_file,"r")

    relationship_cnt = 1
    line_cnt = 1

    edge_input_dictionary = {}
    cnt3 = 1

    while True:
        line = f.readline()
        if not line : break
        line_temp = line.split("@#$")
        type_of_relationship = "PMID_cooccurnce"

        # if('CUI-less' in line_temp[2]):
        #     line_temp[2] = "CUI-less-"+str(line_temp[0])
        node1_name = line_temp[2].split("|")[0]
        try :
            node1_domain = Bern_lable_reverse_dictionary[str(line_temp[1])]
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        # if ('CUI-less' in line_temp[5]):
        #     line_temp[5] = "CUI-less-" + str(line_temp[3])
        node2_name = line_temp[5].split("|")[0]
        try :
            node2_domain = Bern_lable_reverse_dictionary[str(line_temp[4])]
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["PMID_CNT"] = int(line_temp[6])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)

        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1

        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        if (temp003 == -1):
            print(str(node1_name) + "_XXXX_" + str(node2_name))
            continue
        else:
            continue
        #-----------
        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        # print(temp003)
        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()


def node_input(input_file= "C://Users//kms0845//Downloads//LionDB//Node_Cellline.csv"):
    global a
#    input_file =
#    output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"


    csv_file = fileinput.input(input_file, openhook=fileinput.hook_encoded("utf-8-sig"))
    csv_config = csv_file.readline().rstrip('\n').split('@#$')
    print(csv_config)
    csv_input_dictionary = {}
    for i in range(0, len(csv_config)):
        if (csv_config[i][0] == ':'):
            csv_config[i] = csv_config[i][1:]
        elif (':' in csv_config[i]):
            csv_config[i] = csv_config[i].split(':')[0]
        if (csv_config[i].upper() == "TYPE"): csv_config[i] = 'type'
    for i in range(0, len(csv_config)):
        csv_input_dictionary[csv_config[i]] = i
    node_cnt = 1
    try:
        type_index = csv_input_dictionary["type"]
    except:
        type_index = csv_input_dictionary["Type"]

    node_input_dictionary = {}

    cnt = 0
    line_temp = ""
    for line in csv_file:
        label_type = ""
        temp_in = ""
        #,"라는 패턴이 나오면 ",까지 대기

        # if(line.split(",")[-1] != "KEGG\n" and line.split(",")[-1] != "KNApSAcK\n" and line.split(",")[-1] != "COCONUT\n"):
        #    line_temp = line_temp+line.rstrip('\n')
        #    continue
        # else:
        #     line = line_temp + line
        #     line_temp = ""

        #temp_in = csv_parser(line.rstrip('\n'))
        temp_in = line.rstrip('\n').split("@#$")
        cnt = cnt + 1
        #if(cnt < 67040) : continue
        print(temp_in)

        for j in range(0,len(csv_config)):
            node_input_dictionary[csv_config[j]] = temp_in[j]

        try :
            label_type = temp_in[type_index]
        except:
            print("add node without type error.")
            continue

        if(a.node_id_with_lable(node_input_dictionary['ID'],label_type) == -1):
            a.add_nodes(label_type, **node_input_dictionary)
        else:
            print(node_input_dictionary['ID']+" exists")

    print("\nUpload done")
    csv_file.close()

def node_input_BERN(input_file_path="./Corona_Nodes/bern_disease_cui_sorted.txt",data_type="Disease"):
    global a
    #    input_file =
    #    output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"


    #{
    # "LABEL": "entity",
    # "text": "Acetylmuramyl-Alanyl-Isoglutamine",
    # "OID": "D09.067.550.050;D09.811.522.050;D12.644.233.050;",
    # "ID": "MESH:D000119",
    # "type": "Chemical",
    # "remarks": ""
    # }

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()
    csv_input_dictionary = {}

    node_input_dictionary = {"LABLE":"entity","text":"text_null","OID":"OID_null","ID":"ID_null","type":data_type,"remarkts":""}

    cnt = 0
    line_temp = ""
    for line in input_file:
        label_type = ""
        temp_in = line.rstrip("\n").split("@#$")

        node_input_dictionary["text"] = temp_in[0]
        node_input_dictionary["OID"] = temp_in[2]
        node_input_dictionary["ID"] = temp_in[2].split("|")[0]

        temp_in = csv_parser(line.rstrip('\n'))

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

## Node upload method 추가 작업 진행

def node_input_Disease_DisGeNET(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Disease_DisGeNET.txt",entity="MeSH_ID",text="Disease_name",OID="DB_ID",data_type="Disease",remarks="Disease_SemanticType"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_DisGeNET":text,"OID_DisGeNET":OID,"type":data_type,"remarks_DisGeNET":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_DisGeNET"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_DisGeNET"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Disease"
        node_input_dictionary["remarks_DisGeNET"] = str(temp_in[6]).replace('"','')


        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Disease_ChEMBL(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Disease_ChEMBL.txt",entity="MeSH_ID",text="Disease_name",OID="DB_ID",data_type="Disease",remarks="EFO_Terms"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_ChEMBL":text,"OID_ChEMBL":OID,"type":data_type,"remarks_ChEMBL":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_ChEMBL"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_ChEMBL"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Disease"
        node_input_dictionary["remarks_ChEMBL"] = str(temp_in[3]).replace('"','')


        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Disease_CTD(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Disease_CTD.txt",entity="MeSH_ID",text="Disease_name",data_type="Disease"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_CTD":text,"OID_CTD":"OID_null","type":data_type,"remarks_CTD":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_CTD"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Disease"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Protein_ChEMBL(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Protein_ChEMBL.txt",entity="Uniprot_ID",text="Protein_name",OID="DB_ID",data_type="Protein", remarks="Protein_Type"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_ChEMBL":text,"OID_ChEMBL":OID,"type":data_type,"remarks_ChEMBL":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_ChEMBL"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_ChEMBL"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Protein"
        node_input_dictionary["remarks_ChEMBL"] = str(temp_in[3]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Protein_BindingDB(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Protein_BindingDB.txt",entity="Uniprot_ID",text="Protein_name",OID="DB_ID",data_type="Protein", remarks="Uniprot_accessions"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_BindingDB":text,"OID_BindingDB":OID,"type":data_type,"remarks_BindingDB":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_BindingDB"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_BindingDB"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Protein"
        node_input_dictionary["remarks_BindingDB"] = str(temp_in[3]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Protein_Uniprot(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Protein_Uniprot.txt",entity="Uniprot_ID",text="Protein_name",data_type="Protein", remarks="Uniprot_accessions"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_Uniprot":text,"OID_Uniport":"OID_null","type":data_type,"remarks_Uniprot":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_Uniprot"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["type"] = "Protein"
        node_input_dictionary["remarks_Uniprot"] = str(temp_in[1]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Protein_TTD(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Protein_TTD.txt",entity="Uniprot_ID",text="Protein_name",OID="DB_ID",data_type="Protein", remarks="Protein_Type"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_TTD":text,"OID_TTD":OID,"type":data_type,"remarks_TTD":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_TTD"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_TTD"]  = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Protein"
        node_input_dictionary["remarks_TTD"] = str(temp_in[3]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Compound_ChEMBL(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Compound_ChEMBL.txt",entity="ChEMBL_ID", text="Molecular formula",OID="Molecular Species",data_type="Compound", remarks="smile"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_ChEMBL":text,"OID_ChEMBL":OID,"type":data_type,"remarks_ChEMBL":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_ChEMBL"] = str(temp_in[1]).replace('"','')
        node_input_dictionary["OID_ChEMBL"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["type"] = "Compound"
        node_input_dictionary["remarks_ChEMBL"] = str(temp_in[3]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Species_KEGG(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Species_KEGG.txt",entity="Scientific_name",text="DB_Code",OID="DB_ID",data_type="Species", remarks="Category"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_KEGG":text,"OID_KEGG":OID,"type":data_type,"remarks_KEGG":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["text_KEGG"] = str(temp_in[2]).replace('"','')
        node_input_dictionary["OID_KEGG"]  = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Species"
        node_input_dictionary["remarks_KEGG"] = str(temp_in[4]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Species_NPASS(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Species_NPASS.txt",entity="Scientific_name",OID="DB_ID",data_type="Species", remarks="org_tax_level"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_NPASS":"text_null","OID_NPASS":OID,"type":data_type,"remarks_NPASS":remarks}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["OID_NPASS"]  = str(temp_in[1]).replace('"','')
        node_input_dictionary["type"] = "Species"
        node_input_dictionary["remarks_NPASS"] = str(temp_in[2]).replace('"','')

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Species_KNApSAcK(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Species_KNApSAcK.txt",entity="Scientific_name",data_type="Species"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_KNApSAcK":"text_null","OID_KNApSAcK":"OID_null","type":data_type,"remarks_KNApSAcK":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["type"] = "Species"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Species_Uniprot(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Species_Uniprot.txt",entity="Scientific_name",data_type="Species"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_Uniprot":"text_null","OID_Uniprot":"OID_null","type":data_type,"remarks_Uniprot":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["type"] = "Species"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Species_COCONUT(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Species_COCONUT.txt",entity="Scientific_name",data_type="Species"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_COCONUT":"text_null","OID_COCONUT":"OID_null","type":data_type,"remarks_COCONUT":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["type"] = "Species"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_Bioactivity_KNApSAcK(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_Bioactivity_KNApSAcK.txt",entity="Bioactivity_keyword",data_type="Bioactivity"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_KNApSAcK":"text_null","OID_KNApSAcK":"OID_null","type":data_type,"remarks_KNApSAcK":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["type"] = "Bioactivity"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")

def node_input_FunctionalFood_COCONUT(input_file_path="C:\\Users\\seomyungwon\\Desktop\\Upload_test\\Node_FunctionalFood_COCONUT.txt",entity="FunctionalFood_name",data_type="FunctionalFood"):
    global a

    f = open(input_file_path,"r")
    input_file = f.readlines()
    f.close()

    node_input_dictionary = {"ID":entity,"text_COCONUT":"text_null","OID_COCONUT":"OID_null","type":data_type,"remarks_COCONUT":"remarks_null"}

    cnt = 0
    for line in input_file:
        temp_in = line.rstrip("\n").split("\t")

        node_input_dictionary["ID"] = str(temp_in[0]).replace('"','')
        node_input_dictionary["type"] = "FunctionalFood"

        cnt = cnt + 1

        print(temp_in)

        try:
            label_type = data_type
        except:
            print("add node without type error.")
            continue

        a.add_nodes(label_type, **node_input_dictionary)

    print("\nUpload done")


## Link upload method 추가 작업 진행
def edge_input_New(InputFilePath, InputFileName):
    global a
    #output_file = "C://Users//kms0845//Desktop//Work//Data//190531//edges_out_real.csv"

    node1_id = 0
    node2_id = 0
    node1_domain = ""
    node2_domain = ""

    Metabolite_lable_reverse_dictionary = {"Metabolite":"Metabolite", "disease":"Disease", "mutation":"Mutation", "gene":"Gene", "species":"Species", "miRNA":"miRNA",
                                            "pathway":"pathway"}


    #lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
    #                    "Hallmark": 7, "Pro" : 8}

    f = open(InputFilePath + InputFileName + ".txt","r")

    relationship_cnt = 1
    line_cnt = 1

    edge_input_dictionary = {}
    cnt3 = 1
    line = f.readline()

    while True:
        line = f.readline()
        if not line : break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = "Similarity_Distance"

        # if('CUI-less' in line_temp[2]):
        #     line_temp[2] = "CUI-less-"+str(line_temp[0])
        node1_name = line_temp[0]
        try :
            node1_domain = "Metabolite"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        # if ('CUI-less' in line_temp[5]):
        #     line_temp[5] = "CUI-less-" + str(line_temp[3])
        node2_name = line_temp[1]
        try :
            node2_domain = "Metabolite"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Similarity_Distance"] = float(line_temp[2])
        edge_input_dictionary["Entity"] = str("\"Entity\"")

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)

        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        # print(temp003)
        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Disease_Pathway_Protein_TTD(InputFilePath, InputFileName="Link_Disease_Pathway_Protein_TTD.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Pathway_name")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = line_temp[1].replace('"',"")
        print(node2_name)
        try :
            node2_domain = "Disease"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Pathway_name"] = str(line_temp[2]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)

        print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_Species_ChEMBL(InputFilePath, InputFileName="Link_Protein_Species_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Species"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_Species_Uniprot(InputFilePath, InputFileName="Link_Protein_Species_Uniprot.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Species"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Species_Bioactivity_KNApSAcK(InputFilePath, InputFileName="Link_Species_Bioactivity_KNApSAcK.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Species"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Bioactivity"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_EC50_Compound_BindingDB_ChEMBL(InputFilePath, InputFileName="Link_Protein_Bioassay_EC50_Compound_BindingDB_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Bioassay_EC50_nM")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Bioassay_EC50_nM"] = float(line_temp[2])
        edge_input_dictionary['equals'] = str(line_temp[3]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_IC50_Compound_BindingDB_ChEMBL(InputFilePath, InputFileName="Link_Protein_Bioassay_IC50_Compound_BindingDB_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Bioassay_IC50_nM")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Bioassay_IC50_nM"] = float(line_temp[2])
        edge_input_dictionary['equals'] = str(line_temp[3]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_Kd_Compound_BindingDB_ChEMBL(InputFilePath, InputFileName="Link_Protein_Bioassay_Kd_Compound_BindingDB_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Bioassay_Kd_nM")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Bioassay_Kd_nM"] = float(line_temp[2])
        edge_input_dictionary['equals'] = str(line_temp[3]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Protein_Ki_Compound_BindingDB_ChEMBL(InputFilePath, InputFileName="Link_Protein_Bioassay_Ki_Compound_BindingDB_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Bioassay_Ki_nM")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Protein"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Bioassay_Ki_nM"] = float(line_temp[2])
        edge_input_dictionary['equals'] = str(line_temp[3]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Disease_Compound_ChEMBL(InputFilePath, InputFileName="Link_Disease_Compound_ChEMBL.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Disease"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Species_Compound_NPASS(InputFilePath, InputFileName="Link_Species_Compound_NPASS.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Species"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Species_Pathway_Compound_KNApSAcK(InputFilePath, InputFileName="Link_Species_Pathway_Compound_KNApSAcK.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Pathway_name")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "Species"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Compound"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Pathway_name"] = str(line_temp[2]).replace('"','')

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()

def link_input_Species_FunctionalFood_COCONUT(InputFilePath, InputFileName="Link_FunctionalFood_Species_COCONUT.txt"):
    global a

    node1_domain = ""
    node2_domain = ""

    f = open(InputFilePath + InputFileName, "r")

    relationship_cnt = 1
    line_cnt = 1

    cnt3 = 1

    while True:
        line = f.readline()
        if not line: break
        line_temp = line.rstrip("\n").split("\t")
        type_of_relationship = str("Data_relationship")
        print(line_temp)

        node1_name = str(line_temp[0]).replace('"','')
        print(node1_name)
        try :
            node1_domain = "FunctionalFood"
        except:
            print("Node1_DOMAIN_1 Erorr!",cnt3)
            print(line)

        node2_name = str(line_temp[1]).replace('"','')
        print(node2_name)
        try :
            node2_domain = "Species"
        except:
            print("Node1_DOMAIN_2 Erorr!",cnt3)
            print(line)

        relationship_cnt = relationship_cnt + 1
        edge_input_dictionary = {}
        edge_input_dictionary["Data_relationship"] = float(line_temp[2])

        temp_node1_id = a.node_id_with_lable(node1_name, node1_domain)
        temp_node2_id = a.node_id_with_lable(node2_name, node2_domain)


        if (temp_node1_id == -1 or temp_node2_id == -1):
            print(str(node1_name)+"__"+str(node2_name))
            continue
        if (temp_node1_id == None or temp_node2_id == None):
            print(str(node1_name) + "__" + str(node2_name))
            continue

        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1


        temp003 = a.check_relationships_by_id(temp_node1_id, temp_node2_id, type_of_relationship)
        #print(temp003)

        if (temp003 == -1):
            a.create_relationship_by_id(temp_node1_id, temp_node2_id, type_of_relationship, edge_input_dictionary)
        elif (temp003 == -2):
            print("unkown relationship error")
            print(node1_name, node1_domain, node2_name, node2_domain)
            continue
        if (relationship_cnt == 10000):
            relationship_cnt = 0
            print(line_cnt * 10000)
            line_cnt += 1
    f.close()










def output_csv(node_list=[]):
    global a
    print(node_list)
    start_node_id = 0
    end_node_id = 0
    temp003 = 0
    cnt001 = 1
    for i, node_a in enumerate(node_list):
        for j, node_b in enumerate(node_list):
            if (i >= j): continue
            print("i = " + str(i) + " and j = " + str(j))
            print("i = " + node_a + " and j = " + node_b)
            start_node_id = 0
            end_node_id = 0
            search_temp = 0
            search_temp = a.nodes.get(node_a,-1)
            if (search_temp != -1): start_node_id = search_temp
            else:
                start_node_id = a.node_id(node_a)
                if(start_node_id == -1):
                    print("start_node_id 찾을 수 없음 : "+node_a)
                    break
                    #for __ to change i exit j
            search_temp = 0
            search_temp = a.nodes.get(node_b, -1)
            if (search_temp != -1): end_node_id = search_temp
            else :
                end_node_id = a.node_id(node_b)
                if (end_node_id == -1):
                    print("end_node_id 찾을 수 없음 : " + node_b)
                    continue
            temp003 = a.check_relationships_by_id(start_node_id, end_node_id)
            #print(temp003)
            if(temp003 == -1):
                a.create_relationship_by_id(start_node_id,end_node_id,"test",{'cnt':1})
                # cnt001 += 1
                # if(cnt001 >= 10):
                #     driver.close()
                #     sys.exit(1)
            else:
                a.update_relationships_cnt_by_id(start_node_id,end_node_id,temp003)
                #print(temp003)
            #out.write(node_a + "," + node_b + ",,PTC_occurrence\n")
def count_bioconcept(bioconcept_location = "//1TB//FTP_DATA//PubTatorCentral//bioconcepts2pubtatorcentral"):
    template = ""
    new_line = list()
    document_number = ""
    bioconcept = ""
    #out.write(':START_ID,:END_ID,year:int,:TYPE\n')
    # 'C://Users//sonic//Desktop//PubtatorCentral//bioconcepts2pubtatorcentral//bioconcepts2pubtatorcentral'
    with open(bioconcept_location, 'r', encoding='utf-8-sig') as f:
        while True:
            line = f.readline()
            bioconcept = ""
            if not line: break
            # print(line)
            try:
                if (line.split(',')[2].isdigit() == True):
                    if (line.split(',')[1] == "Species"):
                        bioconcept = "NCBI:TAXID:" + line.split(',')[2]
                    elif (line.split(',')[1] == "Gene"):
                        bioconcept = "GeneID:" + line.split(',')[2]
                    else:
                        print("digit error !!")
                else:
                    bioconcept = line.split(',')[2]
            except:
                print(line)
                print("file error")
                continue
                # os.system('Pause')

            if template == line.split(',')[0]:
                # 같은 문서
                new_line.append(bioconcept)
                # print(new_line)
            else:
                # 다른 문서
                if (template == ""):
                    template = line.split(',')[0]
                    new_line.append(bioconcept)
                else:
                    document_number = template
                    output_csv(new_line)
                    # for i,node in enumerate(new_line):
                    #     print(str(i) + "  :  " + node)

                    template = line.split(',')[0]
                    # print('new document')
                    new_line.clear()
                    document_number = ""
                    new_line.append(bioconcept)

                    # print(line.split(',')[0])
                    # print(line.split(',')[2])
                    # new_line.append(line.split(',')[0])
                    # print(new_line)

    # edge.to_csv('C://Users//sonic//Desktop//edge.csv', index=False)
    f.close()

def express_js(data= {'msg':"Hi!!!"}):
    #url = "http://localhost:3000"
    url = "http://192.168.0.82:3000"
    headers = {'Content-type':'application/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)

    for i in data.keys():
        for j,a in enumerate(data[i]):
            for k in a.keys():
                if("\"" in str(data[i][j][k])):
                    #print(data[i][j][k])
                    data[i][j][k] = data[i][j][k].replace("\"","_")
    r1 = requests.post(url, data = json.dumps(data), headers = headers)

    print(json.dumps(data))
    #headers = {'Content-type':'applications/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)


    return
def php_dump(data= {'msg':"Hi!!!"}):

    for i in data.keys():
        for j,a in enumerate(data[i]):
            for k in a.keys():
                if("\"" in str(data[i][j][k])):
                    #print(data[i][j][k])
                    data[i][j][k] = data[i][j][k].replace("\"","_")

    print(json.dumps(data))
    #headers = {'Content-type':'applications/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)

def lionLBDValidation(bioconcept_ID="PR:000003035",bioconcept_Domain="Gene"):
    import cx_Oracle as oci
    Oracle_url = "192.168.0.132"
    conn = oci.connect('neo4j/neo1234@192.168.0.132:1521/graph')

    #f = open("/home/yonsei/PycharmProjects/GraphDB/Pop_up/Chemical_Pop_up/chemical_popup_merge2","r")
    f = open("/home/yonsei/PycharmProjects/GraphDB/Pop_up/Disease/disease_popup","r")
    temp = f.readline()
    print(temp)
    lines = f.readlines()
    test_data = []
    for i in lines:
        test_data.append(i.split("@#$")[0])
    f.close()
    test_out = open("./test_out.text","w")
    # b = Nodes_Noe4j()
    for i in test_data:
#        if(i != "TAXID:487"): continue
        # b.__init__()
        bioconcept_ID = i
        LBDbioconcept_ID = bioconcept_ID
        if("TAXID:" in bioconcept_ID):
            #some virus appears as speceis in disease db
            LBDbioconcept_ID = "NCBITaxon:"+bioconcept_ID.split(':')[1]
            bioconcept_Domain = "Species"
        else:
            bioconcept_Domain = "Disease"
        Neighbor_Base_URL = 'http://lbd.lionproject.net/neighbours/'
        URL = Neighbor_Base_URL + LBDbioconcept_ID
        response = requests.get(URL)
        if(response.status_code != 200):
            print(LBDbioconcept_ID,"Request Error!!")
            continue
        data = response.json()
        path = "./Disease_Lion_LBD/" + str(bioconcept_ID)+".json"
        with open(path,"w") as json_file:
            json.dump(data, json_file)
        # lion_nodes = data["nodes"]
        #
        #
        # arg = str("Lion 4 "+bioconcept_ID+" "+bioconcept_Domain+" 1980 2000").split(" ")
        # b.conditional_start(arg)
        #
        # results_nodes = b.data['nodes']
        # if(results_nodes == 0):
        #     #Starting node without connecting edge
        #     continue
        # found_cnt = 0
        #
        #
        # # print(conn.version)
        # cursor = conn.cursor()
        # # self.lable_web_dictionary = {"Query": 1, "Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6,
        # #                              "CellLine": 7,
        # #                              "Hallmark": 8}
        #
        # excluded_node_cnt = 0
        # filtered_lion_nodes = []
        # for i in lion_nodes:
        #     if("HOC" in i['id']) :
        #         excluded_node_cnt = excluded_node_cnt + 1
        #         continue
        #     if("NCBITaxon:" in i['id']):
        #         i['id'] = "TAXID:"+i['id'].split(':')[1]
        #     # if("CHEBI:" in i['id']):
        #     #     excluded_node_cnt = excluded_node_cnt + 1
        #     #     continue
        #     if("PR:" in i['id']):
        #         excluded_node_cnt = excluded_node_cnt + 1
        #         continue
        #         query_ID_temp = ""
        #         query_ID_temp = query_ID_temp + "PROID = \'" + i['id'] +"\'"
        #         # print('select PROID, DEFINITION from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
        #         cursor.execute('select PROID, GENEID from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
        #         for k in cursor.fetchall():
        #             print(k[1])
        #     filtered_lion_nodes.append(i)
        # total_lion_nodes = len(filtered_lion_nodes)
        # total_results_nodes = len(results_nodes)
        # found_check = False
        # for i in filtered_lion_nodes:
        #     found_check = False
        #     for j in results_nodes:
        #         if(i['id'] == j['cd']):
        #             found_cnt = found_cnt + 1
        #             found_check = True
        #             break
        #     if(found_check == False):
        #         print(i['id'],i['name']," not found !")
        # found_percent = found_cnt/total_lion_nodes*100
        # temp = i['id']+","+str(i['name'])+","+str(total_lion_nodes)+","+str(total_results_nodes)+","+str(found_cnt)+","+str(found_percent)
        print(i)
        test_out.write(i)
        test_out.write("\n")
    # cursor.close()
    conn.close()
    test_out.close()

if __name__ == '__main__':

    start_time = time.time()


    InputFilePath = "C:\\Users\\seomyungwon\\Desktop\\Upload_test\\"


    # Neo4j upload setting

    a = Nodes_Noe4j()

    ## Input Nodes -##

    #[Disease]
    node_input_Disease_ChEMBL()
    node_input_Disease_DisGeNET()
    node_input_Disease_CTD()

    #[Protein]
    node_input_Protein_TTD()
    node_input_Protein_Uniprot()
    node_input_Protein_BindingDB()
    node_input_Protein_ChEMBL

    #[Species]
    node_input_Species_KEGG()
    node_input_Species_NPASS()
    node_input_Species_KNApSAcK()
    node_input_Species_Uniprot()
    node_input_Species_COCONUT()

    #[Bioactivity]
    node_input_Bioactivity_KNApSAcK()

    #[Compound]
    node_input_Compound_ChEMBL()

    #[Functional Food]
    node_input_FunctionalFood_COCONUT()

    ##- Input Links -##

    link_input_Disease_Pathway_Protein_TTD(InputFilePath)
    link_input_Protein_Species_ChEMBL(InputFilePath)
    link_input_Protein_Species_Uniprot(InputFilePath)
    link_input_Species_Bioactivity_KNApSAcK(InputFilePath)
    link_input_Protein_EC50_Compound_BindingDB_ChEMBL(InputFilePath)
    link_input_Protein_IC50_Compound_BindingDB_ChEMBL(InputFilePath)
    link_input_Protein_Kd_Compound_BindingDB_ChEMBL(InputFilePath)
    link_input_Protein_Ki_Compound_BindingDB_ChEMBL(InputFilePath)
    link_input_Disease_Compound_ChEMBL(InputFilePath)
    link_input_Species_Compound_NPASS(InputFilePath)
    link_input_Species_Pathway_Compound_KNApSAcK(InputFilePath)
    link_input_Species_FunctionalFood_COCONUT(InputFilePath)


    #for Input in InputFileList:
    #    edge_input_New(PMN_FilePath, Input)


    #a.load_all_nodes()
    #edge_year_input_node_loaded("./pmid_results_NoneGene_NonGene.csv")
    #edge_year_input_node_loaded_sql_print("/12TB/200211/upload_run/edge_pro_2020.tsv")
    #node_input('/home/yonsei/PycharmProjects/GraphDB/Pop_up/Chemical/chebi_chemical_node.scv')
    #arg = sys.argv
    #arg = '/var/www/cgi-bin/LionDB_Bolts_Class.py 1 PR:000016558 Gene 1980 2020'.split(" ")
    # #disease_hierarchy()
    # if(len(arg) < 5):
    #     arg = "Class.py 2 MESH:D001241 Chemical MESH:D010146 Disease 1980 2020".split(" ")
        # arg = "Class.py 4 MESH:D056684 Disease 1980 2020 ".split(" ")
        # arg = "Lion 1 MESH:D001241 Chemical 1980 2000".split(" ")
    #a.conditional_start(arg)

    #edge_year_input("/3TB/test/191231/pmid_result_Gene_filtered_pro_191230.psv")

    #a.load_all_nodes()
    #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

    #print(a.open_discovery())

    #(target_label_type = "Gene", target_id = "PR:000003035")
    #express_js(a.data)


    #a.load_all_nodes()
    #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

    #print(a.open_discovery())


    #edge_input_domain_fix('./pro_ncbi_edge.csv')
    # edge_year_input("/3TB/test/191230/pmid_result_Gene_filtered_pro_191230.csv")
    #edge_year_input_node_loaded("./pmid_results_sorted_2020_cnt3.csv")

    #print("Query Working Time: {} sec".format(end_time - start_time))
    #a.close_discovery(start_target_label_type="Chemical", start_target_id="MESH:D016685", end_target_label_type="Cellline", end_target_id="CVCL_0023")


    driver.close()