# -*- coding: utf-8 -*-

#Modulo para empregar XPath en Python

from sys import argv
from re import findall

if len(argv) > 1:
	arg_doc = argv[1]
	if not findall("\.xml$",arg_doc):
		arg_doc += ".xml"

class element():
	def __init__(self,id,name,value,attributes,parents):
		self.id = id
		self.name = name
		self.value = value
		self.attributes = attributes
		self.parents = parents

def simple_check_xml(doc):
	doc_string = open(doc,"r").read()
	open_label = False
	for char in doc_string:
		if char == "<":
			if open_label: return False
			open_label = True
		elif char == ">":
			if not open_label: return False
			open_label = False
	return True
	
def xml2element_list(doc):
	ID_element = 0
	doc_string = open(doc,"r").read()
	doc_string = doc_string.replace("\n","").replace("\t","")
	string_elements = findall("<([^>/]*)>([^</]*)|<([^>]*)>",doc_string)
	string_elements = [[e[2]+e[0],e[1]] for e in string_elements]
	xml_elements = []
	parents = []
	for e in string_elements:
		elemento = e[0].split(" ")[0].strip()
		if elemento[0:4] != "?xml":
			atributos = e[0].split(" ")[1:]
			dict_atributos = {}
			for a in atributos:
				dict_atributos[a.split("=")[0]] = findall('".+"',a.split("=")[1]) 
			if elemento[0] != "/":
				xml_elements.append(element(ID_element,elemento,
									" ".join(e[1].strip().split()) if e[1] else {},
									dict_atributos,parents[:]))
			if elemento[0] == "/":
				parents.remove(parents[-1])
			else:
				parents.append(ID_element)
				ID_element += 1
	return xml_elements
	
def show_xml2element_list(doc):
	element_list = xml2element_list(doc)
	for e in element_list:
		print ("\t"*len(e.parents)+"id:"+str(e.id)+" <"+
				e.name+((" "+str(e.attributes)+" ") if e.attributes else "")+
				((" (parents: "+str(e.parents)+")") if e.parents else "")+"> "+
				(("'"+str(e.value)+"'") if e.value else ""))
	
def element_list2dict(element_list):
	dict_xml = {}
	for e in sorted(element_list,key=lambda x: len(x.parents)):
		if not e.parents:
			dict_xml[e.id] = {"name":e.name,"value":e.value,
							"attributes":e.attributes}
		else:
			editable_element = dict_xml
			for i in e.parents:
				editable_element = editable_element[i]["value"]
			editable_element[e.id] = {"name":e.name,"value":e.value,
							"attributes":e.attributes}
	return dict_xml
			
def xml2dict(doc):
	xml_elements = xml2element_list(doc)
	return element_list2dict(xml_elements)
	
def xpath_xmldict(query,xmldict):
	try:
		chopped_query = [x.split("/") for x in query.split("//")]
		resultado = xmldict
		ID = 0
		for section in chopped_query:
			for word in section:
				if word:
					if resultado[ID]["name"] == word:
						resultado = resultado[ID]["value"]
						ID += 1
			return resultado
	except:
		return None
		
if len(argv) > 1:
	show_xml2element_list(arg_doc)
	dict = xml2dict(arg_doc)
	#for a in xpath_xmldict("/root/execucion",dict).values():
	#	print a

#print xpath_xmldict("/root/escritores",xml2dict("doc_xml_01.xml"))