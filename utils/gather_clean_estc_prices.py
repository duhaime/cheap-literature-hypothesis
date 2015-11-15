from __future__ import division
import codecs, csv, re

#TODO: identify and handle french prices. geographic lookups to isolate attention to england, france, colonies. 
#discuss price points that depart from ECCO images N25436

'''exchanges:

2 farthings  = 1 halfpenny
4 farthings  = 1 penny (d)
12 pennies   = 1 shilling (s)
5 shillings  = 1 crown
4 crowns     = 1 pound (l)
21 shillings = 1 guinea

'''

def retrieve_monetary_value(money_shorthand):
	if money_shorthand == "d":
		mvalue = 4
	elif money_shorthand == "s":
		mvalue = 48
	elif money_shorthand == "l":
		mvalue = 960
	elif money_shorthand == "g":
		mvalue = 1008
	elif money_shorthand == "h":
		mvalue = 2
	elif money_shorthand == "c":
		mvalue = 240
	elif "guinea" in money_shorthand:
		mvalue = 1008

	return mvalue
	
md = build_metadata_dict()

def build_page_length_dict():
	length_d = {}
	with codecs.open("gather_ecco_page_lengths/pages_by_estc_id_aggregate.txt","r","utf-8") as len_data:
		len_data = len_data.read().replace("\r","").split("\n")
		for row in len_data[:-1]:
			split_row = row.split("\t")
			id              = split_row[0]
			book_length     = split_row[1]
			length_d[id]    = book_length
		return length_d

ld = build_page_length_dict()		
		
def build_metadata_dict():

	bib_d = {}

	with codecs.open("../estc_streamlined_bib_data.tsv","r","utf-8") as bib:
		bib = bib.read().split("\n")
		for row in bib[:-1]:
			split_row  = row.split("\t")
			id         = split_row[0].replace('"',"")
			length     = split_row[11]
			format     = split_row[13]
			year       = split_row[14]			
			
			bib_d[id]           = {}
			bib_d[id]["year"]   = year
			bib_d[id]["format"] = format
			bib_d[id]["length"] = length
			
	return bib_d

def clean_pagination(raw_pagination):
	sans_square = re.sub(r'\[[^]]*\]\s?' , '', raw_pagination)
	if "-" in sans_square:
		cleaner = sans_square.split("-")[-1]
		cleaner = "".join( x for x in cleaner if x.isdigit() )
	else:
		cleaner = "".join( x for x in sans_square if x.isdigit() )
	return cleaner
	
def clean_book_size(unclean_size):
	if "4" in unclean_size:
		return "4"
	elif "8" in unclean_size:
		return "8"
	elif "12" in unclean_size:
		return "12"
	elif "16" in unclean_size:
		return "16"
	elif "24" in unclean_size:
		return "24"
	elif "2" in unclean_size:
		return "2"
	else:
		return "NA"
	
nums                    = {}
nums["half"]            = ".5"
nums["one"]             = "1"
nums["two"]             = "2"
nums["three"]           = "3"
nums["four"]            = "4"
nums["five"]            = "5"
nums["six"]             = "6"
nums["seven"]           = "7"
nums["eight"]           = "8"
nums["nine"]            = "9"
nums["ten"]             = "10"
nums["eleven"]          = "11"
nums["twelve"]          = "12"
nums["thirteen"]        = "13"
nums["fourteen"]        = "14"
nums["fifteen"]         = "15"
nums["sixteen"]         = "16"
nums["seventeen"]       = "17"
nums["eighteen"]        = "18"
nums["nineteen"]        = "19"
nums["twenty"]          = "20"

money                   = {}
money["sh"]             = "s"
money["shil"]           = "s"
money["shill"]          = "s"
money["shillg"]         = "s"
money["shillgs"]        = "s"
money["silling"]        = "s"
money["shilling"]       = "s"
money["shillings"]      = "s"
money["shelings"]       = "s"
money["shellings"]      = "s"
money["pence"]          = "d"
money["pences"]         = "d"
money["penny"]          = "d"
money["penne"]          = "d"
money["peny"]           = "d"
money["guinea"]         = "g"
money["guineas"]        = "g"
money["halfpence"]      = "h"
money["pound"]          = "l"
money["pounds"]         = "l"
money["halfpenny"]      = "h"
money["crown"]          = "c" 
money["twopence"]       = "2 d"
money["threepence"]     = "3 d"
money["fourpence"]      = "4 d"
money["fivepence"]      = "5 d"
money["sixpence"]       = "6 d"
money["sevenpence"]     = "7 d"
money["eightpence"]     = "8 d"
money["ninepence"]      = "9 d"
money["tenpence"]       = "10 d"
money["elevenpence"]    = "11 d"
money["twelvepence"]    = "12 d"
money["thirteenpence"]  = "13 d"
money["fourteenpence"]  = "14 d"
money["fifteenpence"]   = "15 d"
money["sixteenpence"]   = "14 d"
money["seventeenpence"] = "14 d"
money["eighteenpence"]  = "14 d"
money["nineteenpence"]  = "14 d"


good_nums = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
good_money = ["l","s","d"]

failed_conversions = 0

with codecs.open("estc_prices_need_cleaning.txt","w","utf-8") as out:
	with codecs.open("../500exp20141204.csv","r","utf-8") as f:
		for row in csv.reader(f):
			#row is now a list object [0] = ESTC id, [1] = note value

			try:
				row_id     = row[0]
				row_year   = md[row_id]["year"]
			except:
				row_year   = "NA"
				
			try:
				row_format       = "NA"
				row_id           = row[0]
				row_format       = md[row_id]["format"]
				clean_row_format = clean_book_size(row_format)
				
			except:
				row_format = "NA"

			try:
				row_id     = row[0]
				row_length = md[row_id]["length"]
			except:
				row_length = "NA"
				
			try:
				row_id     = row[0]
				row_pages  = ld[row_id]
			except:
				row_pages  = "NA"
				
			if "price" in row[1].lower():
				if "Price from imprint" in row[1]:
					cleaner_price = row[1].split("Price from imprint")[1].replace(":","").split(";")[0].replace("within","").replace("brackets","").replace("square","").replace(" in "," ").replace("(","").replace(")","").replace("[","").replace("]","").strip()
		
					normalized_price = cleaner_price.lower().replace("-"," ").replace(","," ").replace("."," ").split()
					
					cleaner_normalized = []

					for word in normalized_price:
						if word in good_nums:
							cleaner_normalized.append(word)
						elif word in good_money:
							cleaner_normalized.append(word)
						elif word[0] in good_nums:
								if word[-1] in good_money:
									for subword in word:
										cleaner_normalized.append(subword)
						else:			
							retrieved_word = ""
							try:
								retrieved_word = nums[word]
							except:
								try:
									retrieved_word = money[word]
								except:
									pass

							if retrieved_word:
								cleaner_normalized.append(retrieved_word)
								
					##############################
					# Compute Price in Farthings #
					##############################
					
					total_farthings       = 0
					coefficient           = ''
					monetary_value        = 0

					if len(cleaner_normalized) > 4:
						total_farthings = "PRICING_OPTIONS"
					elif ". or " in cleaner_price:
						total_farthings = "PRICING_OPTIONS"
					elif ", or " in cleaner_price:
						total_farthings = "PRICING_OPTIONS"
					elif " or " in cleaner_price.lower():
						total_farthings = "PRICING_OPTIONS"
					
					else:
						try:
						
							for value in cleaner_normalized:
								if len(value) == 1:
									
									try:
										float(value)
										coefficient = float(value)	
									except Exception as excep:
										monetary_value = retrieve_monetary_value(value)

										#print cleaner_normalized, coefficient, monetary_value, total_farthings

										if coefficient:
											if monetary_value:
												total_farthings += float(coefficient) * monetary_value
										
										coefficient    = ''
										monetary_value = 0
								
								elif len(value) == 2:
									#if len(value) == 2, we're looking at compound coefficient, so store it
									coefficient = float(value)
								
								elif len(value) == 3:
									coefficient        = float(value[0])
									dirty_money_value  = value[2]
									monetary_value     = retrieve_monetary_value(dirty_money_value)
									total_farthings   += coefficient * monetary_value
									
								elif len(value) == 4:
									coefficient        = float(value[0] + value[1])
									dirty_money_value  = value[3]
									monetary_value     = retrieve_monetary_value(dirty_money_value)
									total_farthings   += coefficient * monetary_value

						except Exception as exc:
							print exc
									
					if total_farthings == 0:
						failed_conversions += 1
					else:
						try:
							float(total_farthings)
						except:
							failed_conversions += 1
												
					if row_year == "NA":							
						continue
					if clean_row_format == "NA":
						continue
					if row_pages == "NA":
						continue
					if total_farthings == "PRICING_OPTIONS":
						continue
					elif str(total_farthings) == "0":
						continue
					
					out.write(row[0] + "\t" + row_year + "\t" + row_format + "\t" + clean_row_format + "\t" + row_length + "\t" + clean_pagination(row_length) + "\t" + row_pages + "\t" + row[1] + "\t" + cleaner_price + "\t" + " ".join(w for w in cleaner_normalized) + "\t" + str(total_farthings) + "\t" + str( float(total_farthings) / float(row_pages) ) + "\n")

print failed_conversions
