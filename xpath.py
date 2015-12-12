# -*- coding: utf-8 -*-

#Modulo para empregar XPath en Python

import re

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
	labels = re.findall("<([^>]*)>",doc_string)
	
	dic = {}
	
	for n in range(len(labels)):
		if labels[n][0] == "/":
			if [labels[n-1]] in dic.values():
				dic[labels[n-1]] = labels[n]
		else:
			dic[labels[n]] = 0
		
	
	return dic

	
print xml2dic("proba.xml")