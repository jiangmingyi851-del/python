target=input().lower().strip()
article=' '+input().lower()+' '
words=article.split()
if target not in words:
    print("-1")
else:
    counts=words.count(target)
    position=article.find(' '+target+' ')
    print(counts,position)
