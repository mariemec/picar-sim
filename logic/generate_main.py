def generate_main():
    files = ["position.py", "bille.py", "car.py",  "trajectoire.py", "simulation.py"]
    out_lines = list()

    for filename in files:
        f = open(filename, "r")
        lines = f.readlines()
        out_lines.append(lines)

    out_file = open("main.py", "w")
    out_file.write("import bpy\n")
    out_file.write("import numpy as np\n")
    for line in out_lines:
        for str in line:
            if not str.startswith("from simulation") and not str.startswith("from position"):
                out_file.write(str)
    out_file.close()


if __name__ == '__main__':
    generate_main()
