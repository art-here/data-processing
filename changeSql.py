import gspread


def read():
    gc = gspread.service_account(filename="./art-here.json")
    sh = gc.open("art-here").worksheet("시트1")
    table = sh.get_all_values()

    f = open("sql.txt", 'w', encoding="UTF-8")

    for i in range(1, len(table)):
        data = ["insert into arts ("]

        for j in range(12):
            data.append("%s, " % table[0][j])

        data.append("%s) values (" % table[0][12])

        for j in range(12):

            if 7 < j < 10 or (j == 11 and table[i][j] == "NULL"):
                data.append("%s, " % table[i][j])

            else:
                data.append("'%s', " % table[i][j])

        data.append("'%s');" % table[i][12])

    f.write(''.join(data))
    f.close()

    print("processed")


if __name__ == '__main__':
    read()
