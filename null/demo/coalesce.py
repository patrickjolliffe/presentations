num_args = 65536

with open("coalesce.sql", "w") as file:
    file.write("select coalesce(1);\n\n")

    file.write("select coalesce(\n")
    for i in range(1, num_args + 1):
        file.write(f"{i}")
        if i < num_args:
            file.write(",")
            if i % 10 == 0:
                file.write("\n")    
    file.write(");\n")