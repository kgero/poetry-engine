from features import get_features
from scraper import scraper
from clustering import get_data, cluster

# scraper.download_poems('erika-meitner')

data = get_data.apply('poems')
data = get_data.normalize_features(data)


data = cluster.get_weights(data, data[0])
for item in data:
	print(item['title'])
	print(item['poet'], '\t', end="")
	print("%.2f" % item['weight'], '\t', end="")