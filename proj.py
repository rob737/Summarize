from __future__ import division
import re
  
class SummaryTool(object):
 
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")
 
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")
 
    def sentences_intersection(self, sent1, sent2):
 
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))
 
        if (len(s1) + len(s2)) == 0:
            return 0
 
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)
 
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence
 
    def get_senteces_ranks(self, content,title):
 
        sentences = self.split_content_to_sentences(content)
 
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])
                
 
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
           #use title's relevance as a parameter
            sentences_dic[self.format_sentence(sentences[i])] = score+self.sentences_intersection(sentences[i],title)
        return sentences_dic
 
    def get_best_sentence(self, paragraph, sentences_dic):
 
        sentences = self.split_content_to_sentences(paragraph)
 
        if len(sentences) < 2:
            return ""
 
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s
 
        return best_sentence
 
    def get_summary(self, title, content, sentences_dic):
 
        paragraphs = self.split_content_to_paragraphs(content)
 
        summary = []
        summary.append(title.strip())
        summary.append("")
 
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)
 
        return ("\n").join(summary)
 
 
def main():
 
    title = """
    Akhilesh Yadav tears into Narendra Modi bastion on maiden visit to Gujarat, says third front ready to govern
        """
    content = """
        In his maiden visit to Guajrat, Uttar Pradesh Chief Minister Akhilesh Yadav blamed “some people” from the BJP-ruled state for creating riots in his state.

Apparently hinting at the Muzaffarnagar riots, he said  “some people from here(Gujarat) came to UP and tried to create riots and insult us, but UP has decided that we will stay united and fight these forces. Varanasi will vote for secular people…and it has already proved this by voting in huge numbers in the first phase”.

The BJP prime ministerial candidate Narendra Modi is contesting from Varanasi, apart from Vadodara, which goes to polls on May 11.

“Humne Gujarat main sirf shuruat ki hai, hum apna khaata kholne aaye hain (We have just begun in Gujarat and have come to open our account)”, said Yadav pitching for a third-front at the Centre and his father Mulayam Singh Yadav having a bigger role in it.

“The third front is ready in different states like Tamil Nadu, West Bengal, Odisha and Bihar as these regional parties will win maximum votes in this elections.If there is any one party which is running according to a secular outlook then that is SP,” said Akhilesh.

Calling Modi an “RSS backed PM candidate” Yadav said that a BJP government at the Centre would spoil India’s relations with its neighbours. Interacting with reporters at Sardar Vallabhbhai Patel International Airport in Ahmedabad before heading for Patan, Yadav when asked about the speculation of BJP gaining in UP said, “It was the SP who had once stopped BJP’s march in UP and it will happen again”.

   to help us personalise your reading experience.
According to Yadav, “BJP had grown because of wrong policies of the Congress. Its PM candidate is backed by RSS, VHP and Bajrang Dal. I want to tell you that people of UP will stop him (Modi) from becoming PM.”

About his father and former Defence Minister Mulayam Singh Yadav he said,”There has been no minister who maintained such good links with India’s neighbours as Netaji (Mulayam). BJP will spoil any relations India may have with her neighbours as they are good in breaking up things. Even they did not spare Gandhiji (Mahatma). Look at the history of organisations like VHP and RSS that back the BJP, they are known for disrupting and breaking up things.”

Taking potshots at Modi’s tea vendor roots he said, “Chai ne hamesha gulaam banaya hai” (That cup of tea is the root of all slavery)”.

Speaking to a 2000-odd crowd consisting of Muslims, Thakore and Rabari communities, the SP leader said, “Tea has always made slaves of Indians. Your CM(Modi) is creating a hype out of making people drink tea, tell me which political party does something like this?
        """
 
    st = SummaryTool()
 
    sentences_dic = st.get_senteces_ranks(content,title)
 
    summary = st.get_summary(title, content, sentences_dic)
 
    print summary
 
    print ""
    print "Original Length %s" % (len(title) + len(content))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))
 
 
if __name__ == '__main__':
    main()
