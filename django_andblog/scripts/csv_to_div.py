import sys
import argparse


class Items(object):
    def __init__(self, filename, features):
        self.filename = filename
        self.features = features

    def render(self):
        pass


class VerticalItems(Items):
    """
    This class represents the data structure of Vertical list of items like one after the other by item and not feature
    """
    FEATURES = {'Descr': ('div', 'item-descr', ), 'Source': ('div', 'item-source'), 'Head': ('div', 'item-head')}

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

    items_processor = ITEMS_TYPE.get(argus.itemstype, 0)
    proces = items_processor(argus.filename, argus.features)
    proces.render()
