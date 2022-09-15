def plotResult(my_dict, title='', order=False):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm
    plt.rcParams["figure.figsize"] = (20,10)

    max_value = max(my_dict.values()) / 100
    my_dict_items = list(my_dict.items())
    if order:
        my_dict_items = sorted(my_dict_items, key=lambda item: item[1])

    pn_i = np.linspace(0, 1, len(my_dict_items))        # Range de float para a função cm.jet selecionar as cores
    for i in range(len(my_dict_items)):
        x = my_dict_items[i][0]
        y = my_dict_items[i][1]
        plt.bar(x,
                y,
                color=cm.jet(pn_i[i]),
                label=x)
        plt.text(x, y+max_value, str(y))

    plt.xticks(rotation=90)
    plt.title(title)

    plt.show()


def transformDicts(unsend_dict, mongo_connector):
    total_dict = dict()
    current_dict = dict()
    for document in mongo_connector.getAllDocuments():
        if (document['_id'] in unsend_dict.keys()):
            id = document['_id']
            name = document['name']
            total_value = len(document['video_ids'])
            current_value = len(unsend_dict[id])

            total_dict[name] = total_value
            current_dict[name] = current_value

    return (total_dict, current_dict)


def transformTotalDicts(mongo_connector):
    total_dict = dict()
    for document in mongo_connector.getAllDocuments():
        name = document['name']
        total_value = len(document['video_ids'])

        total_dict[name] = total_value

    return total_dict