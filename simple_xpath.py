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
	def __repr__(self):
		return ("element("+str(self.id)+", "+str(self.name)+", "+
				str(self.attributes)+", "+str(self.parents)+")")
	def __str__(self):
		return ("id: "+str(self.id)+", "+
				"name: "+str(self.name)+", "+
				"value: "+str(self.value)+", "+
				"attributes: "+str(self.attributes)+", "+
				"parents: "+str(self.parents))

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
	string_elements = findall("<([^>]*)>([^</]*)|</([^>]*)>",doc_string)
	string_elements = [[e[2]+e[0],e[1]] for e in string_elements]
	xml_elements = []
	parents = []
	for e in string_elements:
		total_e = e[0].split(" ")
		total_e = [ec for ec in total_e if ec]
		elemento = total_e[0]
		if elemento[0:4] != "?xml":
			atributos = total_e[1:]
			atributos = [a for a in atributos if a]
			dict_atributos = {}
			for a in atributos:
				dict_atributos[a.split("=")[0]] = findall('".+"',a.split("=")[1]) 
			if elemento[0] != "/":
				xml_elements.append(element(ID_element,elemento,
									" ".join(e[1].strip().split()) if e[1] else "",
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
		total_resultados = []
		ID = 0
		for section in chopped_query:
			for word in section:
				if word:
					if resultado[ID]["name"] == word:
						ID += 1
		return resultado
	except:
		return None
		
def xpath_xmllist(query,xmllist,all=False):
		chopped_query = query.split("/")
		chopped_query = [[q] for q in chopped_query if q]
		for c in chopped_query:
			if findall("\[(.+)\]",c[0]):
				c.append(int(findall("\[(.+)\]",c[0])[0]))
				c[0] = c[0].split("[")[0]
			else:
				c.append(0)
		xml = xmllist
		dict_ids = {}
		for query in chopped_query[:len(chopped_query)+(all-1)]:
			q,num = query
			dict_ids[q] = []
			for element in xml:
				if element.name == q:
					dict_ids[q].append(element.id)
			if num > 0:
				dict_ids[q] = [dict_ids[q][num]]
		resultado = []
		values_ids = dict_ids.values()
		for element in xml:
			if all:
				verdadeiros = [True for n in range(len(element.parents)) 
									if element.parents[n] in values_ids[n]]
				if len(verdadeiros) > 0:
					resultado.append(element)
			else:
				if len(element.parents) == len(values_ids):
					verdadeiros = [True for n in range(len(values_ids)) 
									if element.parents[n] in values_ids[n]]
					if len(verdadeiros) == len(values_ids):
						resultado.append(element)
		if chopped_query[-1][1]:
			return [resultado[chopped_query[-1][1]]]
		else:
			return resultado
			
def help():
	print u"Funcións:"
	print "\t> simple_check_xml(doc)"
	print "\t> xml2element_list(doc)"
	print "\t> show_xml2element_list(doc)"
	print "\t> element_list2dict(element_list)"
	print "\t> xml2dict(doc)"
	print "\t> xpath_xmldict(query,xmldict)"
	print "\t> xpath_xmllist(query,xmllist)"
	
#if len(argv) > 1:

	#for i in xml2element_list(arg_doc):
	#	print "\t"*len(i.parents)+str(i)
	
	#lista_elementos = xml2element_list(arg_doc)
	#resultado = xpath_xmllist("/root/execucion/script",lista_elementos)