# -*- coding: utf-8 -*-

#Modulo para empregar XPath en Python

from re import findall

def simple_check_xml(doc):
	doc_string = open(doc,"r").read()
	open_label = False
	for c in doc_string:
		if c == "<":
			if open_label: return False
			open_label = True
		elif c == ">":
			if not open_label: return False
			open_label = False
	return True
			
def xml2dic(doc):
	if not simple_check_xml(doc): return False
	doc_string = open(doc,"r").read()
	doc_string = doc_string.replace("\n","").replace("\t","")
	elements = findall("<([^>/]*)>([^</]*)|<([^>]*)>",doc_string)
	
	xml_tags = [[e[2]+e[0],e[1]] for e in elements]
	
	xml_elements = []
	
	pais = []
	
	for e in xml_tags:
		elemento = e[0].split(" ")[0]
		atributos = e[0].split(" ")[1:]
		dict_atributos = {}
		for a in atributos:
			dict_atributos[a.split("=")[0]] = a.split("=")[1] 
		
		if elemento[0] != "/":
			xml_elements.append({"element":elemento,"atributes":dict_atributos,
								"value":e[1],"parent":pais[:]})
		
		if elemento[0] == "/":
			pais.remove(elemento[1:])
		else:
			pais.append(elemento)
			
	#for e in xml_elements:
	#	print e
	
	for e in xml_elements:
		print {"element":e["element"]}
		if e["parent"]: print "\t", {"parents":e["parent"]}
		if e["atributes"]: print "\t", {"atributes":e["atributes"]}
		if e["value"]: print "\t", {"value":e["value"]}
	
	return None

	
xml2dic("proba.xml")