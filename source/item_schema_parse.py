import vdf

item_schema = vdf.load(open('item_schema.txt'))

num_items = 0
for item_id in item_schema['items_game']['items']:
	if "default" not in item_id:
		if "default_item" not in item_schema['items_game']['items'][item_id]['prefab']:
			num_items+=1
			with open("items.txt", "a") as myfile:
				myfile.write(item_schema['items_game']['items'][item_id]['name'] + '\n')
print "Parsed", num_items, "items"