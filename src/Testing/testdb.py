from cloudant.client import Cloudant
from cloudant.query import Query
import nltk
import token_replacement

#import document

client = Cloudant("1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix","5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638",account="1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix")
client.connect()
my_database = client['amazon_data']

#temp_client = Cloudant("f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix","bfd53fe017adeea40cd4894bb29451ddff6805fc1b94a179eba4de8ef84b632f",account="f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix")
temp_client = Cloudant("fc5dda33-3709-459b-8857-92b93630db31-bluemix","a15d0990d5ebfb2aedd5a61dacdbdb132b6e2266f74a7f46cadfadbc6b982b06",account="fc5dda33-3709-459b-8857-92b93630db31-bluemix")
temp_client.connect()
print temp_client

########ignore
#add check if exists here
#temp_database = temp_client.create_database('testdb2')
#if 'testdb' not in temp_client:
#	temp_database = temp_client.create_database('testdb')
#else:
#	print 'exists'
#for key in temp_client:
#	print key


#temp_database = temp_client['testdb4']
##########

##create
#temp_database = temp_client.create_database('testdb_final_product')

###if exists
temp_database = temp_client['testdb_final_product']

#query = Query(my_database, selector={'asin':"B00BCGRZ04"})
#B0042A8CW2
#query = Query(my_database, selector={'asin':"B0042A8CW2"})
#query = Query(my_database, selector={'asin':'B00BCGRZ04'},fields=["_id"])

#for doc in query.result:
#	print doc
#dddb09bdee0f0ae701af3455b6259cb0


def find_middle(generator):
        sequences = list(generator)
        mid_sentence = len(sequences)/2
        middle_char = sequences[mid_sentence][1]
        middle_char = int(middle_char) + 1
        return middle_char

def split_long_string(text,data):
	print "\n \n text received is \n\n"
	print text
        if len(text) > 3024:
		print "\n split\n"
                sequences = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
                middle = find_middle(sequences)
                second_half = text[middle:].strip()
                first_half = text[:middle].strip()
                #return first_half
		print "\n first half\n"
		print first_half
		print "\n second half\n"
		print second_half
                #data.append([first_half])
                #data.append([second_half])
		print data
                split_long_string(first_half,data)
                split_long_string(second_half,data)
        else:
                return data

query = Query(my_database, selector={'_id':"dddb09bdee0f0ae701af3455b6259cb0"})
for doc in query.result:
	#print doc
	if 'reviewText' in doc:
		text=doc['reviewText']
		data=[]
		data=split_long_string(text,data)
		print data
		#print text
		print "\n"+doc['_id']+"\n"
		####review= token_replacement.token_replacement(text);
		####dict={}
		#specify review id
		####dict['review_id']=doc['_id']
		####dict['review']=review
		####print dict
		##########my_document=temp_database.create_document(dict)

