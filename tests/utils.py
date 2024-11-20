def test_multiple_objects(obj_list, assertion_func):
    """
    Generic test function for validating multiple objects

    Args:
        client_response: List or iterator of objects to validate
        assertion_func: Function to use for asserting each object's structure
    """
    assert obj_list is not None, "Response should not be None"

    # Handle both lists and iterators
    objects = list(obj_list)

    # Validate each object
    for obj in objects:
        assertion_func(obj)
