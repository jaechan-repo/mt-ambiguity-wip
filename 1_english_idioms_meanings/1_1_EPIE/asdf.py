import pandas as pd
df1 = pd.read_csv('idiom_meanings.csv')
df2 = pd.read_csv('EPIE.csv') 

df2 = pd.concat([
    df2.groupby('idiom')['example'].apply(list),
    df2.groupby('idiom')['tag'].apply(list)
], axis=1, join='inner').reset_index()

def func(row):
    def argmax(seq):
        m = max(seq, key=len)
        return seq.index(m)
    i = argmax(row['example'])
    row['example'] = row['example'][i]
    row['tag'] = row['tag'][i]
    return row

df2 = df2.apply(func, axis=1)

df = pd.concat([
    df2.set_index('idiom'), df1.set_index('idiom')
], axis=1).reset_index()[['idiom', 'meaning', 'example', 'tag']]
df.to_csv('idioms.csv', index=False)
