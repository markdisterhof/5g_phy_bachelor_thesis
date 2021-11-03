import re
with open('ascii-art.txt', 'rt') as fin:
    with open("antbin.txt", "wt") as fout:
        for line in fin:
            fout.write(re.sub(pattern=r'[^ ]',repl='1\n', string=line).replace(' ', '0\n'))
with open('ascii-art.txt', 'rt') as fin:
    with open("antbin_aligned.txt", "wt") as fout:
        for line in fin:
            fout.write(re.sub(pattern=r'[^ \n]',repl='1', string=line).replace(' ', '0'))
