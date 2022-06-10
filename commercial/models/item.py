import models.connection as connection
from models.utils import utils

collection = connection.get_collection("item")

class item():
  def init(business_id):
    if collection.find_one({"business_id": business_id}) is None:
      collection.insert_one({"business_id": business_id})
      return True
    else:
      return False

  def append_category(business_id, name):
    #distinct name
    if collection.find_one({"business_id": business_id, "categories.name": name}) is not None:
      return utils.reply("IE-1", 'error', 'category already exists')
    #follow structure
    #set name as key
    collection.update_one({"business_id": business_id}, {"$push": {"categories": {"name": name}}})
    return utils.reply("IS-1", 'success', 'category added')

  def append_item(business_id, category, data):
    #distinct name
    if collection.find_one({"business_id": business_id, "categories.name": category, "categories.items.name": data["name"]}) is not None:
      return utils.reply("IE-1", 'error', 'item already exists')
    #add item id to data
    data["item_id"] = utils.generate_id()
    #push into category and follow structure
    collection.update_one({"business_id": business_id, "categories.name": category}, {"$push": {"categories.$.items": data}})
    return utils.reply("IS-1", 'success', 'item added')

  def delete_category(business_id, category):
    collection.update_one({"business_id": business_id}, {"$pull": {"categories": category}})
    return utils.reply("IS-1", 'success', 'category deleted')

  def delete_item(business_id, category, item_id):
    collection.update_one({"business_id": business_id, "categories.name": category}, {"$pull": {"categories.$.items": {"item_id": item_id}}})
    return utils.reply("IS-1", 'success', 'item deleted')

  def get_categories(business_id):
    #only return category names
    return [category["name"] for category in collection.find_one({"business_id": business_id})["categories"]]

  def get_items(business_id, category):
    #only return item list
    result = collection.find_one({"business_id": business_id, "categories.name": category})
    #return only items
    result = result["categories"]
    #remove non matching category
    matched = "asd"
    for row in result:
      if row["name"] == category:
        matched = row
    #transform item_id to string
    for item in matched['items']:
      item["item_id"] = str(item["item_id"])
    return matched

  def get_item(business_id, category, item):
    return collection.find_one({"business_id": business_id, "categories.name": category, "categories.items.item_id": item})["categories"][0]["items"][0]

  def update_item(business_id, category, item, data):
    collection.update_one({"business_id": business_id, "categories.name": category, "categories.items.item_id": item}, {"$set": {"categories.$.items.$": data}})
    return utils.reply("IS-1", 'success', 'item updated')

  def update_category(business_id, category, data):
    collection.update_one({"business_id": business_id, "categories.name": category}, {"$set": {"categories.$.name": data}})
    return utils.reply("IS-1", 'success', 'category updated')