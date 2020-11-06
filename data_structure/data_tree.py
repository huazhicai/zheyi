# -*- coding=utf-8 -*-

from data_structure.data_store import DataDict, DataList, DataValue
from data_structure import special_rules
from datetime import datetime

KEY_PATH_DELIMITER = '.'
LAST_INDEX = -1

class DataTree(object):
	def __init__(self, meta):
		self.meta = meta
		self.group_id = 0
		self.store = DataDict(None)

	def new_group(self):
		self.group_id += 1
		return self.group_id

	def push_source_group(self, source_group):
		pass

	def push_source(self, source, value, group_path, priority=0, data=None, date_path=None):
		nodes = self.meta.get_node_by_source(source)
		if not nodes:
			# print(source, nodes)
			pass 
			# raise ValueError('unexpected source {}'.format(source))
		if nodes:	
			for node in nodes:
				node_meta = self.meta.get_node_meta(node)
				key_path = node_meta.get_key_path()
				special_rule = node_meta.get_special_rule(source)
				if special_rule:
					getattr(special_rules, special_rule)(self, key_path, DataValue(value, priority), group_path, data, date_path)
				else:
					self.set_value(key_path, DataValue(value, priority), group_path)

	def push_group(self, data, priority_key=None, priority=0):
		def recursion_push(_data, group_path, new_group, data_path, priority=priority):
			if isinstance(_data, dict):
				if new_group:
					group_path = group_path + [self.new_group()]
				if _data.get(priority_key):
					time_str = _data.get(priority_key)
					time_str = time_str[:16]
					priority = datetime.strptime(time_str, '%Y-%m-%d %H:%M').timestamp()
					# try:
					# 	priority = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').timestamp()
					# except Exception as e:
					# 	priority = datetime.strptime(time_str, '%Y-%m-%d %H:%M').timestamp()
				for key, value in _data.items():
					if isinstance(key, int):
						self.push_source(key, value, group_path, priority, data, data_path + [key])
					else:
						recursion_push(value, group_path, False, data_path + [key])
			elif isinstance(_data, list):
				for index, item in enumerate(_data):
					recursion_push(item, group_path, True, data_path + [index])
			else:
				pass 
				# raise Exception('error')
		recursion_push(data, [], False, [])

	def _get_list_nodes(self, key_path):
		result = []
		keys = key_path.split(KEY_PATH_DELIMITER)
		for i in range(len(keys), 0, -1):
			path = KEY_PATH_DELIMITER.join(keys[:i])
			node_meta = self.meta.get_node_by_path(path)
			if node_meta and node_meta.is_list():
				result.append(node_meta.node_id)
		return result

	def set_value(self, key_path, value, group_path):
		keys = key_path.split(KEY_PATH_DELIMITER)
		leaf, parents = keys[-1], keys[:-1]

		list_nodes = self._get_list_nodes(key_path)
		if len(list_nodes) >= len(group_path):
			path_header = []
			for i in range(len(list_nodes) - len(group_path)):
				path_header.append(self.new_group())
			group_path = path_header + group_path
		else:
			group_path = group_path[len(group_path) - len(list_nodes):]

		content = self.store
		current_path = []

		group = None
		for key in parents:
			current_path.append(key)
			node_meta = self.meta.get_node_by_path(KEY_PATH_DELIMITER.join(current_path))
			if node_meta.is_list():
				group = group_path.pop(0)

			if key not in content:
				if node_meta.is_list():
					content[key] = DataList([DataDict(group)])
					content = content[key][LAST_INDEX]
				else:
					content[key] = DataDict(group)
					content = content[key]
			else:
				if node_meta.is_list():
					assert isinstance(content[key], DataList)
					for data_dict in content[key]:
						if data_dict.get_group() == group:
							content = data_dict
							break
					else:
						content[key].append(DataDict(group))
						content = content[key][LAST_INDEX]
				else:
					assert isinstance(content[key], DataDict)
					content = content[key]
		assert isinstance(content, DataDict)
		if leaf in content:
			value = merge_value(content[leaf], value)
		content[leaf] = value

	def merge(self, other_tree):
		assert self.meta == other_tree.meta
		merge(self.store, other_tree.store, [], self.meta)

	def normalize(self):
		normalize(self.store, [], self.meta)

	def export(self):
		return self.store.export()

def normalize_dict(store, current_path, meta):
	assert isinstance(store, DataDict)
	for key, value in store.items():
		normalize(value, current_path + [key], meta)

def normalize_list(store, current_path, meta):
	assert isinstance(store, DataList)
	node_meta = meta.get_node_by_path(KEY_PATH_DELIMITER.join(current_path))
	unique_key = node_meta.get_unique_child_key()
	if unique_key:
		unique_key_meta = meta.get_node_meta(unique_key)
		unique_key = unique_key_meta.get_key()
		unique_table = {}
		new_store = DataList()
		for data in store:
			unique_value = data.get(unique_key)
			if unique_value not in unique_table:
				unique_table[unique_value] = data
				new_store.append(data)
			else:
				merge_dict(unique_table[unique_value], data, current_path , meta)
		store[:] = new_store
		for item in store:
			normalize_dict(item, current_path, meta)

	order_key = node_meta.get_order_key()
	if order_key:
		order_key_meta = meta.get_node_meta(unique_key)
		order_key = order_key_meta.get_key()
		store.sort(key=lambda x:x.get(order_key))


def normalize_value(store):
	assert isinstance(store, DataValue)
	store.normalize()

def normalize(store, current_path, meta):
	if not current_path:
		normalize_dict(store, current_path, meta)
		return

	node_meta = meta.get_node_by_path('.'.join(current_path))
	if node_meta.is_parent():
		if node_meta.is_list():
			normalize_list(store, current_path, meta)
		else:
			normalize_dict(store, current_path, meta)
	else:
		normalize_value(store)

def merge_dict(store1, store2, current_path, meta):
	assert isinstance(store1, DataDict)
	assert isinstance(store2, DataDict)
	for key, value in store2.items():
		store1[key] = merge(store1.get(key), value, current_path + [key], meta)
	return store1

def merge_list(store1, store2):
	assert isinstance(store1, DataList)
	assert isinstance(store2, DataList)
	return DataList(store1 + store2)

def merge_value(store1, store2):
	assert isinstance(store1, DataValue)
	assert isinstance(store2, DataValue)
	return store2 if store2.priority > store1.priority else store1

def merge(store1, store2, current_path, meta):
	if store1 is None or store2 is None:
		return store1 or store2

	if not current_path:
		return merge_dict(store1, store2, current_path, meta)

	node_meta = meta.get_node_by_path(KEY_PATH_DELIMITER.join(current_path))
	if node_meta.is_parent():
		if node_meta.is_list():
			return merge_list(store1, store2)
		else:
			return merge_dict(store1, store2, current_path, meta)
	else:
		return merge_value(store1, store2)


def new_data_tree(config):
	from meta_info import TreeMetaInfo
	meta = TreeMetaInfo()
	meta.init(config)
	return DataTree(meta)
