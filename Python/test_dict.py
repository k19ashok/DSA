import unittest
from dictionary import Dict

class TestDict(unittest.TestCase):

    def setUp(self):
        # This method runs before each test
        self.d = Dict()

    # --- Basic Functionality Tests ---

    def test_initial_state(self):
        self.assertEqual(len(self.d), 0)
        self.assertEqual(self.d.max_len, 8)
        self.assertFalse('a' in self.d)
        with self.assertRaises(KeyError):
            _ = self.d['a']

    def test_setitem_and_getitem(self):
        self.d['key1'] = 'value1'
        self.assertEqual(self.d['key1'], 'value1')
        self.assertEqual(len(self.d), 1)

        self.d['key2'] = 'value2'
        self.assertEqual(self.d['key2'], 'value2')
        self.assertEqual(len(self.d), 2)

    def test_update_item(self):
        self.d['key'] = 'initial'
        self.assertEqual(self.d['key'], 'initial')
        self.assertEqual(len(self.d), 1)

        self.d['key'] = 'updated'
        self.assertEqual(self.d['key'], 'updated')
        self.assertEqual(len(self.d), 1) # Size should not change on update

    def test_contains(self):
        self.d['exist'] = 1
        print(self.d.__getitem__('exist'))
        self.assertTrue('exist' in self.d)
        self.assertFalse('non_exist' in self.d)

    def test_get_method(self):
        self.d['present'] = 100
        self.assertEqual(self.d.get('present'), 100)
        self.assertIsNone(self.d.get('absent'))
        self.assertEqual(self.d.get('absent', 'default_val'), 'default_val')

    def test_keys_values_items(self):
        self.d['a'] = 1
        self.d['b'] = 2
        self.d['c'] = 3

        self.assertCountEqual(self.d.keys(), ['a', 'b', 'c'])
        self.assertCountEqual(self.d.values(), [1, 2, 3])
        self.assertCountEqual(self.d.items(), [('a', 1), ('b', 2), ('c', 3)])

    def test_iteration(self):
        self.d['x'] = 10
        self.d['y'] = 20
        self.d['z'] = 30
        iterated_keys = [k for k in self.d]
        self.assertCountEqual(iterated_keys, ['x', 'y', 'z'])

    def test_repr_str(self):
        self.d['one'] = 1
        self.d['two'] = 2
        # The exact string representation might vary due to insertion order
        # So, we check for presence of expected parts
        repr_str = str(self.d)
        self.assertIn("one - 1", repr_str)
        self.assertIn("two - 2", repr_str)

    # --- Deletion and Tombstone Tests ---

    def test_delitem_basic(self):
        self.d['remove_me'] = 'value'
        self.assertEqual(len(self.d), 1)
        del self.d['remove_me']
        self.assertEqual(len(self.d), 0)
        self.assertFalse('remove_me' in self.d)
        with self.assertRaises(KeyError):
            _ = self.d['remove_me']

    def test_delitem_non_existent(self):
        with self.assertRaises(KeyError):
            del self.d['non_existent']

    def test_delitem_with_collision_chain(self):
        # Create keys that are likely to collide or probe
        # These keys might not actually collide in your specific hash/probing logic,
        # but the test demonstrates intent.
        self.d[1] = 'val1' # Assume this goes to slot X
        self.d[9] = 'val9' # Assume this collides with 1 and goes to slot Y (Y > X)
        self.d[17] = 'val17' # Assume this collides with 1, 9 and goes to slot Z (Z > Y)

        self.assertEqual(len(self.d), 3)
        self.assertEqual(self.d[1], 'val1')
        self.assertEqual(self.d[9], 'val9')
        self.assertEqual(self.d[17], 'val17')

        # Delete an item in the middle of a probe chain (e.g., 9)
        del self.d[9]
        self.assertEqual(len(self.d), 2)
        self.assertFalse(9 in self.d)
        self.assertTrue(1 in self.d) # Ensure 1 is still accessible
        self.assertTrue(17 in self.d) # Ensure 17 is still accessible (tombstone helps here)

        # Delete the first item in the chain (e.g., 1)
        del self.d[1]
        self.assertEqual(len(self.d), 1)
        self.assertFalse(1 in self.d)
        self.assertTrue(17 in self.d) # Ensure 17 is still accessible (multiple tombstones)

        self.assertEqual(self.d[17], 'val17')

    def test_keys_values_items_after_deletion(self):
        self.d['a'] = 1
        self.d['b'] = 2
        self.d['c'] = 3
        del self.d['b'] # Delete an item

        self.assertEqual(len(self.d), 2)
        self.assertCountEqual(self.d.keys(), ['a', 'c'])
        self.assertCountEqual(self.d.values(), [1, 3])
        self.assertCountEqual(self.d.items(), [('a', 1), ('c', 3)])
        self.assertCountEqual([k for k in self.d], ['a', 'c']) # Test iteration

    # --- Resizing Tests ---

    def test_resize_on_load_factor(self):
        # Initial max_len = 8, resize at size >= (8 * 2) // 3 = 5
        self.assertEqual(self.d.max_len, 8)

        # Add 4 items (size 4, max_len 8, no resize)
        for i in range(4):
            self.d[f'k{i}'] = i
        self.assertEqual(len(self.d), 4)
        self.assertEqual(self.d.max_len, 8)

        # Add 5th item (size 5, triggers resize)
        self.d['k4'] = 4
        self.assertEqual(len(self.d), 5)
        # Max_len should now be 16 (8 * 2)
        self.assertEqual(self.d.max_len, 16)

        # Verify all items are still present after resize
        for i in range(5):
            self.assertEqual(self.d[f'k{i}'], i)

    def test_resize_cleans_tombstones(self):
        # Fill to trigger resize soon
        for i in range(4):
            self.d[f'k{i}'] = i
        # Now delete some to create tombstones
        del self.d['k0']
        del self.d['k2']
        self.assertEqual(len(self.d), 2) # k0, k2 are logically deleted

        # Add items to force resize, cleaning tombstones
        # Current size 2. Add 3 more to reach 5, triggering resize (max_len 8 -> 16)
        self.d['new_k1'] = 10
        self.d['new_k2'] = 20
        self.d['new_k3'] = 30 # This should trigger resize

        self.assertEqual(len(self.d), 5)
        self.assertEqual(self.d.max_len, 16) # Should have resized

        # Verify only live items are present
        self.assertFalse('k0' in self.d)
        self.assertTrue('k1' in self.d)
        self.assertFalse('k2' in self.d)
        self.assertTrue('k3' in self.d)
        self.assertTrue('new_k1' in self.d)
        self.assertTrue('new_k2' in self.d)
        self.assertTrue('new_k3' in self.d)

        # Confirm the actual stored items from items()
        expected_items = {('k1', 1), ('k3', 3), ('new_k1', 10), ('new_k2', 20), ('new_k3', 30)}
        self.assertCountEqual(set(self.d.items()), expected_items)

    def test_insertion_into_tombstone_slot(self):
        # Create a collision chain and delete the middle element to make a tombstone
        # We need to pick keys that are highly likely to collide and probe linearly
        # Let's try simple integers where hash(x) = x
        # This might require some tuning based on your probing `(5 * seed + 1 + p)`
        # For a generic test, we'll try to trigger it by adding many items
        # that could create dense areas.

        # Fill almost to resize capacity
        for i in range(4): # k0, k1, k2, k3
            self.d[f'test_key_{i}'] = f'val_{i}'
        self.assertEqual(self.d.max_len, 8)
        self.assertEqual(len(self.d), 4)

        # Delete one item. This creates a tombstone.
        # Let's pick 'test_key_1' for deletion
        del self.d['test_key_1']
        self.assertEqual(len(self.d), 3) # Test_key_1 is now a tombstone

        # Now insert a new key. If _get_next_index works correctly,
        # it should find the tombstone first for a good hash.
        # This new key should hash to a location *before* the tombstone
        # in the natural probe order, and then ideally pick up the tombstone.
        # This is hard to guarantee without knowing exact hash and probe.
        # Simpler approach: Rely on the _get_next_index logic to find the first_available_slot.

        # If _get_next_index prioritizes tombstones for insertion, this will reuse one.
        # The resize test also implicitly covers this when it re-inserts.
        self.d['new_key_reusing_slot'] = 'new_value'
        self.assertEqual(len(self.d), 4)
        self.assertEqual(self.d['new_key_reusing_slot'], 'new_value')
        self.assertFalse('test_key_1' in self.d) # Still deleted

        # Add enough to trigger a resize, which will compact the entries
        self.d['force_resize_1'] = 1
        self.d['force_resize_2'] = 2 # This triggers resize
        self.assertEqual(self.d.max_len, 16) # Resized
        print(self.d)
        self.assertEqual(len(self.d), 6) # k0, k2, k3, new_key_reusing_slot, force_resize_1, force_resize_2
        self.assertFalse('test_key_1' in self.d) # Confirms tombstone was handled and not re-inserted

    # --- Edge Cases and General Robustness ---

    def test_many_insertions_and_resizes(self):
        num_items = 100
        for i in range(num_items):
            self.d[str(i)] = i * 10
            # Check a few random items to ensure they're there during growth
            if i % 10 == 0 and i > 0:
                self.assertEqual(self.d[str(i-5)], (i-5) * 10) # check something earlier

        self.assertEqual(len(self.d), num_items)
        for i in range(num_items):
            self.assertEqual(self.d[str(i)], i * 10)

    def test_insert_delete_insert_cycle(self):
        self.d['cycle_key'] = 'initial'
        self.assertEqual(len(self.d), 1)
        del self.d['cycle_key']
        self.assertEqual(len(self.d), 0)
        self.assertFalse('cycle_key' in self.d)

        self.d['cycle_key'] = 'reinserted'
        self.assertEqual(len(self.d), 1)
        self.assertEqual(self.d['cycle_key'], 'reinserted')
        self.assertTrue('cycle_key' in self.d)

        # Delete again
        del self.d['cycle_key']
        self.assertEqual(len(self.d), 0)
        self.assertFalse('cycle_key' in self.d)

    def test_keys_with_same_hash_different_value(self):
        # This is a challenging one for hash tables.
        # We need to craft two objects that have the same hash but are not equal.
        # Python's default hash for objects usually relies on id(), so this is hard.
        # For strings/numbers, hash(x) is usually unique.
        # Example: Custom objects with __hash__ and __eq__
        class CustomKey:
            def __init__(self, val, hash_val):
                self.val = val
                self._hash_val = hash_val
            def __hash__(self):
                return self._hash_val
            def __eq__(self, other):
                if not isinstance(other, CustomKey):
                    return False
                return self.val == other.val # Equal only if vals are same
            def __repr__(self):
                return f"CustomKey({self.val}, hash={self._hash_val})"

        k1 = CustomKey('alpha', 123)
        k2 = CustomKey('beta', 123) # Same hash as k1, different value

        self.assertEqual(hash(k1), hash(k2))
        self.assertNotEqual(k1, k2) # Ensure they are not equal

        self.d[k1] = 'value_alpha'
        self.assertEqual(self.d[k1], 'value_alpha')
        self.assertEqual(len(self.d), 1)

        self.d[k2] = 'value_beta' # This should trigger a collision and probe
        self.assertEqual(self.d[k2], 'value_beta')
        self.assertEqual(self.d[k1], 'value_alpha') # Ensure k1 is still there
        self.assertEqual(len(self.d), 2)

        del self.d[k1]
        self.assertEqual(len(self.d), 1)
        self.assertFalse(k1 in self.d)
        self.assertTrue(k2 in self.d)
        self.assertEqual(self.d[k2], 'value_beta')

        del self.d[k2]
        self.assertEqual(len(self.d), 0)
        self.assertFalse(k2 in self.d)

    def test_non_hashable_key(self):
        # Lists are not hashable
        with self.assertRaises(TypeError):
            self.d[[1, 2]] = 'list_value'

    def test_empty_key_and_value(self):
        self.d[''] = '' # Empty string key, empty string value
        self.assertEqual(self.d[''], '')
        self.assertEqual(len(self.d), 1)

        self.d[None] = None # None as key, None as value
        self.assertEqual(self.d[None], None)
        self.assertEqual(len(self.d), 2)

        del self.d['']
        self.assertFalse('' in self.d)
        self.assertTrue(None in self.d)


# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
