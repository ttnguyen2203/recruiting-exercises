

class InventoryAllocator():
	"""
	Class to compute the cheapest way an order can be shipped (shipments) given 
		inventory across a set of warehouses (inventory distribution)

	Attributes:
        order: Dictionary, stores names of item and numbers of each item required
        	key = string, value = integer > 0

        warehouse: List of warehouses sorted by shipment cost, each warehouse has
        	form: {'name': string, 'inventory': Dictionary of items and numbers}

        solution: List of warehouses and corresponding items and counts to for
        	delivery distribution
	    	
	"""

	def __init__(self, order={}, warehouse_list=[]):
		self.order = order
		self.warehouse_list = warehouse_list
		self.solution = []

	def solve(self):
		# No zero in ordered items
		ordered_items = list(self.order.keys())
		for item in ordered_items:
			if self.order[item] == 0:
				del self.order[item]

		for warehouse in self.warehouse_list:
			if not self.order:
				break

			required_items = set(self.order.keys())
			inventory_items = set(warehouse['inventory'].keys())
			overlapping_items = required_items.intersection(inventory_items)
			if not overlapping_items:
				continue
			
			shipment = {}
			inventory = warehouse['inventory']
			for item in overlapping_items:
				if inventory[item] == 0:
					continue
				retrieved_amount = min(inventory[item], self.order[item])

				assert retrieved_amount > 0, 'Item count cannot be negative or zero'
				assert isinstance(retrieved_amount, int), 'Count must be integer'
				
				shipment[item] = retrieved_amount
				self.order[item] -= retrieved_amount

				if self.order[item] == 0:
					del self.order[item]

			self.solution.append({warehouse['name']: shipment})

		if self.order:
			self.solution = []
		
		return self.solution

	def get_solution(self):
		return self.solution
