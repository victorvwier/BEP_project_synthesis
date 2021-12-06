def horizontal_string_join(s1, s2):
    rows1 = s1.split("\n")
    width = max(len(row) for row in rows1)
    rows2 = s2.split("\n")
    rows = []
    height = max(len(rows1), len(rows2))
    rows1 += ([""] * (height - len(rows1)))
    rows2 += ([""] * (height - len(rows2)))
    rows = [rows1[i] + " " * (width-len(rows1[i])) + "   " + rows2[i] for i in range(height)]
    return "\n".join(rows)
