import sys
import argparse
import csv


LINE_SEP = '=================================================================================================================================='


class Rules(object):
    pass


class Items(object):
    def __init__(self, filename, features):
        self.filename = filename
        self.features = features

    def render(self):
        items_header = []
        item_html = []
        with open(self.filename, 'r') as f:
            data = csv.reader(f)
            next_item = 0
            features = []
            for count, row in enumerate(data):
                if count == 0:
                    items_header = [self.FEATURES['Head'].format(header) for header in row[1:]]
                    continue

                temp = row[0].split('_')
                category, feature_name = ''.join(temp[:-1]), temp[-1]
                next_item += 1
                features.append([self.FEATURES[feature_name].format(item) for item in row[1:]])

                if next_item == self.FEATURES_COUNT:
                    next_item = 0
                    items_html = []
                    for c, header in enumerate(items_header):
                        item_html = ''
                        item_html += header
                        for feature in features:
                            item_html += feature[c]
                        items_html.append(self.ITEM_WRAPPER_HTML.format(item_html))
                    print LINE_SEP
                    print "CATEGORY: ", category
                    print LINE_SEP
                    print self.WRAPPER_HTML.format(''.join(items_html))
                    features = []


class VerticalItems(Items):
    """
    This class represents the data structure of Vertical list of items like one after the other by item and not feature
    """
    WRAPPER_HTML = '<div class="items cmp-ver">{}</div>'
    ITEM_WRAPPER_HTML = '<div class="item">{}</div>'
    FEATURES_COUNT = 2
    FEATURES = {'Descr': '<div class="item-descr">{}</div>', 'Source': '<div class="item-source">{}</div>', 'Head': '<div class="item-head">{}</div>'}

    def __init__(self, *args, **kwargs):
        super(VerticalItems, self).__init__(*args, **kwargs)
        pass


class HorizontalItems(Items):
    pass


if __name__ == '__main__':
    ITEMS_TYPE = {'0': VerticalItems, '1': HorizontalItems}

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--features', dest='features', default=None, help='Features to iterate for vertically')
    parser.add_argument('-f', '--filename', dest='filename', default='', help='File name to read and emit the html')
    parser.add_argument('-t', '--itemstype', dest='itemstype', default=0, help='Items Types whether vertical 0 or Horizontal 1')

    argus = parser.parse_args()
    print argus

    if not argus.filename:
        print "File name must be specified."
        sys.exit()

    items_processor = ITEMS_TYPE.get(argus.itemstype, VerticalItems)
    proces = items_processor(argus.filename, argus.features)
    proces.render()
