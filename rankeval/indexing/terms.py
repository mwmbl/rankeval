"""
Identify terms we need in the index to evaluate ranking.
"""
from html import unescape

import pandas as pd

from rankeval.paths import RANKINGS_DATASET_TRAIN_PATH


pd.options.display.width = 0


# Taken from https://gist.github.com/sebleier/554280?permalink_comment_id=3525942#gistcomment-3525942
STOPWORDS = "0,1,2,3,4,5,6,7,8,9,a,A,about,above,across,after,again,against,all,almost,alone,along,already,also," \
            "although,always,am,among,an,and,another,any,anyone,anything,anywhere,are,aren't,around,as,at,b,B,back," \
            "be,became,because,become,becomes,been,before,behind,being,below,between,both,but,by,c,C,can,cannot,can't," \
            "could,couldn't,d,D,did,didn't,do,does,doesn't,doing,done,don't,down,during,e,E,each,either,enough,even," \
            "ever,every,everyone,everything,everywhere,f,F,few,find,first,for,four,from,full,further,g,G,get,give,go," \
            "h,H,had,hadn't,has,hasn't,have,haven't,having,he,he'd,he'll,her,here,here's,hers,herself,he's,him," \
            "himself,his,how,however,how's,i,I,i'd,if,i'll,i'm,in,interest,into,is,isn't,it,it's,its,itself,i've," \
            "j,J,k,K,keep,l,L,last,least,less,let's,m,M,made,many,may,me,might,more,most,mostly,much,must,mustn't," \
            "my,myself,n,N,never,next,no,nobody,noone,nor,not,nothing,now,nowhere,o,O,of,off,often,on,once,one,only," \
            "or,other,others,ought,our,ours,ourselves,out,over,own,p,P,part,per,perhaps,put,q,Q,r,R,rather,s,S,same," \
            "see,seem,seemed,seeming,seems,several,shan't,she,she'd,she'll,she's,should,shouldn't,show,side,since,so," \
            "some,someone,something,somewhere,still,such,t,T,take,than,that,that's,the,their,theirs,them,themselves," \
            "then,there,therefore,there's,these,they,they'd,they'll,they're,they've,this,those,though,three,through," \
            "thus,to,together,too,toward,two,u,U,under,until,up,upon,us,v,V,very,w,W,was,wasn't,we,we'd,we'll,well," \
            "we're,were,weren't,we've,what,what's,when,when's,where,where's,whether,which,while,who,whole,whom,who's," \
            "whose,why,why's,will,with,within,without,won't,would,wouldn't,x,X,y,Y,yet,you,you'd,you'll,your,you're," \
            "yours,yourself,yourselves,you've,z,Z".split(',')


def run():
    dataset = pd.read_csv(RANKINGS_DATASET_TRAIN_PATH)
    queries = dataset['query'].unique().tolist()
    unescaped = [unescape(x) for x in queries]
    tokens = set()
    stopword_set = set(STOPWORDS)
    for query in unescaped:
        query_tokens = query.replace('.', ' ').lower().split()
        tokens.update(query_tokens)
    print("Tokens", tokens)
    print("Num tokens", len(tokens))
    cleaned = tokens - stopword_set
    print("Cleaned", len(cleaned))


if __name__ == '__main__':
    run()
