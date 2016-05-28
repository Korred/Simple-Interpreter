import pygame

title = "Game Of Life"

# The framerate of the game (in milliseconds)
framerate = 15
screen_dim = (1000, 500)
cell_size = 5


def from_lifestring(string):
    '''
    Creates Game of Life field from given string
    returns set with (x,y) coordinates of living cells
    '''

    lines = string.split("\n")
    field = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'X':
                field.add((x, y))

    return field


def center_cells(field):
    '''
    centers cells in field
    '''
    new_field = set()
    x_min, y_min = map(min, zip(*field))
    x_max, y_max = map(max, zip(*field))

    field_size_x = screen_dim[0] // cell_size
    field_size_y = screen_dim[1] // cell_size

    x_move = (field_size_x // 2) - ((x_max - x_min) // 2)
    y_move = (field_size_y // 2) - ((y_max - y_min) // 2)
    for cell in field:
        new_field.add((cell[0] + x_move, cell[1] + y_move))

    return new_field


def lifestep(field):
    offset = range(-1, 2)
    new_field = set()
    # for every neighbour of a living cell
    # count adjacent living cells
    # if neighbour was a living cell and has 2-3 adjacent living cells -> add to new field
    # if neighbour was a dead cell and has 3 adjacent living cells -> add to new field

    for cell in field:
        for y in offset:
            for x in offset:
                check = (cell[0] + x, cell[1] + y)
                adjacent = 0
                for cy in offset:
                    for cx in offset:
                        neighbour = (check[0] + cy, check[1] + cx)
                        if neighbour in field and neighbour != check:
                            adjacent += 1
                if check in field:
                    if adjacent == 2 or adjacent == 3:
                        new_field.add(check)
                else:
                    if adjacent == 3:
                        new_field.add(check)

    return new_field


def main():

    while True:
        path = input("Provide path to .life file: ")
        try:
            with open(path) as f:
                field = center_cells(from_lifestring(f.read()))
            break
        except FileNotFoundError:
            print("File at '{}' does not exist".format(path))
            print()

    # Initialize pygame elements
    screen, bg, clock = init_screen()

    # Even loop
    while True:
        clock.tick(framerate)
        for cell in field:
            c = (cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(bg, (255, 0, 0), c)

        # draw the background screen to the actual one
        screen.blit(bg, (0, 0))
        # update the screen
        pygame.display.flip()

        # look out for window close events:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        field = lifestep(field)
        bg.fill((0, 0, 0))


def init_screen():
    pygame.init()
    screen = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption(title)
    bg = pygame.Surface(screen_dim)
    clock = pygame.time.Clock()
    return screen, bg, clock


main()
