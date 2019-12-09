from ...classes import Solution


COLORS = {
    "0": f'\033[40m  \033[0m',
    "1": f'\033[47m  \033[0m',
}


def parse_input(data):
    return data[0].strip()


def chunk(iter, size):
    for i in range(0, len(iter), size):
        yield iter[i:i + size]


def sif_decode(data, width, height):
    image = []
    layer_size = width * height
    layers = list(chunk(data, layer_size))
    for layer in layers:
        rows = list(chunk(layer, width))
        image.append(rows)
    return image


def sif_checksum(image):
    min_count = len(image[0][0]) + 1
    target_layer_id = None
    for layer_id, layer in enumerate(image):
        zeroes = sum(row.count("0") for row in layer)
        if zeroes < min_count:
            target_layer_id = layer_id
            min_count = zeroes
    target_layer = image[target_layer_id]
    ones = sum(row.count("1") for row in target_layer)

    twos = sum(row.count("2") for row in target_layer)
    return ones * twos


def render_image(image):
    # apply the layers to get the actual colors
    rendered = ""
    height = len(image[0])
    width = len(image[0][0])
    for row in range(height):
        colored_row = []
        for pixel in range(width):
            color = "2"
            layer = 0
            while color == "2":
                color = image[layer][row][pixel]
                layer += 1
            rendered += COLORS[color]
        rendered += "\n"
    return rendered


def phase1(data):
    width = 25
    height = 6
    image = sif_decode(data, width, height)
    checksum = sif_checksum(image)
    return checksum


def phase2(data):
    width = 25
    height = 6
    image = sif_decode(data, width, height)
    render = render_image(image)
    return "\n" + render


solution = Solution(2019, 8, phase1=phase1, phase2=phase2, input_parser=parse_input)
