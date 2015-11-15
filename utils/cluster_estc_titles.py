import codecs, sys, os
from difflib import SequenceMatcher as SM	
from collections import defaultdict

def clean_string(s):
	'''Read in a string and return it in cleaned form'''
	return s.lower()

def string_similarity(s1, s2):
	'''Read in two strings and return their difflib similarlity'''
	s1 = clean_string(s1)
	s2 = clean_string(s2)
	return SM(None, s1, s2).ratio() 
	
def cluster_title_rows():
	'''Read in the titles and return a defaultdict from row_number: [cluster_id]'''
	title_clusters = defaultdict()
	cluster_years = defaultdict(list)
	canonical_title = {}

	with codecs.open(sys.argv[1], 'r',' utf-8') as f:
		f = f.read().split("\n")
		titles = []
		cluster_id = 0

		# Retrieve titles
		for r in f[:-1]:
			sr = r.split("\t")
			titles.append( sr[13] )

		# For each title, if it's similar to the following title, add them both to the current cluster
		for i, r in enumerate(f[:-1]):
			if i < len(titles) -1:
				if string_similarity( titles[i], titles[i+1] ) > .95:
					title_clusters[i] = cluster_id
					title_clusters[i+1] = cluster_id

					# Append the current year to array to track number of unique years per cluster
					sr = r.split("\t")
					
					cluster_years[cluster_id].append( sr[1] )
					cluster_years[cluster_id].append( f[i+1].split("\t")[1] )

					# Store a canonical title for the given cluster
					canonical_title[cluster_id] = sr[13]
				else:
					cluster_id += 1
	return title_clusters, cluster_years, canonical_title

def write_clustered_titles():
	'''Read in the original file and for each row write the cluster to which the title belongs (if any)'''
	with codecs.open( ".".join(os.path.basename(sys.argv[1]).split(".")[:-1]) + "_clustered.txt", 'w', 'utf-8') as out:
		with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
			title_clusters, cluster_years, canonical_title = cluster_title_rows()

			f = f.read().replace("\r",'').split("\n")
			for c, r in enumerate(f[:-1]):
				try:
					# Retrieve the cluster id for the current row index
					cluster_id = title_clusters[c]
					unique_years_in_cluster = len(list(set(cluster_years[cluster_id])))
					
					print unique_years_in_cluster, cluster_years[cluster_id], title_clusters[c]
					
					out.write( r + "\t" + str(title_clusters[c]) + "\t" + str(unique_years_in_cluster) + "\t" + canonical_title[cluster_id] + "\n" )
				except KeyError:
					out.write( r + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\n" )		 
				
if __name__ == "__main__":
	write_clustered_titles()	
