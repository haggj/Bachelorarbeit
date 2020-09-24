import gprof2dot

def extract_hotspots(callgrind, count):
    """Opens a callgrind.out file and finds the most expensive functions

    Args:
        callgrind (path): Path to callgrind function
        count (int): Number of functions to return

    Returns:
       list of the most expensive functions.
    """
    f = open(callgrind)
    parser = gprof2dot.CallgrindParser(f)
    profile = parser.parse()

    
    class Function:
        def __init__(self, name, instructions, percentage):
            self.absolute_instructions = instructions
            self.name = name
            self.percentage = percentage

        def __str__(self):
            return self.name.split("/")[-1] + ": " + str(round(self.percentage*100,2)) + "%"
    
    functions = []
    for name, fun in profile.functions.items():
        percentage=None
        samples=None
        for event, value in fun.events.items():
            if event.name=="Time ratio":
                percentage=value
            elif event.name=="Samples":
                samples=value
        if percentage and samples:
            functions.append(Function(name, samples, percentage))


    functions = sorted(functions, key=lambda func: func.percentage, reverse=True)
    return [str(f) for f in functions[:count]]


def extract_function_calls(callgrind, function):
    """Opens a callgrind.out file and returns all functions called within the specified function.

    Args:
        callgrind (path): Path to callgrind file
        function (string): Name of a called function

    Returns:
       dictionary that contains all called function with the specified function as keys (values are the measured opcounts)
    """
    f = open(callgrind)
    parser = gprof2dot.CallgrindParser(f)
    profile = parser.parse()

    ret = {}

    for call in profile.functions[function].calls.values():
        callee = profile.functions[call.callee_id]
        for event, data in call.events.items():
            if event.name == "Samples":
                ret[callee.name] = int(data)
    return ret