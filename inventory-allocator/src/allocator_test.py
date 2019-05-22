from allocator import InventoryAllocator
import unittest


class TestInventoryAllocator(unittest.TestCase):

	def test_no_input(self):
		inventory_allocator = InventoryAllocator()
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Empty order and empty store should return empty solution')

	def test_empty_order(self):
		order = {}
		store = [{'name':'a', 'inventory': {'apple': 5, 'orange': 5, 'banana': 5}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Empty order should return empty solution')

	def test_empty_warehouse(self):
		order = {'apple': 2, 'orange': 5}
		store = []
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Empty warehouse should return empty solution')

	def test_order_not_in_inventory(self):
		order = {'apple': 10}
		store = [{'name':'a', 'inventory': {'beef': 10}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Return empty solution if cant fulfill order')

		order = {'apple': 10, 'carrot': 1}
		store = [{'name':'a', 'inventory': {'apple': 10, 'beef': 10}},
				 {'name':'b', 'inventory': {'apple': 10, 'onion': 10}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Return empty solution if cant fulfill order')

	def test_exact_match(self):
		order = {'apple': 2}
		store = [{'name':'a', 'inventory': {'apple': 2}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [{'a': {'apple': 2}}], 'Exact match between order and store')

		order = {'apple': 2, 'orange': 5, 'beef': 1}
		store = [{'name':'a', 'inventory': {'apple': 2, 'orange': 5, 'beef': 1}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [{'a': {'apple': 2, 'orange': 5, 'beef': 1}}], 'Exact match between order and store')

	def test_inventory_split(self):
		order = {'apple': 10} 
		store = [{ 'name': 'a', 'inventory': { 'apple': 5 }}, 
				 {  'name': 'b', 'inventory': { 'apple': 5 }}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		correct_solution = [{ 'a': { 'apple': 5 }}, { 'b': { 'apple': 5 } }]
		self.assertEqual(solution, correct_solution, 'Incorrect solution, got ' + str(solution) + '; Should be ' + str(correct_solution))

		order = {'bear': 3, 'beets': 5, 'battlestar': 1, 'galatica': 2} 
		store = [{ 'name': 'a', 'inventory': { 'bear': 2, 'galatica': 1 }}, 
				 { 'name': 'b', 'inventory': { 'beets': 5, 'battlestar': 1 }},
				 { 'name': 'c', 'inventory': { 'bear': 5, 'galatica': 1 }}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		correct_solution = [{ 'a': { 'bear': 2, 'galatica': 1 }}, 
							{ 'b': { 'beets': 5, 'battlestar': 1 }},
							{ 'c': { 'bear': 1, 'galatica': 1 }}]
		self.assertEqual(solution, correct_solution, 'Incorrect solution, got ' + str(solution) + '; Should be ' + str(correct_solution))

	def test_leftover(self):
		order = {'apple': 2}
		store = [{'name':'a', 'inventory': {'apple': 10}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [{'a': {'apple': 2}}], 'Incorrect solution, got ' + str(solution))

		order = {'apple': 2}
		store = [{'name':'a', 'inventory': {'beets': 10, 'broccoli': 2, 'apple': 2}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [{'a': {'apple': 2}}], 'Incorrect solution, got ' + str(solution))

	def test_not_enough_inventory(self):
		order = {'apple': 10}
		store = [{'name':'a', 'inventory': {'apple': 1}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Return empty solution if cant fulfill order')

		order = {'apple': 10}
		store = [{'name':'a', 'inventory': {'apple': 5}}, {'name': 'b', 'inventory': {'apple': 4}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Return empty solution if cant fulfill order')

		order = {'apple': 10, 'beets': 5, 'banana': 6}
		store = [{'name': 'a', 'inventory': { 'apple': 1, 'banana' : 3}}, 
				 {'name': 'b', 'inventory': { 'apple': 10, 'beets': 4}},
				 {'name': 'c', 'inventory': { 'banana': 5}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Return empty solution if cant fulfill order')

	def test_negative_count(self):
		order = {'apple': 10}
		store = [{'name':'a', 'inventory': {'apple': -5}}]
		inventory_allocator = InventoryAllocator(order, store)
		self.assertRaises(AssertionError, inventory_allocator.solve)

		order = {'apple': -10}
		store = [{'name':'a', 'inventory': {'apple': 5}}]
		inventory_allocator = InventoryAllocator(order, store)
		self.assertRaises(AssertionError, inventory_allocator.solve)

	def test_type_count(self):
		order = {'apple': 0.01, 'beet': 1.5}
		store = [{'name':'a', 'inventory': {'apple': 100, 'beet': 1}}]
		inventory_allocator = InventoryAllocator(order, store)
		self.assertRaises(AssertionError, inventory_allocator.solve)

	def test_order_with_zero(self):
		order = {'apple': 0}
		store = [{'name':'a', 'inventory': {'apple': 10}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Order with zero does not count')

		order = {'apple': 0, 'bee': 1}
		store = [{'name':'a', 'inventory': {'apple': 10, 'bee': 2}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [{'a': {'bee': 1}}], 'Order with zero does not count')

	def test_warehouse_with_zero(self):
		order = {'apple': 10}
		store = [{'name':'a', 'inventory': {'apple': 0}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Storage with zero does not count')

		order = {'apple': 0}
		store = [{'name':'a', 'inventory': {'apple': 0}}]
		inventory_allocator = InventoryAllocator(order, store)
		solution = inventory_allocator.solve()
		self.assertEqual(solution, [], 'Storage with zero does not count')

unittest.main()