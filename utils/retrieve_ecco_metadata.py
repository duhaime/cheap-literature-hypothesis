from bs4 import BeautifulSoup
from multiprocessing import Pool
import glob, codecs, sys, json

# path to target: /scratch30/avyushko/ECCO_2of2/GenRef/0080102000/xml

def extract_features(file_path):
    with codecs.open(file_path, 'r', 'latin1') as f:
        f = f.read()

	# Extract the high level genre label from the path to the file
	genre = file_path.split("/")[-4]

	# Retrieve the uniform title from the current record
	try:
		uniform_title = f.split("<uniformTitle>")[1].split("<")[0]
	except IndexError:
		uniform_title = ''

        # Retrieve the ESTC ID for the current work
        estc_id = f.split("<ESTCID>")[1].split("<")[0]

        # Determine the number of libraries that own the current work
        holdings_count = str( len(f.split("<holdings>")) )

        # Find the document type
        document_type = f.split("<documentType>")[1].split("<")[0]

        # Retrieve the document language
        language = f.split("<language>")[1].split("<")[0]

        # Each of the subject fields seems to start with a consistent string (locSubjectHead)
        # Loop over all subject fields and extract the terms within each of those fields
        subject_field_terms = []
        subject_field_start = '<locSubjectHead'
        subject_field_end = '</locSubjectHead>'
        for subject_field in f.split(subject_field_start)[1:]:
            subject_field = subject_field.split(subject_field_end)[0]
            for j in subject_field.split("<locSubject")[1:]:

                field_term = j.split(">")[1].split("<")[0]
                subject_field_terms.append( field_term )

        # Retrieve the author's name
        try:
            author_name = f.split("<author>")[1].split("<marcName>")[1].split("<")[0]
        except IndexError:
            author_name = None

        # Retrieve the author's death date
        try:
            death_date = f.split("<author>")[1].split("<deathDate>")[1].split("<")[0]
        except IndexError:
            death_date = None

        # Retrieve the full title
        full_title = f.split("<fullTitle>")[1].split("<")[0]

	# Retrieve the display title
	display_title = f.split("<displayTitle>")[1].split("<")[0]

	# Retrieve the imprint year
	imprint_year = f.split("<imprintYear>")[1].split("<")[0]

	# Retrieve the shelfmarks as a list
	shelfmark_list = []
	shelfmarks = f.split("<libraryShelfmark>")[1]
	for i in shelfmarks:
		shelfmark_list.append(i.split("<")[0])

        # Find the total number of volumes and current volume
        current_volume = f.split("<currentVolume>")[1].split("<")[0]
        total_volumes = f.split("<totalVolumes>")[1].split("<")[0]

        # Retrieve the publication location
        publication_location = f.split("<imprintCity>")[1].split("<")[0]

        return [estc_id, file_path, genre, uniform_title, \
 	holdings_count, document_type, language, subject_field_terms, \
	author_name, death_date, full_title, len(full_title), \
 	display_title, imprint_year, shelfmark_list, \
 	current_volume, total_volumes, \
        publication_location]

if __name__ == "__main__":
    files = glob.glob(sys.argv[1])
    pool_one = Pool(40)
    results = []

    print "preparing to process", len(files), "files"

    '''
    for c, r in enumerate( pool_one.imap(extract_features, files) ):
        print "processed", c, "files"
        results.append(r)
    '''

    for i in files:
        print i
        results.append( extract_features(i) )   

    with open("derived_metadata.json",'w') as json_file:
        json.dump(results, json_file)

