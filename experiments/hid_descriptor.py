"""Inspect short HID descriptor items without opening a device."""


def input_fields(descriptor):
    page = size = count = offset = minimum = maximum = 0
    usages, usage_min, usage_max = [], None, None
    fields, stack = [], []
    index = 0
    while index < len(descriptor):
        prefix = descriptor[index]
        index += 1
        if prefix == 0xfe:
            raise ValueError('Long HID items are not supported by this inspector')
        length = (0, 1, 2, 4)[prefix & 3]
        data = descriptor[index:index + length]
        if len(data) != length:
            raise ValueError('Truncated HID item')
        index += length
        value = int.from_bytes(data, 'little')
        kind, tag = (prefix >> 2) & 3, prefix >> 4
        if kind == 1:
            if tag == 0:
                page = value
            elif tag == 1:
                minimum = int.from_bytes(data, 'little', signed=True)
            elif tag == 2:
                maximum = int.from_bytes(data, 'little', signed=minimum < 0)
            elif tag == 7:
                size = value
            elif tag == 8:
                raise ValueError('Report IDs require separate report state; not supported')
            elif tag == 9:
                count = value
            elif tag == 10:
                stack.append((page, size, count, minimum, maximum))
            elif tag == 11:
                page, size, count, minimum, maximum = stack.pop()
        elif kind == 2:
            if tag == 0:
                usages.append((page, value))
            elif tag == 1:
                usage_min = value
            elif tag == 2:
                usage_max = value
        elif kind == 0:
            if tag == 8:
                if not 1 <= size <= 32 or not 1 <= count <= 128:
                    raise ValueError('Invalid or excessive report dimensions')
                if usage_min is not None and usage_max is not None:
                    if not 0 <= usage_min <= usage_max <= 0xffff or usage_max - usage_min > 127:
                        raise ValueError('Invalid or excessive usage range')
                    usages += [(page, usage) for usage in range(usage_min, usage_max + 1)]
                for number in range(count):
                    usage = usages[min(number, len(usages) - 1)] if usages and not value & 1 else None
                    fields.append((offset, size, usage, value, minimum, maximum))
                    offset += size
            usages, usage_min, usage_max = [], None, None
    if stack:
        raise ValueError('Unbalanced global HID state')
    return offset, fields
