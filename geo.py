def get_ll_spn(toponym: dict):
    object_ll = ','.join(toponym['Point']['pos'].split())
    envelope = toponym['boundedBy']['Envelope']
    left, bottom = envelope['lowerCorner'].split()
    right, top = envelope['upperCorner'].split()
    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    object_spn = f"{dx},{dy}"
    return object_ll, object_spn

