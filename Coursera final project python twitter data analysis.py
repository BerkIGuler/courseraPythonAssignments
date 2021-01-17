
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
# lists of words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())
            
            
def strip_punctuation(Str):
    for char in punctuation_chars:
        Str = Str.replace(char, '')
    return Str 

def get_neg(Str):
    count_neg = 0
    new_Str = Str.split()
    for word in new_Str:
        word = strip_punctuation(word)
        if word.lower() in negative_words:
            count_neg += 1
    return count_neg 

def get_pos(Str):
    count_pos = 0
    new_Str = Str.split()
    for word in new_Str:
        word = strip_punctuation(word)
        if word.lower() in positive_words:
            count_pos += 1
    return count_pos 

infile = open("project_twitter_data.csv", 'r')
outfile = open("resulting_data.csv", 'w')
in_data = infile.readlines()
outfile.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n")
for line in in_data[1:]:
    line = line.rstrip().split(',')
    text = line[0]
    num_rt = line[1]
    num_rp = line[2]
    pos_score = get_pos(text)
    neg_score = get_neg(text)
    net_score = pos_score - neg_score
    outfile.write("{},{},{},{},{}".format(num_rt, num_rp, pos_score, neg_score, net_score))
    outfile.write("\n")
                                         
outfile.close()
infile.close()      
                                         