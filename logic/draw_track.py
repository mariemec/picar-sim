from PIL import Image
import numpy as np

## After calling the following method on sim.trajectoire.map
# def print_map_to_file(self):
#     rotated = [[self._map[j][i] for j in range(len(self._map))] for i in range(len(self._map[0]) - 1, -1, -1)]
#     my_track = open("output.txt", "w")
#     for row in rotated:
#         np.savetxt(my_track, row)
#     my_track.close()

# Use this main to generate a black and white image of the track
if __name__ == '__main__':
    original_array = np.loadtxt("output.txt").reshape(300, 300).astype('uint8')*255
    im = Image.fromarray(original_array)
    im.save('track.png')