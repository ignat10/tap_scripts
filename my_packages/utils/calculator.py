from my_packages.data.accounts import farms

decryptor = {
    1: [1, 0],
    2: [1, 1],
}
bots = []
for x in farms:
    bots.extend(decryptor[x])
